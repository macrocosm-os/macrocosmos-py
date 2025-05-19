import asyncio
import random
from typing import List, Optional, Dict, Union

import grpc

from macrocosmos import __package_name__, __version__
from macrocosmos.generated.apex.v1 import apex_p2p, apex_pb2, apex_pb2_grpc
from macrocosmos.types import MacrocosmosError, ChatMessage, SamplingParameters
from macrocosmos.resources._client import BaseClient


class AsyncDeepResearch:
    """Asynchronous DeepResearch resource for the Apex (subnet 1) API."""

    def __init__(self, client: BaseClient):
        """
        Initialize the asynchronous DeepResearch resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client

    async def create_job(
        self,
        messages: List[Union[ChatMessage, Dict]] = None,
        sampling_parameters: Union[SamplingParameters, Dict] = None,
        stream: bool = True,
        seed: Optional[int] = None,
        **kwargs,
    ) -> apex_pb2.DeepResearcherJobSubmitResponse:
        """
        Create a new deep research job.

        Args:
            messages: A list of messages comprising the research query and context.
            sampling_parameters: The sampling parameters to use for the completion.
            stream: Whether to stream the response (default: True).
            seed: The seed to use for the completion.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A deep researcher job submit response containing the job ID, initial status created_at and updated_at info.
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

        # Handle sampling parameters
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
                max_new_tokens=8192,
                do_sample=False,
            )

        # Set default parameters if not provided
        if "inference_mode" not in kwargs:
            kwargs["inference_mode"] = "Chain-of-Thought"
        elif kwargs["inference_mode"] != "Chain-of-Thought":
            raise ValueError("inference_mode must be 'Chain-of-Thought'")

        if "task" not in kwargs:
            kwargs["task"] = "InferenceTask"

        if "mixture" not in kwargs:
            kwargs["mixture"] = False

        if "timeout" not in kwargs:
            kwargs["timeout"] = 2100

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
                channel = self._client.get_channel()
                stub = apex_pb2_grpc.ApexServiceStub(channel)
                response = await stub.SubmitDeepResearcherJob(
                    request,
                    metadata=metadata,
                    timeout=kwargs.get("timeout", self._client.timeout),
                    compression=compression,
                )
                await channel.close()
                return response
            except grpc.RpcError as e:
                last_error = MacrocosmosError(f"RPC error: {e.code()}: {e.details()}")
                retries += 1
                await channel.close()
            except Exception as e:
                await channel.close()
                raise MacrocosmosError(f"Error creating research job: {e}")

        raise last_error

    async def get_job_results(
        self,
        job_id: str,
        **kwargs,
    ) -> apex_pb2.DeepResearcherJobStatusResponse:
        """
        Get the status and current result of a deep research job.

        Args:
            job_id: The ID of the research job to check.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A deep researcher job status response containing the current status and results.
        """
        if not job_id:
            raise AttributeError("job_id is a required parameter")

        request = apex_pb2.GetDeepResearcherJobRequest(
            job_id=job_id,
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
                channel = self._client.get_channel()
                stub = apex_pb2_grpc.ApexServiceStub(channel)
                response = await stub.GetDeepResearcherJob(
                    request,
                    metadata=metadata,
                    timeout=kwargs.get("timeout", self._client.timeout),
                    compression=compression,
                )
                await channel.close()
                return response
            except grpc.RpcError as e:
                last_error = MacrocosmosError(f"RPC error: {e.code()}: {e.details()}")
                retries += 1
                await channel.close()
            except Exception as e:
                await channel.close()
                raise MacrocosmosError(f"Error getting research job status: {e}")

        raise last_error


class SyncDeepResearch:
    """Synchronous DeepResearch resource for the Apex (subnet 1) API."""

    def __init__(self, client: BaseClient):
        """
        Initialize the synchronous DeepResearch resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client
        self._async_deep_research = AsyncDeepResearch(client)

    def create_job(
        self,
        messages: List[Union[ChatMessage, Dict]] = None,
        sampling_parameters: Union[SamplingParameters, Dict] = None,
        stream: bool = True,
        seed: Optional[int] = None,
        **kwargs,
    ) -> apex_pb2.DeepResearcherJobSubmitResponse:
        """
        Create a new deep research job synchronously.

        Args:
            messages: A list of messages comprising the research query and context.
            sampling_parameters: The sampling parameters to use for the completion.
            stream: Whether to stream the response (default: True).
            seed: The seed to use for the completion.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A deep researcher job submit response containing the job ID, initial status created_at and updated_at info.
        """
        return asyncio.run(
            self._async_deep_research.create_job(
                messages=messages,
                sampling_parameters=sampling_parameters,
                stream=stream,
                seed=seed,
                **kwargs,
            )
        )

    def get_job_results(
        self,
        job_id: str,
        **kwargs,
    ) -> apex_pb2.DeepResearcherJobStatusResponse:
        """
        Get the status and results of a deep research job synchronously.

        Args:
            job_id: The ID of the research job to check.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A deep researcher job status response containing the current status and results.
        """
        return asyncio.run(
            self._async_deep_research.get_job_results(
                job_id=job_id,
                **kwargs,
            )
        )
