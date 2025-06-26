import os
from typing import Optional

from macrocosmos.resources.sn13 import AsyncSn13, SyncSn13
from macrocosmos.resources._client import BaseClient


class AsyncSn13Client(BaseClient):
    """
    Asynchronous client for the SN13 API service.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: int = 0,
        compress: bool = True,
        secure: Optional[bool] = None,
        app_name: Optional[str] = None,
    ):
        """
        Initialize the asynchronous SN13 API client.


        Args:
            api_key: The API key.
            base_url: The base URL for the API.
            timeout: Time to wait for a response in seconds. (default: None)
            max_retries: The maximum number of retries. (default: 0)
            compress: Whether to compress the request using gzip (default: True).
            secure: Whether to use HTTPS (default: True).
            app_name: The name of the application using the client.
        """
        if not api_key:
            api_key = os.environ.get("SN13_API_KEY")

        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            secure=secure,
            compress=compress,
            app_name=app_name,
        )

        self.sn13 = AsyncSn13(self)


class Sn13Client(BaseClient):
    """
    Synchronous client for the SN13 API service.
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
        Initialize the synchronous SN13 API client.

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
            api_key = os.environ.get("SN13_API_KEY")

        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            secure=secure,
            compress=compress,
            app_name=app_name,
        )

        self.sn13 = SyncSn13(self)
