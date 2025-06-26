import os
from typing import Optional

from macrocosmos.resources.billing import AsyncBilling, SyncBilling
from macrocosmos.resources._client import BaseClient


class AsyncBillingClient(BaseClient):
    """
    Asynchronous client for the Billing API.
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
        Initialize the asynchronous Billing client.

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
            api_key = os.environ.get("BILLING_API_KEY")

        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            secure=secure,
            compress=compress,
            app_name=app_name,
        )

        self.billing = AsyncBilling(self)


class BillingClient(BaseClient):
    """
    Synchronous client for the Billing API.
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
        Initialize the synchronous Billing client.

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
            api_key = os.environ.get("BILLING_API_KEY")

        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            secure=secure,
            compress=compress,
            app_name=app_name,
        )

        self.billing = SyncBilling(self)
