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

# Import client and types
from .client import ApexClient, AsyncApexClient, AsyncGravityClient, GravityClient
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
    "ChatMessage",
    "ChatCompletionResponse",
    "ChatCompletionChunkResponse",
    "SamplingParameters",
    "WebRetrievalResponse",
]
