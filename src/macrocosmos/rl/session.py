"""An RL session: train with Tinker, sample on Macrocosmos GPUs.

The calls are Tinker's own. `session.trainer` is the Tinker training client
itself. `session.save_weights_and_get_sampling_client()` exports its current
LoRA, as Tinker's method of the same name does, and returns a sampler whose
`sample(...)` runs on Macrocosmos: it sends the prompt to
`POST /platform/rl/inference`, which queues it in the rollout fleet's work
pool, then polls `GET /platform/rl/inference/{handle}` until the workers have
posted the result. The result comes back as Tinker's `SampleResponse`.

Creating a session opens it on Macrocosmos (`POST /platform/rl/sessions`),
which records the base model and the GPU workers wanted and returns the
session's id; leaving the `with` block closes it. Macrocosmos routes the
session's tasks to the workers hosting it.
"""

from __future__ import annotations

import asyncio
import dataclasses
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Sequence

import tinker
from tinker import types
from tinker.lib.public_interfaces.api_future import AwaitableConcurrentFuture

from macrocosmos.types._exceptions import MacrocosmosError

from ._platform import POLL_INTERVAL_S, WAIT_TIMEOUT_S, RlPlatform

# How long an exported adapter's download links stay valid.
ADAPTER_TTL_SECONDS = 24 * 3600
# Samples waited on at once (each waits on its own request).
_SAMPLE_THREADS = 64
_executor = ThreadPoolExecutor(max_workers=_SAMPLE_THREADS, thread_name_prefix="mc-rl-sample")


@dataclasses.dataclass(frozen=True)
class RlSampleResponse(types.SampleResponse):
    """Tinker's `SampleResponse`, plus `policy_version`: the adapter version the
    worker actually sampled with. Workers never go back to an older version,
    so a sampler used after a newer export can get a newer one than it asked
    for; -1 means the base model."""

    policy_version: int | None = None


class RlSamplingClient:
    """Tinker's `SamplingClient`, served by Macrocosmos. Samples with one fixed
    adapter (or the base model when it has none)."""

    def __init__(self, session: RlSession, adapter: dict[str, Any] | None) -> None:
        self._session = session
        self.adapter = adapter

    def sample(
        self,
        prompt: types.ModelInput | str | Sequence[int],
        num_samples: int = 1,
        sampling_params: types.SamplingParams | None = None,
        *,
        timeout: float = WAIT_TIMEOUT_S,
        poll_interval: float = POLL_INTERVAL_S,
        logprobs: bool = True,
    ) -> AwaitableConcurrentFuture:
        """Sample `num_samples` completions of one prompt. Returns a future of
        Tinker's `SampleResponse`, as Tinker's `sample` does: `.result()` waits.

        The response's `policy_version` is the adapter version the worker
        used. Each token's logprob comes back unless `logprobs=False`; the workers
        leave them out unless asked, and RL losses need them. `timeout` is how
        long to wait for the result; `poll_interval` how often to check."""
        tokens = self._tokens(prompt)
        return AwaitableConcurrentFuture(
            _executor.submit(
                self._sample, tokens, num_samples, sampling_params, timeout, poll_interval, logprobs
            )
        )

    async def sample_async(self, prompt, num_samples: int = 1, sampling_params=None, **kw):
        return await asyncio.wrap_future(self.sample(prompt, num_samples, sampling_params, **kw)._future)

    def _sample(
        self,
        tokens: list[int],
        num_samples: int,
        sampling_params: types.SamplingParams | None,
        timeout: float,
        poll_interval: float,
        logprobs: bool,
    ) -> RlSampleResponse:
        platform = self._session._platform
        params = sampling_params.model_dump(exclude_none=True) if sampling_params else {}
        if isinstance(params.get("stop"), str):
            params["stop"] = [params["stop"]]
        prompt_entry = {"prompt_tokens": tokens, "n": num_samples, "logprobs": logprobs, **params}

        # Into the work pool through Macrocosmos, then poll it for the result.
        handle = platform.submit(
            session_id=self._session.session_id, prompts=[prompt_entry], adapter=self.adapter
        )
        [result] = platform.wait(handle, timeout=timeout, interval=poll_interval)
        if result["state"] != "done":
            raise MacrocosmosError(f"sampling failed: {result.get('error')}")
        return RlSampleResponse(
            policy_version=result.get("policy_version"),
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


def _rest_client_for(training_client: tinker.TrainingClient) -> tinker.RestClient:
    """A Tinker REST client on the training client's own connection, so it uses
    the same API key and base URL however they were given (TINKER_API_KEY or
    `api_key=`). Falls back to a client configured from the environment."""
    holder = getattr(training_client, "holder", None)
    if holder is not None:
        try:
            return tinker.RestClient(_holder=holder)
        except TypeError:  # a Tinker release without the `_holder` argument
            pass
    return tinker.RestClient()


class RlSession:
    """Use as a context manager: `with client.wrap(training_client) as session:`.

    Opened on Macrocosmos when created; closed by `close()` or on leaving the
    `with` block, which releases its GPU workers."""

    def __init__(
        self,
        training_client: tinker.TrainingClient,
        *,
        platform: RlPlatform,
        max_gpus: int = 1,
        min_gpus: int | None = None,
        gpu_type: Sequence[str] | None = None,
        max_output_tokens: int | None = None,
        base_model: str | None = None,
        owns_platform: bool = False,
    ) -> None:
        self.trainer = training_client
        self._adapter_version = -1
        self._version_lock = threading.Lock()
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

    def save_weights_and_get_sampling_client(self, name: str | None = None) -> RlSamplingClient:
        """Export the trainer's current LoRA from Tinker and return a sampler
        that samples with it on Macrocosmos. Tinker's method of the same name,
        with the sampling moved to Macrocosmos."""
        # Each export gets its own, higher version, even when called from
        # several threads at once.
        with self._version_lock:
            self._adapter_version += 1
            version = self._adapter_version
            if self._rest is None:
                self._rest = _rest_client_for(self.trainer)
        name = name or f"mc-rl-{version:06d}"
        saved = self.trainer.save_weights_external(name, ttl_seconds=ADAPTER_TTL_SECONDS).result()
        urls = self._rest.get_external_weights_urls(saved.path).result().urls
        return RlSamplingClient(self, {"urls": dict(urls), "version": version})

    async def save_weights_and_get_sampling_client_async(self, name: str | None = None) -> RlSamplingClient:
        return await asyncio.to_thread(self.save_weights_and_get_sampling_client, name)

    def create_sampling_client(self) -> RlSamplingClient:
        """A sampler for the base model, with no adapter."""
        return RlSamplingClient(self, None)

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
