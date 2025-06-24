import os
from typing import Optional

from macrocosmos.resources.chat import (
    AsyncChat,
    AsyncCompletions,
    SyncChat,
    SyncCompletions,
)
from macrocosmos.resources.web_search import AsyncWebSearch, SyncWebSearch
from macrocosmos.resources.deep_research import SyncDeepResearch, AsyncDeepResearch
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
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            secure=secure,
            compress=compress,
            app_name=app_name,
        )

        self.chat = AsyncChat(self)
        self.completions = AsyncCompletions(self)
        self.web_search = AsyncWebSearch(self)
        self.deep_research = AsyncDeepResearch(self)


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
        compress: bool = True,
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
            compress: Whether to compress the request using gzip (default: True).
            app_name: The name of the application using the client.
        """
        if not api_key:
            api_key = os.environ.get("APEX_API_KEY")

        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            secure=secure,
            compress=compress,
            app_name=app_name,
        )

        self.chat = SyncChat(self)
        self.completions = SyncCompletions(self)
        self.web_search = SyncWebSearch(self)
        self.deep_research = SyncDeepResearch(self)
