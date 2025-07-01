from typing import List

import grpc

from macrocosmos import __package_name__, __version__
from macrocosmos.generated.apex.v1 import apex_pb2, apex_pb2_grpc
from macrocosmos.types import MacrocosmosError
from macrocosmos.resources._client import BaseClient
from macrocosmos.resources._utils import run_sync_threadsafe


class AsyncWebSearch:
    """Asynchronous WebSearch resource for the Apex (subnet 1) API."""

    def __init__(self, client: BaseClient):
        """
        Initialize the asynchronous WebSearch resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client

    async def search(
        self,
        search_query: str,
        n_miners: int = 5,
        max_results_per_miner: int = 5,
        max_response_time: int = 30,
        uids: List[int] = None,
        **kwargs,
    ) -> apex_pb2.WebRetrievalResponse:
        """
        Retrieve web search results.

        Args:
            search_query: The search query to find relevant web results.
            n_miners: The number of miners to use for the query.
            max_results_per_miner: The max number of results to return per miner.
            max_response_time: The max response time in seconds to allow for miners to respond.
            uids: Optional list of specific miner UIDs to use.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A web retrieval response with search results.
        """
        if not search_query:
            raise AttributeError("search_query is a required parameter")

        request = apex_pb2.WebRetrievalRequest(
            search_query=search_query,
            n_miners=n_miners,
            n_results=max_results_per_miner,
            max_response_time=max_response_time,
            uids=uids or [],
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
            channel = None
            try:
                channel = self._client.get_async_channel()
                stub = apex_pb2_grpc.ApexServiceStub(channel)
                response = await stub.WebRetrieval(
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
                raise MacrocosmosError(f"Error retrieving web search results: {e}")
            finally:
                if channel:
                    await channel.close()

        raise last_error


class SyncWebSearch:
    """Synchronous WebSearch resource for the Apex (subnet 1) API."""

    def __init__(self, client: BaseClient):
        """
        Initialize the synchronous WebSearch resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client
        self._async_web_search = AsyncWebSearch(client)

    def search(
        self,
        search_query: str,
        n_miners: int = 5,
        max_results_per_miner: int = 5,
        max_response_time: int = 30,
        uids: List[int] = None,
        **kwargs,
    ) -> apex_pb2.WebRetrievalResponse:
        """
        Retrieve web search results synchronously.

        Args:
            search_query: The search query to find relevant web results.
            n_miners: The number of miners to use for the query.
            max_results_per_miner: The max number of results to return per miner.
            max_response_time: The max response time in seconds to allow for miners to respond.
            uids: Optional list of specific miner UIDs to use.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A web retrieval response with search results.
        """
        return run_sync_threadsafe(
            self._async_web_search.search(
                search_query=search_query,
                n_miners=n_miners,
                max_results_per_miner=max_results_per_miner,
                max_response_time=max_response_time,
                uids=uids,
                **kwargs,
            )
        )
