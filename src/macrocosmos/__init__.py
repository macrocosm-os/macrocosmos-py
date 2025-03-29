"""Official Python SDK for Macrocosmos"""

__package_name__ = "macrocosmos-py-sdk"

try:
    from importlib.metadata import version, PackageNotFoundError

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
from .client import AsyncApexClient

__all__ = [
    "AsyncApexClient",
    "__package_name__",
]
