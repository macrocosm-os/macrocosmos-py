import random
from typing import AsyncIterator, Dict, List, Optional, Union

import grpc

from macrocosmos import __package_name__, __version__
from macrocosmos.generated.apex.v1 import apex_p2p, apex_pb2, apex_pb2_grpc
from macrocosmos.resources._stream import StreamGenerator
from macrocosmos.resources._client import BaseClient
from macrocosmos.types import (
    ChatCompletionChunkResponse,
    ChatCompletionResponse,
    ChatMessage,
    MacrocosmosError,
    SamplingParameters,
)
from macrocosmos.resources._utils import run_sync_threadsafe


class AsyncCompletions:
    """Asynchronous Completions resource for the Apex (subnet 1) API."""

    def __init__(self, client: BaseClient):
        """
        Initialize the asynchronous Completions resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client

    async def create(
        self,
        messages: List[Union[ChatMessage, Dict]] = None,
        sampling_parameters: Union[SamplingParameters, Dict] = None,
        stream: bool = False,
        seed: Optional[int] = None,
        **kwargs,
    ) -> Union[ChatCompletionResponse, AsyncIterator[ChatCompletionChunkResponse]]:
        """
        Create a chat completion.

        Args:
            messages: A list of messages comprising the conversation so far.
            sampling_parameters: The sampling parameters to use for the completion.
            stream: Whether to stream the response.
            seed: The seed to use for the completion.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A completion response or a stream of completion chunks.
        """
        if seed is None:
            seed = random.randint(0, 2**16 - 1)

        proto_messages = []
        if messages:
            for msg in messages:
                if isinstance(msg, apex_p2p.ChatMessage):
                    proto_messages.append(apex_pb2.ChatMessage(**msg.model_dump()))
                elif isinstance(msg, dict):
                    proto_messages.append(apex_pb2.ChatMessage(**msg))
                else:
                    raise TypeError(f"Invalid type for message: {type(msg)}")
        else:
            raise AttributeError("messages is a required parameter")

        proto_sampling_params = None
        if sampling_parameters:
            if isinstance(sampling_parameters, apex_p2p.SamplingParameters):
                proto_sampling_params = apex_pb2.SamplingParameters(
                    **sampling_parameters.model_dump()
                )
            elif isinstance(sampling_parameters, dict):
                proto_sampling_params = apex_pb2.SamplingParameters(
                    **sampling_parameters
                )
            else:
                raise TypeError(
                    f"Invalid type for sampling_parameters '{type(sampling_parameters)}'"
                )
        else:
            proto_sampling_params = apex_pb2.SamplingParameters(
                temperature=0.7,
                top_p=0.95,
                max_new_tokens=4096,
                do_sample=True,
            )

        if "timeout" not in kwargs and self._client.timeout:
            kwargs["timeout"] = self._client.timeout

        request = apex_pb2.ChatCompletionRequest(
            messages=proto_messages,
            sampling_parameters=proto_sampling_params,
            stream=stream,
            seed=seed,
            **kwargs,
        )

        metadata = [
            ("x-source", self._client.app_name),
            ("x-client-id", __package_name__),
            ("x-client-version", __version__),
            ("authorization", f"Bearer {self._client.api_key}"),
        ]

        compression = grpc.Compression.Gzip if self._client.compress else None

        retries = 0
        last_error = None
        while retries <= self._client.max_retries:
            try:
                channel = self._client.get_async_channel()
                stub = apex_pb2_grpc.ApexServiceStub(channel)
                if not stream:
                    response = await stub.ChatCompletion(
                        request,
                        metadata=metadata,
                        timeout=kwargs.get("timeout", self._client.timeout),
                        compression=compression,
                    )
                    await channel.close()
                    return response
                else:
                    stream_response = stub.ChatCompletionStream(
                        request,
                        metadata=metadata,
                        timeout=kwargs.get("timeout", self._client.timeout),
                        compression=compression,
                    )

                    return StreamGenerator[ChatCompletionChunkResponse](
                        stream_response, channel
                    )
            except grpc.RpcError as e:
                last_error = MacrocosmosError(f"RPC error: {e.code()}: {e.details()}")
                retries += 1
                await channel.close()
            except Exception as e:
                await channel.close()
                raise MacrocosmosError(f"Error creating chat completion: {e}")

        raise last_error


class AsyncChat:
    """Asynchronous Chat resource for the Apex (subnet 1) API."""

    def __init__(self, client: BaseClient):
        """
        Initialize the asynchronous Chat resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client
        self.completions = AsyncCompletions(client)


class SyncCompletions:
    """Synchronous Completions resource for the Apex (subnet 1) API."""

    def __init__(self, client: BaseClient):
        """
        Initialize the synchronous Completions resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client
        self._async_completions = AsyncCompletions(client)

    def create(
        self,
        messages: List[Union[ChatMessage, Dict]] = None,
        sampling_parameters: Union[SamplingParameters, Dict] = None,
        seed: Optional[int] = None,
        **kwargs,
    ) -> apex_p2p.ChatCompletionResponse:
        """
        Create a chat completion synchronously.

        Args:
            messages: A list of messages comprising the conversation so far.
            sampling_parameters: The sampling parameters to use for the completion.
            seed: The seed to use for the completion.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A completion response.
        """

        if "timeout" not in kwargs and self._client.timeout:
            kwargs["timeout"] = self._client.timeout

        return run_sync_threadsafe(
            self._async_completions.create(
                messages=messages,
                sampling_parameters=sampling_parameters,
                stream=False,
                seed=seed,
                **kwargs,
            )
        )


class SyncChat:
    """Synchronous Chat resource for the Apex (subnet 1) API."""

    def __init__(self, client: BaseClient):
        """
        Initialize the synchronous Chat resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client
        self.completions = SyncCompletions(client)
