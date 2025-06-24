from typing import Optional

from macrocosmos.resources.logger import AsyncLogger, Logger
from macrocosmos.resources._client import BaseClient


class AsyncLoggerClient(BaseClient):
    """
    Asynchronous client for the Logger API.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: int = 0,
        compress: bool = True,
        secure: Optional[bool] = None,
        app_name: Optional[str] = None,
    ):
        """
        Initialize the asynchronous Logger client.

        Args:
            base_url: The base URL for the API.
            timeout: Time to wait for a response in seconds. (default: None)
            max_retries: The maximum number of retries. (default: 0)
            compress: Whether to compress the request using gzip (default: True).
            secure: Whether to use HTTPS (default: True).
            app_name: The name of the application using the client.
        """

        super().__init__(
            api_key="NOT_NEEDED",
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            secure=secure,
            compress=compress,
            app_name=app_name,
        )

        self.logger = AsyncLogger(self)


class LoggerClient(BaseClient):
    """
    Synchronous client for the Logger API.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: int = 0,
        secure: Optional[bool] = None,
        app_name: Optional[str] = None,
    ):
        """
        Initialize the synchronous Logger client.

        Args:
            api_key: The API key.
            base_url: The base URL for the API.
            timeout: Time to wait for a response in seconds. (default: None)
            max_retries: The maximum number of retries. (default: 0)
            secure: Whether to use HTTPS (default: True).
            app_name: The name of the application using the client.
        """

        super().__init__(
            api_key="NOT_NEEDED",
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            secure=secure,
            app_name=app_name,
        )

        self.logger = Logger(self)
