"""Official Python SDK for Macrocosmos"""

__package_name__ = "macrocosmos-py-sdk"

try:
    from importlib.metadata import PackageNotFoundError, version

    try:
        __version__ = version("macrocosmos")
    except PackageNotFoundError:
        __version__ = "unknown"
except ImportError:
    try:
        import pkg_resources

        __version__ = pkg_resources.get_distribution("macrocosmos").version
    except Exception:
        __version__ = "unknown"

# Import clients from separate files
from .apex_client import ApexClient, AsyncApexClient
from .gravity_client import AsyncGravityClient, GravityClient
from .billing_client import BillingClient, AsyncBillingClient
from .sn13_client import Sn13Client, AsyncSn13Client
from .logger_client import LoggerClient, AsyncLoggerClient

from .types import (
    ChatCompletionChunkResponse,
    ChatCompletionResponse,
    ChatMessage,
    SamplingParameters,
    WebRetrievalResponse,
)

__all__ = [
    "__package_name__",
    "AsyncApexClient",
    "ApexClient",
    "AsyncGravityClient",
    "GravityClient",
    "BillingClient",
    "AsyncBillingClient",
    "ChatMessage",
    "ChatCompletionResponse",
    "ChatCompletionChunkResponse",
    "SamplingParameters",
    "WebRetrievalResponse",
    "Sn13Client",
    "AsyncSn13Client",
    "LoggerClient",
    "AsyncLoggerClient",
]
