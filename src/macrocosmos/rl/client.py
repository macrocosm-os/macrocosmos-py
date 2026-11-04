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
                IOTA_API_KEY, then LC_API_KEY. Not MACROCOSMOS_API_KEY: that is
                the other services' key (Gravity, SN13).
            base_url: The Macrocosmos API base URL. Defaults to MACROCOSMOS_RL_BASE_URL.
            timeout: Time to wait for each HTTP response in seconds. (default: 30)
            app_name: The name of the application using the client.
        """
        if not api_key:
            api_key = (os.environ.get("IOTA_API_KEY") or os.environ.get("LC_API_KEY") or "").strip()
            if not api_key:
                # Checked here so BaseClient never falls back to MACROCOSMOS_API_KEY.
                raise MacrocosmosError(
                    "The api_key client option must be set either by passing api_key to the client "
                    "or by setting the IOTA_API_KEY (or LC_API_KEY) environment variable"
                )

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
        max_gpus: int = 1,
        min_gpus: Optional[int] = None,
        gpu_type: Optional[Sequence[str]] = None,
        max_output_tokens: Optional[int] = None,
        base_model: Optional[str] = None,
    ) -> RlSession:
        """Open an RL session around a Tinker training client.

        Args:
            training_client: The Tinker LoRA training client. Its base model and
                LoRA rank are sent with the session.
            max_gpus: The most GPU workers the session may use.
            min_gpus: GPU workers kept for the session even while idle. Only
                staff or an org Admin may set it; left unset, Macrocosmos uses 1.
            gpu_type: Preferred GPU types. Not sent yet.
            max_output_tokens: The most tokens one completion may produce.
            base_model: Overrides the base model read from the training client.
        """
        return RlSession(
            training_client,
            platform=self.platform,
            min_gpus=min_gpus,
            max_gpus=max_gpus,
            gpu_type=gpu_type,
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
    gpu_type: Optional[Sequence[str]] = None,
    max_output_tokens: Optional[int] = None,
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
        max_output_tokens=max_output_tokens,
        base_model=base_model,
        owns_platform=owned,
    )
