from typing import AsyncIterator, Generic, TypeVar

from grpc.aio import Channel

T = TypeVar("T")


class StreamGenerator(Generic[T], AsyncIterator[T]):
    """Generator for async iterator to close the channel when the iterator is closed."""

    def __init__(self, stream_response: AsyncIterator[T], channel: Channel):
        self._generator = self.stream_generator(stream_response)
        self._channel = channel

    async def stream_generator(self, stream_response: AsyncIterator[T]):
        async for chunk in stream_response:
            yield chunk

    def __aiter__(self):
        return self

    async def __anext__(self) -> T:
        try:
            return await self._generator.__anext__()
        except StopAsyncIteration:
            await self._channel.close()
            raise

    async def aclose(self):
        await self._channel.close()
