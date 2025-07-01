import asyncio
import threading


def run_sync_threadsafe(coro):
    """
    Run async code synchronously, even if inside a running event loop.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        # If there's no running event loop, run the coroutine directly
        return asyncio.run(coro)

    # If we get here, there's a running event loop - use thread-safe approach
    result = None
    exception = None

    def runner():
        nonlocal result, exception
        try:
            result = asyncio.run(coro)
        except Exception as e:
            exception = e

    thread = threading.Thread(target=runner)
    thread.start()
    thread.join()

    if exception:
        raise exception
    return result
