"""`APIFuture`: what every call returns, as on Tinker.

Calls are submitted when they're made, in order, so `forward_backward` and
`optim_step` can be queued back to back. The result is fetched when it's asked
for: `.result()` blocks, `await future` doesn't.
"""

from __future__ import annotations

import asyncio
import functools
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Generator, Generic, Optional, TypeVar

from .errors import APITimeoutError, RequestFailedError

T = TypeVar("T")
U = TypeVar("U")

_NOT_YET = object()

# Awaited futures wait in these threads. Waiting is mostly sleeping between
# polls, so a generous pool lets many samples be gathered at once.
_WAITERS = ThreadPoolExecutor(
    max_workers=128, thread_name_prefix="macrocosmos-post-training"
)


class APIFuture(Generic[T]):
    """The result of a call to the gateway.

    `future.result(timeout=None)` waits for it and returns it, or raises the
    call's error. `await future` does the same without blocking the event loop.
    A timeout leaves the call running: ask again to keep waiting.
    """

    def __init__(
        self, resolve: Callable[[Optional[float]], T], *, label: str = ""
    ) -> None:
        self._resolve = resolve
        self._label = label
        self._lock = threading.Lock()
        self._value: Any = _NOT_YET
        self._error: Optional[Exception] = None

    @classmethod
    def completed(cls, value: T, *, label: str = "") -> "APIFuture[T]":
        future: APIFuture[T] = cls(lambda _timeout: value, label=label)
        future._value = value
        return future

    def result(self, timeout: Optional[float] = None) -> T:
        deadline = None if timeout is None else time.monotonic() + timeout
        # Another thread may be waiting on this same call; wait our turn, within our timeout.
        if not self._lock.acquire(timeout=-1 if timeout is None else max(timeout, 0)):
            raise APITimeoutError(f"{self._label}: not finished after {timeout:g}s")
        try:
            if self._value is _NOT_YET and self._error is None:
                remaining = (
                    None if deadline is None else max(deadline - time.monotonic(), 0.0)
                )
                try:
                    self._value = self._resolve(remaining)
                except APITimeoutError:
                    raise  # not final: a later call may wait longer
                except Exception as e:  # noqa: BLE001 - kept, and raised to every caller
                    self._error = e
            if self._error is not None:
                raise self._error
            return self._value
        finally:
            self._lock.release()

    async def result_async(self, timeout: Optional[float] = None) -> T:
        if self.done():
            return self.result()
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            _WAITERS, functools.partial(self.result, timeout)
        )

    def __await__(self) -> Generator[Any, None, T]:
        return self.result_async().__await__()

    def then(self, fn: Callable[[T], U], *, label: str = "") -> "APIFuture[U]":
        """A future of `fn(result)`, resolved when it's asked for."""
        return APIFuture(
            lambda timeout: fn(self.result(timeout)), label=label or self._label
        )

    def done(self) -> bool:
        return self._value is not _NOT_YET or self._error is not None

    def __repr__(self) -> str:
        state = (
            "failed"
            if self._error is not None
            else "done"
            if self.done()
            else "pending"
        )
        return f"<APIFuture {self._label} {state}>"


def poll(
    fetch: Callable[[], Any],
    ready: Callable[[Any], bool],
    *,
    timeout: Optional[float],
    what: str,
) -> Any:
    """Call `fetch` until `ready(reply)`, backing off from 0.2 s to 2 s."""
    deadline = None if timeout is None else time.monotonic() + timeout
    delay = 0.2
    while True:
        reply = fetch()
        if ready(reply):
            return reply
        if deadline is not None and time.monotonic() + delay > deadline:
            raise APITimeoutError(f"{what}: not finished after {timeout:g}s")
        time.sleep(delay)
        delay = min(delay * 1.5, 2.0)


def wait_for_job(
    gateway: Any, handle: str, timeout: Optional[float], *, what: str = ""
) -> Any:
    """Wait for a training job (`GET .../training/{handle}`) and return its result.

    Only `done` and `failed` are final; any other state keeps it waiting.
    """
    job = poll(
        lambda: gateway.request("GET", f"/training/{handle}"),
        lambda j: j.get("state") in ("done", "failed"),
        timeout=timeout,
        what=what or handle,
    )
    if job["state"] == "failed":
        raise RequestFailedError(
            f"{what or handle} failed: {job.get('error') or 'no reason given'}",
            handle=handle,
        )
    return job.get("result") or {}


def run_in(
    executor: ThreadPoolExecutor, fn: Callable[..., T], *args: Any, **kwargs: Any
) -> "asyncio.Future[T]":
    """Run a blocking call in `executor` from async code."""
    return asyncio.get_running_loop().run_in_executor(
        executor, functools.partial(fn, *args, **kwargs)
    )
