import os
from typing import Optional

import tinker

from macrocosmos.types._exceptions import MacrocosmosError

from ._platform import RlPlatform
from .session import RlSession


class RlClient:
    """
    Client for RL on Macrocosmos: train with Tinker, sample on Macrocosmos GPUs.
    Plain HTTP, so it doesn't use the gRPC `BaseClient` the other clients share.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30,
        app_name: Optional[str] = None,
    ):
        """
        Initialize the RL client.

        Args:
            api_key: The API key, from an approved Macrocosmos org. Defaults to
                MACROCOSMOS_RL_API_KEY.
            base_url: The Macrocosmos API base URL. Defaults to MACROCOSMOS_RL_BASE_URL.
            timeout: Time to wait for each HTTP response in seconds. (default: 30)
            app_name: The name of the application using the client.
        """
        if not api_key:
            api_key = (os.environ.get("MACROCOSMOS_RL_API_KEY") or "").strip()
            if not api_key:
                raise MacrocosmosError(
                    "The api_key client option must be set either by passing api_key to the client "
                    "or by setting the MACROCOSMOS_RL_API_KEY environment variable"
                )

        if not base_url:
            base_url = (os.environ.get("MACROCOSMOS_RL_BASE_URL") or "").strip()
            if not base_url:
                raise MacrocosmosError(
                    "The base_url client option must be set either by passing base_url to the client "
                    "or by setting the MACROCOSMOS_RL_BASE_URL environment variable"
                )

        self.api_key = api_key.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.app_name = app_name
        self.platform = RlPlatform(
            api_key=self.api_key, base_url=self.base_url, timeout=timeout, app_name=app_name
        )

    def wrap(
        self,
        training_client: tinker.TrainingClient,
        *,
        max_gpus: int = 1,
        min_gpus: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        base_model: Optional[str] = None,
    ) -> RlSession:
        """Open an RL session around a Tinker training client.

        Args:
            training_client: The Tinker LoRA training client. Its base model and
                LoRA rank are sent with the session.
            max_gpus: The most GPU workers the session may use.
            min_gpus: GPU workers kept for the session even while idle. Left
                unset, Macrocosmos uses 1.
            max_output_tokens: The most tokens one completion may produce.
            base_model: Overrides the base model read from the training client.
        """
        return RlSession(
            training_client,
            platform=self.platform,
            min_gpus=min_gpus,
            max_gpus=max_gpus,
            max_output_tokens=max_output_tokens,
            base_model=base_model,
        )

    def close(self) -> None:
        self.platform.close()

    def __enter__(self) -> "RlClient":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def wrap(
    training_client: tinker.TrainingClient,
    *,
    max_gpus: int = 1,
    min_gpus: Optional[int] = None,
    max_output_tokens: Optional[int] = None,
    base_model: Optional[str] = None,
    client: Optional[RlClient] = None,
) -> RlSession:
    """`RlClient().wrap(...)`, with the client built from the environment if not
    given. A client made here is closed with the session."""
    options = dict(
        max_gpus=max_gpus, min_gpus=min_gpus, max_output_tokens=max_output_tokens, base_model=base_model
    )
    if client is not None:
        return client.wrap(training_client, **options)
    client = RlClient()
    try:
        return RlSession(training_client, platform=client.platform, owns_platform=True, **options)
    except BaseException:
        client.close()
        raise
