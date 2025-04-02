from abc import ABC
import grpc
from typing import Optional
import os
from macrocosmos.types import MacrocosmosError

DEFAULT_BASE_URL = "localhost:4000"
# DEFAULT_BASE_URL = "159.89.87.66:4000"
# DEFAULT_BASE_URL = "staging-constellation-api-t572.encr.app"
# DEFAULT_BASE_URL = "constellation.api.cloud.macrocosmos.ai"
DEFAULT_SECURE = False


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
            secure: Whether to use HTTPS (default: True).
            compress: Whether to compress the request using gzip (default: True).
            app_name: The name of the application using the client.
        """
        if not api_key:
            api_key = os.environ.get("MACROCOSMOS_API_KEY")
        if not api_key:
            raise MacrocosmosError(
                "The api_key client option must be set either by passing api_key to the client or by setting the APEX_API_KEY or MACROCOSMOS_API_KEY environment variable"
            )

        if not base_url:
            base_url = DEFAULT_BASE_URL

        if not secure:
            secure = DEFAULT_SECURE

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.secure = secure
        self.compress = compress
        self.app_name = app_name

    def get_channel(self) -> grpc.aio.Channel:
        """
        Get a channel for the given client.
        """
        if self.secure:
            return grpc.aio.secure_channel(
                self.base_url, grpc.ssl_channel_credentials()
            )
        return grpc.aio.insecure_channel(self.base_url)
