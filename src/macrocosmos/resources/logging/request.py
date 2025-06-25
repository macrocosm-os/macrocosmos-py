import grpc

from macrocosmos import __package_name__, __version__
from macrocosmos.generated.logger.v1 import logger_pb2, logger_pb2_grpc
from macrocosmos.resources._client import BaseClient
from macrocosmos.types import MacrocosmosError


def make_sync_request(client: BaseClient, method_name: str, request) -> logger_pb2.Ack:
    """
    Make a request to the Logger service.

    Args:
        client: The client instance for making requests.
        method_name: The name of the method to call.
        request: The request message.

    Returns:
        The response from the service.
    """
    metadata = [
        ("x-source", client.app_name),
        ("x-client-id", __package_name__),
        ("x-client-version", __version__),
    ]

    retries = 0
    last_error = None
    while retries <= client.max_retries:
        channel = None
        try:
            channel = client.get_sync_channel()
            stub = logger_pb2_grpc.LoggerServiceStub(channel)
            method = getattr(stub, method_name)
            response = method(
                request,
                metadata=metadata,
                timeout=client.timeout,
                compression=grpc.Compression.Gzip,
            )
            return response
        except grpc.RpcError as e:
            last_error = MacrocosmosError(f"RPC error: {e.code()}: {e.details()}")
            retries += 1
        except Exception as e:
            raise MacrocosmosError(f"Error calling {method_name}: {e}")
        finally:
            if channel:
                channel.close()

    raise last_error


async def make_async_request(
    client: BaseClient, method_name: str, request
) -> logger_pb2.Ack:
    """
    Make an async request to the Logger service.

    Args:
        client: The client instance for making requests.
        method_name: The name of the method to call.
        request: The request message.

    Returns:
        The response from the service.
    """
    metadata = [
        ("x-source", client.app_name),
        ("x-client-id", __package_name__),
        ("x-client-version", __version__),
    ]

    retries = 0
    last_error = None
    while retries <= client.max_retries:
        channel = None
        try:
            channel = client.get_async_channel()
            stub = logger_pb2_grpc.LoggerServiceStub(channel)
            method = getattr(stub, method_name)
            response = await method(
                request,
                metadata=metadata,
                timeout=client.timeout,
                compression=grpc.Compression.Gzip,
            )
            return response
        except grpc.RpcError as e:
            last_error = MacrocosmosError(f"RPC error: {e.code()}: {e.details()}")
            retries += 1
        except Exception as e:
            raise MacrocosmosError(f"Error calling {method_name}: {e}")
        finally:
            if channel:
                await channel.close()

    raise last_error
