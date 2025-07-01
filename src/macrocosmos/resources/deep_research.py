from typing import List, Optional, Dict, Union

import grpc

from macrocosmos import __package_name__, __version__
from macrocosmos.generated.apex.v1 import apex_p2p, apex_pb2, apex_pb2_grpc
from macrocosmos.types import MacrocosmosError, ChatMessage, SamplingParameters
from macrocosmos.resources._client import BaseClient
from macrocosmos.resources._utils import run_sync_threadsafe


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
        messages: List[Union[ChatMessage, Dict]],
        uids: Optional[List[int]] = None,
        model: Optional[str] = None,
        sampling_parameters: Optional[Union[SamplingParameters, Dict]] = None,
        seed: Optional[int] = None,
    ) -> apex_pb2.SubmitDeepResearcherJobResponse:
        """
        Create a new deep research job.

        Args:
            messages: A list of messages comprising the research query and context.
            uids: Optional list of specific miner UIDs to use. If not provided, the validator will select available miners.
            model: Optional model to use. If not provided, Apex will use the default model.
            sampling_parameters: Optional sampling parameters for the completion.
            seed: Optional seed for reproducibility. If not provided, a random seed will be used.

        Returns:
            A deep researcher job submit response containing the job ID, initial status created_at and updated_at info.
        """
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

        request = apex_pb2.ChatCompletionRequest(
            uids=uids,
            messages=proto_messages,
            seed=seed,
            task="InferenceTask",
            model=model,
            mixture=False,
            sampling_parameters=proto_sampling_params,
            inference_mode="Chain-of-Thought",
            stream=True,
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
            channel = None
            try:
                channel = self._client.get_async_channel()
                stub = apex_pb2_grpc.ApexServiceStub(channel)
                response = await stub.SubmitDeepResearcherJob(
                    request,
                    metadata=metadata,
                    timeout=self._client.timeout,
                    compression=compression,
                )
                return response
            except grpc.RpcError as e:
                last_error = MacrocosmosError(f"RPC error: {e.code()}: {e.details()}")
                retries += 1
            except Exception as e:
                raise MacrocosmosError(f"Error creating research job: {e}")
            finally:
                if channel:
                    await channel.close()

        raise last_error

    async def get_job_results(
        self,
        job_id: str,
    ) -> apex_pb2.GetDeepResearcherJobResponse:
        """
        Get the status and current result of a deep research job.

        Args:
            job_id: The ID of the research job to check.

        Returns:
            A deep researcher job status response containing the current status and results.
        """
        if not job_id:
            raise AttributeError("job_id is a required parameter")

        request = apex_pb2.GetDeepResearcherJobRequest(
            job_id=job_id,
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
            channel = None
            try:
                channel = self._client.get_async_channel()
                stub = apex_pb2_grpc.ApexServiceStub(channel)
                response = await stub.GetDeepResearcherJob(
                    request,
                    metadata=metadata,
                    timeout=self._client.timeout,
                    compression=compression,
                )
                return response
            except grpc.RpcError as e:
                last_error = MacrocosmosError(f"RPC error: {e.code()}: {e.details()}")
                retries += 1
            except Exception as e:
                raise MacrocosmosError(f"Error getting research job status: {e}")
            finally:
                if channel:
                    await channel.close()

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
        uids: Optional[List[int]] = None,
        model: Optional[str] = None,
        sampling_parameters: Optional[Union[SamplingParameters, Dict]] = None,
        seed: Optional[int] = None,
    ) -> apex_pb2.SubmitDeepResearcherJobResponse:
        """
        Create a new deep research job synchronously.

        Args:
            messages: A list of messages comprising the research query and context.
            uids: Optional list of specific miner UIDs to use. If not provided, the validator will select available miners.
            model: Optional model to use. If not provided, Apex will use the default model.
            sampling_parameters: Optional sampling parameters for the completion.
            seed: Optional seed for reproducibility. If not provided, a random seed will be used.

        Returns:
            A deep researcher job submit response containing the job ID, initial status created_at and updated_at info.
        """
        return run_sync_threadsafe(
            self._async_deep_research.create_job(
                messages=messages,
                uids=uids,
                model=model,
                sampling_parameters=sampling_parameters,
                seed=seed,
            )
        )

    def get_job_results(
        self,
        job_id: str,
    ) -> apex_pb2.GetDeepResearcherJobResponse:
        """
        Get the status and results of a deep research job synchronously.

        Args:
            job_id: The ID of the research job to check.

        Returns:
            A deep researcher job status response containing the current status and results.
        """
        return run_sync_threadsafe(
            self._async_deep_research.get_job_results(
                job_id=job_id,
            )
        )
