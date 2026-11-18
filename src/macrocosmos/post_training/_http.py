"""The one HTTP connection to the gateway: auth headers, error mapping, retries."""

from __future__ import annotations

import json
import os
import time
from typing import Any, Optional

import httpx

from macrocosmos import __package_name__, __version__

from .errors import APIConnectionError, PostTrainingError, error_for_status

API_KEY_ENV = "MACROCOSMOS_POST_TRAINING_API_KEY"
BASE_URL_ENV = "MACROCOSMOS_POST_TRAINING_BASE_URL"
# The post-training routes sit under this prefix on the gateway. The planned
# standalone gateway serves them under `/v1`; moving there is this one line
# (and the base URL).
API_PREFIX = "/platform/rl"
# Routes that sit outside the prefix on the current gateway.
_OUTSIDE_PREFIX = {"/base-models": "/platform/base-models"}


def url_path(path: str) -> str:
    """The gateway path for a route, given relative to the prefix (`/sessions`)."""
    return _OUTSIDE_PREFIX.get(path) or API_PREFIX + path


# Request bodies over 16 KB are refused. Stay under that with some headroom.
MAX_BODY_BYTES = 15 * 1024

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
    ) -> None:
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

    def request(
        self, method: str, path: str, body: Any = None, *, idempotent: bool = True
    ) -> Any:
        """Send one request; return the decoded JSON or raise a typed error.

        Reads and idempotent writes (closing a session, creating its model,
        training ops deduplicated by `seq_id`) are retried on transport errors
        and 502/503/504. A non-idempotent write (opening a session, submitting
        samples) is retried only when it never reached the server, so a retry
        can't open a second session or pay for samples twice.
        """
        if self.closed:
            raise PostTrainingError(
                "this client is closed; create a new one to keep going"
            )
        content = None if body is None else encode(body)
        headers = {"content-type": "application/json"} if content else None
        for attempt in range(_RETRIES + 1):
            last = attempt == _RETRIES
            try:
                resp = self._http.request(
                    method, url_path(path), content=content, headers=headers
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

    def close(self) -> None:
        self.closed = True
        self._http.close()


def _decode(resp: httpx.Response) -> Any:
    if resp.is_success:
        return resp.json() if resp.content else None
    try:
        body = resp.json()
        detail = body.get("detail", body) if isinstance(body, dict) else body
    except ValueError:  # some errors (413) come back as HTML
        body, detail = resp.text, resp.reason_phrase
    if resp.status_code == 413:
        detail = f"{detail} (request bodies are limited to 16 KB; send fewer datums per call)"
    where = f"{resp.request.method} {resp.request.url.path}"
    raise error_for_status(
        resp.status_code, f"{where}: {resp.status_code} {detail}", body
    )
