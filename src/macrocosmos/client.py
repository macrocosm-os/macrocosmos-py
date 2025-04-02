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
from macrocosmos.types import MacrocosmosError

# DEFAULT_BASE_URL = "159.89.87.66:4000"
DEFAULT_BASE_URL = "staging-constellation-api-t572.encr.app"
# DEFAULT_BASE_URL = "constellation.api.cloud.macrocosmos.ai"


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
            api_key = os.environ.get(
                "APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY")
            )
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
        self.web_search = AsyncWebSearch(self)


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
            api_key = os.environ.get(
                "APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY")
            )
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
        self.web_search = SyncWebSearch(self)


class AsyncGravityClient:
    """
    Asynchronous client for the Gravity (subnet 13) API on Bittensor.

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
            api_key = os.environ.get(
                "GRAVITY_API_KEY", os.environ.get("MACROCOSMOS_API_KEY")
            )
        if api_key is None:
            raise MacrocosmosError(
                "The api_key client option must be set either by passing api_key to the client or by setting the GRAVITY_API_KEY or MACROCOSMOS_API_KEY environment variable"
            )
        self.api_key = api_key

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.compress = compress

        # Initialize resources
        self.gravity = AsyncGravity(self)


class GravityClient:
    """
    Synchronous client for the Gravity (subnet 13) API on Bittensor.

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
            api_key = os.environ.get(
                "GRAVITY_API_KEY", os.environ.get("MACROCOSMOS_API_KEY")
            )
        if api_key is None:
            raise MacrocosmosError(
                "The api_key client option must be set either by passing api_key to the client or by setting the GRAVITY_API_KEY or MACROCOSMOS_API_KEY environment variable"
            )
        self.api_key = api_key

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.compress = compress

        # Initialize resources with synchronous versions
        self.gravity = SyncGravity(self)
