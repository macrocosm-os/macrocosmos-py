"""The Macrocosmos RL endpoints, over HTTP.

`POST /platform/rl/sessions` opens a session and returns its `session_id`;
`POST /platform/rl/sessions/{id}/close` closes it. `POST /platform/rl/inference`
queues one sampling task per prompt for a session and returns a handle.
`GET /platform/rl/inference/{handle}` returns `{"results": null}` until every
task has finished, then one result per prompt.
"""

from __future__ import annotations

import time
from typing import Any

import httpx

from macrocosmos import __package_name__, __version__
from macrocosmos.types._exceptions import MacrocosmosError


class RlPlatformClient:
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
        self._http = httpx.Client(base_url=base_url.rstrip("/"), headers=headers, timeout=timeout)

    def close(self) -> None:
        self._http.close()

    def open_session(self, *, base_model: str, requirements: dict[str, Any]) -> dict[str, Any]:
        """Open an RL session; returns it, including its `session_id`."""
        body = {"base_model": base_model, "requirements": requirements}
        return _json(self._http.post("/platform/rl/sessions", json=body))

    def close_session(self, session_id: str) -> dict[str, Any]:
        """Close an RL session. Closing an already closed one is fine."""
        return _json(self._http.post(f"/platform/rl/sessions/{session_id}/close"))

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
        return _json(self._http.post("/platform/rl/inference", json=body))["handle"]

    def wait(self, handle: str, *, timeout: float = 600, interval: float = 1.0) -> list[dict[str, Any]]:
        """Poll until the batch has finished; returns one result per prompt."""
        deadline = time.monotonic() + timeout
        while True:
            results = _json(self._http.get(f"/platform/rl/inference/{handle}"))["results"]
            if results is not None:
                return results
            if time.monotonic() > deadline:
                # Usually no GPU worker is hosting this session yet.
                raise MacrocosmosError(f"no results for batch {handle} after {timeout:.0f}s")
            time.sleep(interval)


def _json(resp: httpx.Response) -> dict[str, Any]:
    if resp.is_error:
        raise MacrocosmosError(
            f"{resp.request.method} {resp.request.url.path}: {resp.status_code} {resp.text[:300]}"
        )
    return resp.json()
