"""The one HTTP connection to the gateway: auth headers, error mapping, retries."""

from __future__ import annotations

import json
import os
import threading
import time
from typing import Any, Dict, Optional

import httpx

from macrocosmos import __package_name__, __version__

from .errors import APIConnectionError, PostTrainingError, error_for_status

API_KEY_ENV = "MACROCOSMOS_POST_TRAINING_API_KEY"
BASE_URL_ENV = "MACROCOSMOS_POST_TRAINING_BASE_URL"
API_PREFIX_ENV = "MACROCOSMOS_POST_TRAINING_API_PREFIX"
MAX_REQUEST_BYTES_ENV = "MACROCOSMOS_POST_TRAINING_MAX_REQUEST_BYTES"
MAX_INFLIGHT_BYTES_ENV = "MACROCOSMOS_POST_TRAINING_MAX_INFLIGHT_BYTES"

# Every post-training route sits under this prefix on the gateway.
API_PREFIX = (os.environ.get(API_PREFIX_ENV) or "/v1").rstrip("/")


def url_path(path: str) -> str:
    """The gateway path for a route, given relative to the prefix (`/sessions`)."""
    return API_PREFIX + path


# Size limits for training data, as on Tinker: each request carries at most
# `max_request_bytes` (bigger batches are split across requests), and at most
# `max_inflight_bytes` of a session's data is queued on the gateway at once (more
# waits for earlier requests to finish). The gateway sets both in
# `GET /v1/client/config`, read once on first use, as Tinker's client reads its
# server's config. The `max_request_bytes=` / `max_inflight_bytes=` client options
# or the environment variables above override them; 0 turns the in-flight limit off.
LIMITS = ("max_request_bytes", "max_inflight_bytes")
# Room in each request for seq_id, loss_fn and its config.
_ENVELOPE_BYTES = 512


def _override(value: Optional[int], env: str) -> Optional[int]:
    """A size limit the user set: the option if given, else the environment, else None."""
    if value is None:
        raw = os.environ.get(env, "").strip().replace("_", "")
        if not raw:
            return None
        if not raw.isdigit():
            raise ValueError(f"{env} must be a whole number of bytes, got {raw!r}")
        value = int(raw)
    return _checked("", value)


def _checked(name: str, value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        where = f"the gateway's {name}" if name else "a size limit"
        raise ValueError(f"{where} must be a whole number of bytes >= 0, got {value!r}")
    return value


_RETRY_STATUS = frozenset({502, 503, 504})
_RETRIES = 4


def encode(body: Any) -> bytes:
    try:
        return json.dumps(body, separators=(",", ":"), allow_nan=False).encode()
    except (
        ValueError
    ) as e:  # NaN or infinity: not valid JSON, and a sign of a bug upstream
        raise ValueError(
            "a value to send is NaN or infinite; check the rewards and advantages"
        ) from e


class Gateway:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        *,
        timeout: float = 30.0,
        app_name: Optional[str] = None,
        transport: Optional[httpx.BaseTransport] = None,
        max_request_bytes: Optional[int] = None,
        max_inflight_bytes: Optional[int] = None,
    ) -> None:
        self._overrides = {
            "max_request_bytes": _override(max_request_bytes, MAX_REQUEST_BYTES_ENV),
            "max_inflight_bytes": _override(max_inflight_bytes, MAX_INFLIGHT_BYTES_ENV),
        }
        _check_request_limit(self._overrides["max_request_bytes"])
        self._config: Optional[Dict[str, int]] = None
        self._config_lock = threading.Lock()
        api_key = (api_key or os.environ.get(API_KEY_ENV) or "").strip()
        if not api_key:
            raise error_for_status(
                401, f"No API key: pass api_key= or set {API_KEY_ENV}"
            )
        base_url = (base_url or os.environ.get(BASE_URL_ENV) or "").strip().rstrip("/")
        if not base_url:
            raise PostTrainingError(f"No API URL: pass base_url= or set {BASE_URL_ENV}")
        headers = {
            "X-API-Key": api_key,
            "x-client-id": __package_name__,
            "x-client-version": __version__,
        }
        if app_name:
            headers["x-source"] = app_name
        self.base_url = base_url
        self.closed = False
        self._http = httpx.Client(
            base_url=base_url, headers=headers, timeout=timeout, transport=transport
        )
        # Signed storage URLs carry their own authorisation: never send them the API key.
        self._storage = httpx.Client(
            timeout=300.0, transport=transport, follow_redirects=True
        )

    def request(
        self,
        method: str,
        path: str,
        body: Any = None,
        *,
        idempotent: bool = True,
        retries: int = _RETRIES,
        timeout: Optional[float] = None,
    ) -> Any:
        """Send one request; return the decoded JSON or raise a typed error.

        Reads and idempotent writes (closing a session, creating its model,
        training ops deduplicated by `seq_id`) are retried on transport errors
        and 502/503/504. A non-idempotent write (opening a session, submitting
        samples) is retried only when it never reached the server, so a retry
        can't open a second session or pay for samples twice.

        `retries` and `timeout` (seconds) narrow this for calls that must not
        linger, such as closing sessions at exit.
        """
        if self.closed:
            raise PostTrainingError(
                "this client is closed; create a new one to keep going"
            )
        content = None if body is None else encode(body)
        headers = {"content-type": "application/json"} if content else None
        extra = {} if timeout is None else {"timeout": timeout}
        for attempt in range(retries + 1):
            last = attempt == retries
            try:
                resp = self._http.request(
                    method, url_path(path), content=content, headers=headers, **extra
                )
            except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                if last:
                    raise APIConnectionError(f"{method} {path}: {e}") from e
            except httpx.TransportError as e:
                if last or not idempotent:
                    raise APIConnectionError(f"{method} {path}: {e}") from e
            else:
                if last or not idempotent or resp.status_code not in _RETRY_STATUS:
                    return _decode(resp)
            time.sleep(min(0.5 * 2**attempt, 8.0))
        raise AssertionError("unreachable")

    @property
    def max_request_bytes(self) -> int:
        return self._limit("max_request_bytes")

    @property
    def max_inflight_bytes(self) -> int:
        return self._limit("max_inflight_bytes")

    def _limit(self, name: str) -> int:
        override = self._overrides[name]
        return override if override is not None else self._client_config()[name]

    def _client_config(self) -> Dict[str, int]:
        """The gateway's limits, read once (`GET /v1/client/config`)."""
        with self._config_lock:
            if self._config is None:
                reply = self.request("GET", "/client/config")
                if not isinstance(reply, dict) or any(n not in reply for n in LIMITS):
                    raise PostTrainingError(
                        f"the gateway's client config lacks {', '.join(LIMITS)}: {reply!r}"
                    )
                config = {name: _checked(name, reply[name]) for name in LIMITS}
                _check_request_limit(config["max_request_bytes"])
                self._config = config
            return self._config

    def fetch(self, url: str) -> bytes:
        """Download a signed storage URL (no API key is sent)."""
        try:
            resp = self._storage.get(url)
        except httpx.TransportError as e:
            raise APIConnectionError(f"downloading {url.split('?')[0]}: {e}") from e
        if not resp.is_success:
            raise error_for_status(
                resp.status_code,
                f"downloading {url.split('?')[0]}: {resp.status_code} {resp.reason_phrase}",
            )
        return resp.content

    def close(self) -> None:
        self.closed = True
        self._http.close()
        self._storage.close()


def _check_request_limit(value: Optional[int]) -> None:
    if value is not None and value <= _ENVELOPE_BYTES:
        raise ValueError(f"max_request_bytes must be over {_ENVELOPE_BYTES} bytes")


def _decode(resp: httpx.Response) -> Any:
    if resp.is_success:
        return resp.json() if resp.content else None
    try:
        body = resp.json()
        detail = body.get("detail", body) if isinstance(body, dict) else body
    except ValueError:  # not JSON, e.g. a proxy's HTML error page
        body, detail = resp.text, resp.reason_phrase
    if resp.status_code == 413:
        detail = (
            f"{detail} (the gateway takes smaller requests than this client sends; "
            f"lower max_request_bytes= or {MAX_REQUEST_BYTES_ENV})"
        )
    where = f"{resp.request.method} {resp.request.url.path}"
    raise error_for_status(
        resp.status_code, f"{where}: {resp.status_code} {detail}", body
    )
