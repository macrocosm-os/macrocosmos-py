import os
import asyncio
from typing import Optional

from macrocosmos.types import MacrocosmosError
from macrocosmos.resources._chat import AsyncChat, AsyncCompletions, SyncChat, SyncCompletions

DEFAULT_BASE_URL = "159.89.87.66:4000"  # "constellation.api.macrocosmos.ai"


class AsyncApexClient:
    """
    Asynchronous client for the Apex (subnet 1) API on Bittensor.

    Args:
        api_key: The API key.
        base_url: The base URL for the API.
        timeout: Time to wait for a response in seconds. (default: None)
        max_retries: The maximum number of retries. (default: 0)
        compress: Whether to compress the request using gzip (default: True).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Optional[int] = None,
        max_retries: int = 0,
        compress: bool = True,
    ):
        if api_key is None:
            api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))
        if api_key is None:
            raise MacrocosmosError(
                "The api_key client option must be set either by passing api_key to the client or by setting the APEX_API_KEY or MACROCOSMOS_API_KEY environment variable"
            )
        self.api_key = api_key

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.compress = compress

        # Initialize resources
        self.chat = AsyncChat(self)
        self.completions = AsyncCompletions(self)


class ApexClient:
    """
    Synchronous client for the Apex (subnet 1) API on Bittensor.

    Args:
        api_key: The API key.
        base_url: The base URL for the API.
        timeout: Time to wait for a response in seconds. (default: None)
        max_retries: The maximum number of retries. (default: 0)
        compress: Whether to compress the request using gzip (default: True).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Optional[int] = None,
        max_retries: int = 0,
        compress: bool = True,
    ):
        if api_key is None:
            api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))
        if api_key is None:
            raise MacrocosmosError(
                "The api_key client option must be set either by passing api_key to the client or by setting the APEX_API_KEY or MACROCOSMOS_API_KEY environment variable"
            )
        self.api_key = api_key

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.compress = compress

        # Initialize resources with synchronous versions
        self.chat = SyncChat(self)
        self.completions = SyncCompletions(self)
