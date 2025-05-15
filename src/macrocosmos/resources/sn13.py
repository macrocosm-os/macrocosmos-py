import asyncio
from typing import Dict, List, Optional

import grpc
from google.protobuf.json_format import MessageToDict
from macrocosmos import __package_name__, __version__
from macrocosmos.generated.sn13.v1 import sn13_validator_pb2, sn13_validator_pb2_grpc, sn13_validator_p2p
from macrocosmos.resources._client import BaseClient
from macrocosmos.types import MacrocosmosError


class AsyncSn13:
    """Asynchronous SN13 resource for the Data Universe (subnet 13) API on Bittensor."""

    def __init__(self, client: BaseClient):
        """
        Initialize the asynchronous SN13 resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client

    async def OnDemandData(
        self,
        source: str,
        usernames: List[str],
        keywords: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 5,
    ) -> sn13_validator_pb2.OnDemandDataResponse:
        """
        Retrieves on-demand data from the SN13 API service asynchronously, based on the provided parameters.

        Args:
            source (str): The data source (X or Reddit)
            usernames (List[str]): List of usernames to fetch data from
            keywords (List[str]): List of keywords to search for
            start_date (str): Date from which we want to start fetching data. ISO 8601 formatted date string (e.g. "2024-01-01T00:00:00Z")
            end_date (str): Date up to which we want to fetch data. ISO 8601 formatted date string (e.g. "2024-01-01T00:00:00Z")
            limit (int): Maximum number of results to return

        Returns:
            dict: 
                - status (str): The request status
                - data (List[dict]): The data object returned by the miners
                - meta (dict): Additional metadata about the request
        """
        request = sn13_validator_pb2.OnDemandDataRequest(
            source=source,
            usernames=usernames,
            keywords=keywords,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
        )

        return await self._make_request("OnDemandData", request)


    async def _make_request(self, method_name, request):
        """
        Make a request to the SN13 service.

        Args:
            method_name: The name of the method to call.
            request: The request message.

        Returns:
            The response from the service.
        """
        metadata = [
            ("x-source", self._client.app_name),
            ("x-client-id", __package_name__),
            ("x-client-version", __version__),
            ("authorization", f"Bearer {self._client.api_key}"),
            (
                "remote-user-email",
                "example@example.com",
            ),  # TODO: Remove this once authentication is fully implemented
        ]

        compression = grpc.Compression.Gzip if self._client.compress else None

        retries = 0
        last_error = None
        while retries <= self._client.max_retries:
            try:
                channel = self._client.get_channel()
                stub = sn13_validator_pb2_grpc.Sn13ServiceStub(channel)
                method = getattr(stub, method_name)
                response = await method(
                    request,
                    metadata=metadata,
                    timeout=self._client.timeout,
                    compression=compression,
                )
                await channel.close()
                # Unpack the response into a dictionary
                return MessageToDict(response, preserving_proto_field_name=True)
            except grpc.RpcError as e:
                last_error = MacrocosmosError(f"RPC error: {e.code()}: {e.details()}")
                retries += 1
                await channel.close()
            except Exception as e:
                await channel.close()
                raise MacrocosmosError(f"Error calling {method_name}: {e}")

        raise last_error


class SyncSn13:
    """Synchronous SN13 resource for the Data Universe (subnet 13) API on Bittensor."""

    def __init__(self, client: BaseClient):
        """
        Initialize the synchronous SN13 resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client
        self._async_sn13 = AsyncSn13(client)

    def OnDemandData(
        self,
        source: str,
        usernames: List[str],
        keywords: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 5,
    ) -> sn13_validator_pb2.OnDemandDataResponse:
        """
        Retrieves on-demand data from the SN13 API service synchronously, based on the provided parameters.

        Args:
            source (str): The data source (X or Reddit)
            usernames (List[str]): List of usernames to fetch data from
            keywords (List[str]): List of keywords to search for
            start_date (str): Date from which we want to start fetching data. ISO 8601 formatted date string (e.g. "2024-01-01T00:00:00Z")
            end_date (str): Date up to which we want to fetch data. ISO 8601 formatted date string (e.g. "2024-01-01T00:00:00Z")
            limit (int): Maximum number of results to return

        Returns:
            dict: 
                - status (str): The request status
                - data (List[dict]): The data object returned by the miners
                - meta (dict): Additional metadata about the request
        """
        return asyncio.run(
            self._async_sn13.OnDemandData(
                source=source,
                usernames=usernames,
                keywords=keywords,
                start_date=start_date,
                end_date=end_date,
                limit=limit,
            )
        )

