from abc import ABC
import grpc
from typing import Optional
import os
from macrocosmos.types import MacrocosmosError

DEFAULT_BASE_URL = "constellation.api.cloud.macrocosmos.ai"
DEFAULT_USE_HTTPS = True


class BaseClient(ABC):
    """
    Abstract base class for client.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: int = 0,
        secure: Optional[bool] = None,
        compress: bool = True,
        app_name: Optional[str] = None,
    ):
        """
        Initialize the abstract base class for the client.

        Args:
            api_key: The API key.
            base_url: The base URL for the API.
            timeout: Time to wait for a response in seconds. (default: None)
            max_retries: The maximum number of retries. (default: 0)
            secure: Whether to use HTTPS. Set this if you're using a custom base URL.
            compress: Whether to compress the request using gzip (default: True).
            app_name: The name of the application using the client.
        """
        if not api_key:
            api_key = os.environ.get("MACROCOSMOS_API_KEY")
            api_key = api_key.strip() if api_key else ""
            if not api_key:
                raise MacrocosmosError(
                    "The api_key client option must be set either by passing api_key to the client or by setting the MACROCOSMOS_API_KEY environment variable"
                )

        if not base_url:
            base_url = os.environ.get("MACROCOSMOS_BASE_URL")
            base_url = base_url.strip() if base_url else ""
            if not base_url:
                base_url = DEFAULT_BASE_URL

        if not isinstance(secure, bool):
            secure_str = os.environ.get("MACROCOSMOS_USE_HTTPS", "")
            secure_str = secure_str.strip().lower() if secure_str else ""
            if secure_str == "":
                secure = DEFAULT_USE_HTTPS
            else:
                secure = secure_str in ["true", "1", "yes", "y", "on"]

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.secure = secure
        self.compress = compress
        self.app_name = app_name

    def get_async_channel(self) -> grpc.aio.Channel:
        """
        Get an asynchronous channel for the given client.
        """
        if self.secure:
            return grpc.aio.secure_channel(
                self.base_url, grpc.ssl_channel_credentials()
            )
        return grpc.aio.insecure_channel(self.base_url)

    def get_sync_channel(self) -> grpc.Channel:
        """
        Get a synchronous channel for the given client.
        """
        if self.secure:
            return grpc.secure_channel(self.base_url, grpc.ssl_channel_credentials())
        return grpc.insecure_channel(self.base_url)
