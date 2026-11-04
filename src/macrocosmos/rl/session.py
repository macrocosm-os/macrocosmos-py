"""An RL session: a Tinker training client whose sampling runs on Macrocosmos GPUs.

`session.trainer` is the Tinker training client itself: train with it as
usual. `session.generator.sample(...)` sends a prompt to Macrocosmos and waits
for the completions. `session.weights_sync()` exports the current LoRA from
Tinker so the next samples use it.

Creating a session opens it on Macrocosmos (`POST /platform/rl/sessions`),
which records the base model and the GPU workers wanted and returns the
session's id; leaving the `with` block closes it. Macrocosmos routes the
session's tasks to the workers hosting it.
"""

from __future__ import annotations

import uuid
from typing import Any, Sequence

import tinker
from tinker import types

from macrocosmos.types._exceptions import MacrocosmosError

from .platform_client import POLL_INTERVAL_S, WAIT_TIMEOUT_S, RlPlatformClient

# How long an exported adapter's download links stay valid.
ADAPTER_TTL_SECONDS = 24 * 3600


class Generator:
    """Sampling, served by Macrocosmos."""

    def __init__(self, session: RlSession) -> None:
        self._session = session

    def sample(
        self,
        prompt: types.ModelInput | str | Sequence[int],
        num_samples: int = 1,
        sampling_params: types.SamplingParams | None = None,
        *,
        timeout: float = WAIT_TIMEOUT_S,
        poll_interval: float = POLL_INTERVAL_S,
        logprobs: bool = True,
    ) -> types.SampleResponse:
        """Sample `num_samples` completions of one prompt, as Tinker's `SampleResponse`.
        Each token's logprob comes back unless `logprobs=False`; the workers
        leave them out unless asked, and RL losses need them. `timeout` is how
        long to wait for the result; `poll_interval` how often to check."""
        session = self._session
        params = sampling_params.model_dump(exclude_none=True) if sampling_params else {}
        if isinstance(params.get("stop"), str):
            params["stop"] = [params["stop"]]
        prompt_entry = {
            "prompt_tokens": self._tokens(prompt), "n": num_samples, "logprobs": logprobs, **params,
        }

        handle = session._platform.submit(
            session_id=session.session_id, prompts=[prompt_entry], adapter=session.adapter
        )
        [result] = session._platform.wait(handle, timeout=timeout, interval=poll_interval)
        if result["state"] != "done":
            raise MacrocosmosError(f"sampling failed: {result.get('error')}")
        return types.SampleResponse(
            sequences=[
                types.SampledSequence(
                    stop_reason=seq["stop_reason"],
                    sequence_id=uuid.uuid4().hex,
                    _tokens_list=seq["tokens"],
                    _logprobs_list=seq.get("logprobs"),
                )
                for seq in result["sequences"]
            ]
        )

    def _tokens(self, prompt: types.ModelInput | str | Sequence[int]) -> list[int]:
        if isinstance(prompt, types.ModelInput):
            return prompt.to_ints()
        if isinstance(prompt, str):
            return self._session.trainer.get_tokenizer().encode(prompt)
        return list(prompt)


class RlSession:
    """Use as a context manager: `with client.wrap(training_client) as session:`.

    Opened on Macrocosmos when created; closed by `close()` or on leaving the
    `with` block, which releases its GPU workers."""

    def __init__(
        self,
        training_client: tinker.TrainingClient,
        *,
        platform: RlPlatformClient,
        max_gpus: int = 1,
        min_gpus: int | None = None,
        gpu_type: Sequence[str] | None = None,
        max_output_tokens: int | None = None,
        base_model: str | None = None,
        owns_platform: bool = False,
    ) -> None:
        self.trainer = training_client
        self.generator = Generator(self)
        # The adapter samples are drawn from; None means the base model.
        self.adapter: dict[str, Any] | None = None
        self._adapter_version = -1
        self._rest: tinker.RestClient | None = None
        self._platform = platform
        self._owns_platform = owns_platform
        self._closed = False

        info = training_client.get_info()
        # One rollout worker serves one replica of the base model. min_workers
        # is sent only when asked for: setting it needs staff or an org Admin.
        requirements: dict[str, Any] = {"max_workers": max_gpus}
        if min_gpus is not None:
            requirements["min_workers"] = min_gpus
        if info.lora_rank:
            requirements["max_lora_rank"] = info.lora_rank
        if max_output_tokens:
            requirements["max_output_tokens"] = max_output_tokens
        # Macrocosmos has no field for GPU types yet; kept here until it does.
        self.gpu_type = list(gpu_type) if gpu_type else None

        opened = platform.open_session(
            base_model=base_model or info.model_data.model_name, requirements=requirements,
        )
        self.session_id: str = opened["session_id"]
        self.base_model: str = opened["base_model"]

    def weights_sync(self, name: str | None = None) -> dict[str, Any]:
        """Export the trainer's current LoRA from Tinker; later samples are
        drawn from it."""
        self._adapter_version += 1
        name = name or f"mc-rl-{self._adapter_version:06d}"
        saved = self.trainer.save_weights_external(name, ttl_seconds=ADAPTER_TTL_SECONDS).result()
        if self._rest is None:
            self._rest = tinker.RestClient()
        urls = self._rest.get_external_weights_urls(saved.path).result().urls
        self.adapter = {"urls": dict(urls), "version": self._adapter_version}
        return self.adapter

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self._platform.close_session(self.session_id)
        finally:
            if self._owns_platform:
                self._platform.close()

    def __enter__(self) -> RlSession:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
