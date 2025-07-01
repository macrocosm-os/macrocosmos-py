import grpc

from macrocosmos import __package_name__, __version__
from macrocosmos.generated.billing.v1 import billing_pb2, billing_pb2_grpc
from macrocosmos.types import MacrocosmosError
from macrocosmos.resources._client import BaseClient
from macrocosmos.resources._utils import run_sync_threadsafe


class AsyncBilling:
    """Asynchronous Billing resource for the Billing API."""

    def __init__(self, client: BaseClient):
        """
        Initialize the asynchronous Billing resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client

    async def GetUsage(
        self,
        product_type: str = "",
    ) -> billing_pb2.GetUsageResponse:
        """
        Get the usage and billing information for a product.

        Args:
            product_type: The type of the product (e.g. "gravity").

        Returns:
            A response containing the usage and billing information.
        """
        request = billing_pb2.GetUsageRequest(
            product_type=product_type,
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
                stub = billing_pb2_grpc.BillingServiceStub(channel)
                response = await stub.GetUsage(
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
                raise MacrocosmosError(f"Error getting usage: {e}")
            finally:
                if channel:
                    await channel.close()

        raise last_error


class SyncBilling:
    """Synchronous Billing resource for the Billing API."""

    def __init__(self, client: BaseClient):
        """
        Initialize the synchronous Billing resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client
        self._async_billing = AsyncBilling(client)

    def GetUsage(
        self,
        product_type: str = "",
    ) -> billing_pb2.GetUsageResponse:
        """
        Get the usage and billing information for a product synchronously.

        Args:
            product_type: The type of the product (e.g. "gravity").

        Returns:
            A response containing the usage and billing information.
        """
        return run_sync_threadsafe(
            self._async_billing.GetUsage(
                product_type=product_type,
            )
        )
