import os
from typing import Optional

from macrocosmos.resources.chat import (
    AsyncChat,
    AsyncCompletions,
    SyncChat,
    SyncCompletions,
)
from macrocosmos.resources.gravity import AsyncGravity, SyncGravity
from macrocosmos.resources.web_search import AsyncWebSearch, SyncWebSearch
from macrocosmos.resources._client import BaseClient


class AsyncApexClient(BaseClient):
    """
    Asynchronous client for the Apex (subnet 1) API on Bittensor.
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
        Initialize the asynchronous Apex client.

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
            api_key = os.environ.get("APEX_API_KEY")

        super().__init__(
            api_key, base_url, timeout, max_retries, secure, compress, app_name
        )

        # Initialize resources
        self.chat = AsyncChat(self)
        self.completions = AsyncCompletions(self)
        self.web_search = AsyncWebSearch(self)


class ApexClient(BaseClient):
    """
    Synchronous client for the Apex (subnet 1) API on Bittensor.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: int = 0,
        secure: Optional[bool] = None,
        app_name: Optional[str] = None,
    ):
        """
        Initialize the synchronous Apexclient.

        Args:
            api_key: The API key.
            base_url: The base URL for the API.
            timeout: Time to wait for a response in seconds. (default: None)
            max_retries: The maximum number of retries. (default: 0)
            secure: Whether to use HTTPS (default: True).
            app_name: The name of the application using the client.
        """
        if not api_key:
            api_key = os.environ.get("APEX_API_KEY")

        super().__init__(api_key, base_url, timeout, max_retries, secure, app_name)

        # Initialize resources with synchronous versions
        self.chat = SyncChat(self)
        self.completions = SyncCompletions(self)
        self.web_search = SyncWebSearch(self)


class AsyncGravityClient(BaseClient):
    """
    Asynchronous client for the Gravity (subnet 13) API on Bittensor.
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
        Initialize the asynchronous Gravity client.


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
            api_key = os.environ.get("GRAVITY_API_KEY")

        super().__init__(
            api_key, base_url, timeout, max_retries, secure, compress, app_name
        )

        # Initialize resources
        self.gravity = AsyncGravity(self)


class GravityClient:
    """
    Synchronous client for the Gravity (subnet 13) API on Bittensor.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: int = 0,
        secure: Optional[bool] = None,
        app_name: Optional[str] = None,
    ):
        """
        Initialize the synchronous Gravity client.

        Args:
            api_key: The API key.
            base_url: The base URL for the API.
            timeout: Time to wait for a response in seconds. (default: None)
            max_retries: The maximum number of retries. (default: 0)
            secure: Whether to use HTTPS (default: True).
            app_name: The name of the application using the client.
        """
        if not api_key:
            api_key = os.environ.get("GRAVITY_API_KEY")

        super().__init__(api_key, base_url, timeout, max_retries, secure, app_name)

        # Initialize resources with synchronous versions
        self.gravity = SyncGravity(self)
