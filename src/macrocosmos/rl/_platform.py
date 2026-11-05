"""The Macrocosmos RL endpoints, over HTTP.

`POST /platform/rl/sessions` opens a session and returns its `session_id`;
`POST /platform/rl/sessions/{id}/close` closes it. `POST /platform/rl/inference`
queues one sampling task per prompt for a session and returns a handle.
`GET /platform/rl/inference/{handle}` returns `{"results": null}` until every
task has finished, then one result per prompt.
"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import httpx

from macrocosmos import __package_name__, __version__
from macrocosmos.types._exceptions import MacrocosmosError

# Requests waited on at once; each waits in its own thread.
MAX_IN_FLIGHT = 64
# Statuses a poll retries: the service briefly unavailable.
_RETRY_STATUS = frozenset({502, 503, 504})


class RlPlatform:
    def __init__(
        self, *, api_key: str, base_url: str, timeout: float = 30, app_name: str | None = None
    ) -> None:
        headers = {
            "X-API-Key": api_key,
            "x-client-id": __package_name__,
            "x-client-version": __version__,
        }
        if app_name:
            headers["x-source"] = app_name
        self._http = httpx.Client(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
            # One kept-alive connection per thread that may be waiting.
            limits=httpx.Limits(max_keepalive_connections=MAX_IN_FLIGHT),
        )
        # Runs blocking submit-and-wait calls so callers get a future back.
        self.executor = ThreadPoolExecutor(max_workers=MAX_IN_FLIGHT, thread_name_prefix="mc-rl")

    def close(self) -> None:
        self.executor.shutdown(wait=False)
        self._http.close()

    def open_session(self, *, base_model: str, requirements: dict[str, Any]) -> dict[str, Any]:
        """Open an RL session; returns it, including its `session_id`."""
        body = {"base_model": base_model, "requirements": requirements}
        return _json(self._request("POST", "/platform/rl/sessions", json=body))

    def close_session(self, session_id: str) -> None:
        """Close an RL session. Closing an already closed one is fine."""
        _json(self._request("POST", f"/platform/rl/sessions/{session_id}/close"))

    def submit(
        self,
        *,
        session_id: str,
        prompts: list[dict[str, Any]],
        adapter: dict[str, Any] | None = None,
    ) -> str:
        """Queue a batch; returns its handle."""
        body: dict[str, Any] = {"session_id": session_id, "prompts": prompts}
        if adapter:
            body["adapter"] = adapter
        return _json(self._request("POST", "/platform/rl/inference", json=body))["handle"]

    def wait(self, handle: str, *, timeout: float, interval: float) -> list[dict[str, Any]]:
        """Poll until the request has finished; returns one result per prompt.

        A poll that fails in transit or with a 502/503/504 is retried until the
        deadline: the tasks are still running, and polling is safe to repeat."""
        deadline = time.monotonic() + timeout
        last_error: str | None = None
        while True:
            try:
                resp = self._request("GET", f"/platform/rl/inference/{handle}")
            except MacrocosmosError as e:
                last_error = str(e)
            else:
                if resp.status_code in _RETRY_STATUS:
                    last_error = f"{resp.status_code} {resp.text[:300]}"
                else:
                    results = _json(resp)["results"]
                    if results is not None:
                        return results
                    last_error = None
            if time.monotonic() > deadline:
                # With no error, usually no GPU worker is hosting this session yet.
                detail = f"; last error: {last_error}" if last_error else ""
                raise MacrocosmosError(f"no results for batch {handle} after {timeout:.0f}s{detail}")
            time.sleep(interval)

    def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        try:
            return self._http.request(method, path, **kwargs)
        except httpx.TransportError as e:
            raise MacrocosmosError(f"{method} {path}: {type(e).__name__}: {e}") from e


def _json(resp: httpx.Response) -> dict[str, Any]:
    where = f"{resp.request.method} {resp.request.url.path}"
    if resp.is_error:
        raise MacrocosmosError(f"{where}: {resp.status_code} {resp.text[:300]}")
    try:
        return resp.json()
    except ValueError as e:
        raise MacrocosmosError(f"{where}: response is not JSON: {resp.text[:300]}") from e
