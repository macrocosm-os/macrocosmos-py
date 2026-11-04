import os
from typing import Optional, Sequence

import tinker

from macrocosmos.resources._client import BaseClient
from macrocosmos.types._exceptions import MacrocosmosError

from .platform_client import RlPlatformClient
from .session import RlSession


class RlClient(BaseClient):
    """
    Client for RL on Macrocosmos: train with Tinker, sample on Macrocosmos GPUs.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = 30,
        app_name: Optional[str] = None,
    ):
        """
        Initialize the RL client.

        Args:
            api_key: The API key, from an approved Macrocosmos org. Defaults to
                RL_API_KEY, then MACROCOSMOS_API_KEY.
            base_url: The Macrocosmos API base URL. Defaults to MACROCOSMOS_RL_BASE_URL.
            timeout: Time to wait for each HTTP response in seconds. (default: 30)
            app_name: The name of the application using the client.
        """
        if not api_key:
            api_key = os.environ.get("RL_API_KEY")

        # The RL endpoints are HTTP, not the gRPC host the other clients default to.
        if not base_url:
            base_url = (os.environ.get("MACROCOSMOS_RL_BASE_URL") or "").strip()
            if not base_url:
                raise MacrocosmosError(
                    "The base_url client option must be set either by passing base_url to the client "
                    "or by setting the MACROCOSMOS_RL_BASE_URL environment variable"
                )

        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout, app_name=app_name)

        self.platform = RlPlatformClient(
            api_key=self.api_key, base_url=self.base_url, timeout=timeout or 30, app_name=app_name
        )

    def wrap(
        self,
        training_client: tinker.TrainingClient,
        *,
        min_gpus: int = 1,
        max_gpus: int = 1,
        gpu_type: Optional[Sequence[str]] = None,
        max_context_tokens: Optional[int] = None,
        base_model: Optional[str] = None,
    ) -> RlSession:
        """Open an RL session around a Tinker training client.

        Args:
            training_client: The Tinker LoRA training client. Its base model and
                LoRA rank are sent with the session.
            min_gpus / max_gpus: The GPU workers the session wants serving it.
            gpu_type: Preferred GPU types. Not sent yet.
            max_context_tokens: The longest prompt + completion a sequence may reach.
            base_model: Overrides the base model read from the training client.
        """
        return RlSession(
            training_client,
            platform=self.platform,
            min_gpus=min_gpus,
            max_gpus=max_gpus,
            gpu_type=gpu_type,
            max_context_tokens=max_context_tokens,
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
    min_gpus: int = 1,
    max_gpus: int = 1,
    gpu_type: Optional[Sequence[str]] = None,
    max_context_tokens: Optional[int] = None,
    base_model: Optional[str] = None,
    client: Optional[RlClient] = None,
) -> RlSession:
    """`RlClient().wrap(...)`, with the client built from the environment if not
    given. A client made here is closed with the session."""
    owned = client is None
    client = client or RlClient()
    return RlSession(
        training_client,
        platform=client.platform,
        min_gpus=min_gpus,
        max_gpus=max_gpus,
        gpu_type=gpu_type,
        max_context_tokens=max_context_tokens,
        base_model=base_model,
        owns_platform=owned,
    )
