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
from .gravity_client import AsyncGravityClient, GravityClient
from .billing_client import BillingClient, AsyncBillingClient
from .sn13_client import Sn13Client, AsyncSn13Client
from .logger_client import LoggerClient, AsyncLoggerClient

__all__ = [
    "__package_name__",
    "GravityClient",
    "AsyncGravityClient",
    "BillingClient",
    "AsyncBillingClient",
    "Sn13Client",
    "AsyncSn13Client",
    "LoggerClient",
    "AsyncLoggerClient",
]
