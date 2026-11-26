from __future__ import annotations

import dataclasses
import uuid
import warnings
from typing import Any, Dict, NoReturn, Optional

from ._http import Gateway, encode
from .errors import (
    APITimeoutError,
    NotSupportedError,
    PayloadTooLargeError,
    RequestFailedError,
)
from .futures import _WAITERS, APIFuture, poll, run_in
from .tokenizer import Tokenizer, load_tokenizer
from .types import SampledSequence, SampleResponse, SamplingParams, to_ints

#: How long `.result()` waits for samples when no timeout is given. The first
#: request in a session also waits for a GPU worker to start.
DEFAULT_SAMPLE_TIMEOUT_S = 900.0


class SamplingClient:
    """Samples from a session's model on Macrocosmos GPUs. Tinker's `SamplingClient`.

    Made by `TrainingClient.save_weights_and_get_sampling_client()` or
    `PostTrainingClient.create_sampling_client()`.

    It samples with the adapter the session currently serves; see
    `save_weights_and_get_sampling_client` for what that means after a save.
    """

    def __init__(
        self,
        gateway: Gateway,
        session_id: str,
        *,
        base_model: str,
        model_path: Optional[str] = None,
        version: Optional[int] = None,
        tokenizer_id: Optional[str] = None,
    ) -> None:
        self._gw = gateway
        self.session_id = session_id
        self.base_model = base_model
        self.model_path = model_path
        self.version = version
        """Which save this sampler samples (`adapters/rollout-{version}`), or None for
        the session's newest; `SampleResponse.policy_version` says which answered."""
        self._tokenizer_id = tokenizer_id or base_model
        self._warned_version = False

    def sample(
        self,
        prompt: Any,
        num_samples: int = 1,
        sampling_params: Optional[SamplingParams] = None,
        **tinker_options: Any,
    ) -> APIFuture[SampleResponse]:
        """Sample `num_samples` completions of `prompt`, a `ModelInput` or token ids.

        Each sequence comes back with its tokens' logprobs, which RL losses need.
        """
        unsupported = [
            k for k, v in tinker_options.items() if v and k != "record_stability_info"
        ]
        if unsupported:
            raise NotSupportedError(
                f"sample() doesn't support {', '.join(sorted(unsupported))} yet"
            )
        entry: Dict[str, Any] = {
            "prompt_tokens": to_ints(prompt),
            "n": num_samples,
            "logprobs": True,
            **_sampling_options(sampling_params),
        }
        body: Dict[str, Any] = {"session_id": self.session_id, "prompts": [entry]}
        # A sampler made from a save asks for that save; otherwise the session's
        # newest save answers.
        # `SampleResponse.policy_version` says which one it was.
        if self.version is not None:
            body["adapter_version"] = self.version
        if len(encode(body)) > self._gw.max_request_bytes:
            raise PayloadTooLargeError(
                f"a prompt of {len(entry['prompt_tokens'])} tokens is over the "
                f"{self._gw.max_request_bytes:,}-byte request limit",
                status_code=413,
            )
        handle = self._gw.request("POST", "/sampling", body, idempotent=False)["handle"]
        return APIFuture(
            lambda timeout: self._collect(handle, timeout),
            label=f"sample({num_samples})",
        )

    async def sample_async(
        self,
        prompt: Any,
        num_samples: int = 1,
        sampling_params: Optional[SamplingParams] = None,
        **kw: Any,
    ) -> SampleResponse:
        # Submitting is a blocking HTTP call: keep it off the event loop.
        future = await run_in(
            _WAITERS, self.sample, prompt, num_samples, sampling_params, **kw
        )
        return await future

    def compute_logprobs(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError("compute_logprobs is not supported yet")

    def get_tokenizer(self) -> Tokenizer:
        """The base model's tokenizer, loaded locally from the Hugging Face Hub."""
        return load_tokenizer(self._tokenizer_id)

    def get_base_model(self) -> str:
        return self.base_model

    def __repr__(self) -> str:
        return f"SamplingClient(session={self.session_id!r}, model_path={self.model_path!r})"

    def _collect(self, handle: str, timeout: Optional[float]) -> SampleResponse:
        try:
            reply = poll(
                lambda: self._gw.request("GET", f"/sampling/{handle}"),
                lambda r: r.get("results") is not None,
                timeout=DEFAULT_SAMPLE_TIMEOUT_S if timeout is None else timeout,
                what=f"sampling {handle}",
            )
        except APITimeoutError as e:
            raise APITimeoutError(
                f"{e}. No GPU worker has answered session {self.session_id} yet; the first "
                "request in a session waits for one to start. Wait longer with .result(timeout=...)."
            ) from None
        [result] = reply["results"]
        if result.get("state") != "done":
            raise RequestFailedError(
                f"sampling failed: {result.get('error')}", handle=handle
            )
        policy_version = result.get("policy_version")
        if (
            self.version is not None
            and policy_version is not None
            and policy_version != self.version
            and not self._warned_version
        ):
            self._warned_version = True
            warnings.warn(
                f"asked for adapter version {self.version}, got samples from version {policy_version}",
                stacklevel=4,
            )
        return SampleResponse(
            sequences=[
                SampledSequence(
                    stop_reason=seq["stop_reason"],
                    tokens=seq["tokens"],
                    logprobs=seq.get("logprobs"),
                    sequence_id=uuid.uuid4().hex,
                )
                for seq in result["sequences"]
            ],
            policy_version=policy_version,
        )


def _sampling_options(params: Any) -> Dict[str, Any]:
    """`SamplingParams` (ours, or Tinker's pydantic one) as the worker's options."""
    if params is None:
        return {}
    if dataclasses.is_dataclass(params):
        options = {k: v for k, v in dataclasses.asdict(params).items() if v is not None}
    else:
        options = params.model_dump(exclude_none=True)
    stop = options.pop("stop", None)
    if isinstance(stop, str):
        options["stop"] = [stop]
    elif stop and all(isinstance(s, int) for s in stop):
        options["stop_token_ids"] = list(stop)  # Tinker's renderers stop on token ids
    elif stop:
        options["stop"] = list(stop)
    return options
