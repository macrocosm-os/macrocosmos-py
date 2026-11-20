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


def __getattr__(name: str):
    # Post-training needs its extra (`pip install "macrocosmos[post-training]"`), so
    # it loads on first use: `import macrocosmos` keeps working without it.
    if name in ("PostTrainingClient", "post_training"):
        import importlib

        module = importlib.import_module(".post_training", __name__)
        return module if name == "post_training" else module.PostTrainingClient
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
