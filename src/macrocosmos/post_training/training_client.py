from __future__ import annotations

import dataclasses
import threading
import time
import warnings
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Mapping, NoReturn, Optional, Sequence

from ._http import MAX_BODY_BYTES, Gateway, encode
from .errors import NotSupportedError, PayloadTooLargeError, RequestFailedError
from .futures import APIFuture, run_in, wait_for_job
from .sampling_client import SamplingClient
from .tokenizer import Tokenizer, load_tokenizer
from .types import (
    AdamParams,
    ForwardBackwardOutput,
    GetInfoResponse,
    LossFnType,
    OptimStepResponse,
    SaveWeightsForSamplerResponse,
    SaveWeightsExternalResponse,
    SaveWeightsResponse,
    TensorData,
    datum_to_wire,
)

#: How long `.result()` waits for a training op when no timeout is given.
DEFAULT_TRAIN_TIMEOUT_S = 1800.0
_MAX_REPLAYS = 3


class TrainingClient:
    """Trains a LoRA adapter on Macrocosmos trainer GPUs. Tinker's `TrainingClient`.

    Made by `PostTrainingClient.create_lora_training_client()`. Every method returns
    an `APIFuture`. Calls are sent in the order they're made, so you can queue
    `forward_backward` and `optim_step` before waiting on either.
    """

    def __init__(
        self, gateway: Gateway, session_id: str, info: GetInfoResponse, *, step: int = 0
    ) -> None:
        self._gw = gateway
        self.session_id = session_id
        self._info = info
        self._lock = threading.Lock()
        self._seq = 0  # 0 was the create job; ops count from 1 and never reuse a number
        self._step = step  # the optimizer step the next optim_step applies at
        self._unstepped: List[
            Dict[str, Any]
        ] = []  # forward_backward bodies since the last step
        self._last_step: Optional[APIFuture[OptimStepResponse]] = None
        self._submitter = ThreadPoolExecutor(
            max_workers=1, thread_name_prefix="macrocosmos-post-training-submit"
        )
        self._warned_state = False

    @property
    def model_id(self) -> str:
        return self._info.model_id

    # --- training -------------------------------------------------------------------

    def forward_backward(
        self,
        data: Sequence[Any],
        loss_fn: LossFnType,
        loss_fn_config: Optional[Mapping[str, Any]] = None,
    ) -> APIFuture[ForwardBackwardOutput]:
        """Compute the loss on `data` and accumulate gradients.

        `data` holds `Datum`s, ours or Tinker's. A batch too big for one request
        is split across several; the output is the same as for a single call.

        If this raises partway through a split batch, part of it may already be
        with the trainer. Don't send it again: the next `optim_step` reconciles
        with the trainer and resends the step's data if needed.
        """
        if not data:
            raise ValueError("forward_backward needs at least one Datum")
        batches = _split([datum_to_wire(d) for d in data])
        config = dict(loss_fn_config) if loss_fn_config else None
        with self._lock:
            handles = []
            for batch in batches:
                body = {"data": batch, "loss_fn": loss_fn, "loss_fn_config": config}
                # Recorded before sending: if the send fails after reaching the
                # trainer, the step's count still matches; if it never reached it,
                # optim_step's replay sends it.
                self._unstepped.append(body)
                handles.append(self._submit("forward_backward", body))

        def resolve(timeout: Optional[float]) -> ForwardBackwardOutput:
            deadline = _deadline(timeout)
            results = [self._wait(h, _remaining(deadline)) for h in handles]
            return _merge(results, sizes=[len(b) for b in batches], loss_fn=loss_fn)

        return APIFuture(resolve, label=f"forward_backward({len(data)} datums)")

    def optim_step(
        self,
        optim_params: Optional[AdamParams] = None,
        *,
        adam_params: Optional[AdamParams] = None,
    ) -> APIFuture[OptimStepResponse]:
        """Apply the accumulated gradients with Adam.

        Steps apply in order: each one waits for the step before it. If the
        trainer lost a step's gradients, they're sent again; when later steps'
        `forward_backward` calls were already queued, those reach the trainer
        first, so for reliable recovery wait for each `optim_step` before
        queuing the next step's data.
        """
        params = _asdict(adam_params or optim_params or AdamParams())
        with self._lock:
            at_step, step_data = self._step, list(self._unstepped)
            handle = self._submit_step(params, at_step, step_data)
            # Only now has the trainer got the step, so only now move on.
            self._step, self._unstepped = at_step + 1, []
            previous = self._last_step

        # Kept across calls, so waiting again after a timeout picks up where it stopped.
        replays = 0
        resent: Optional[List[str]] = None

        def resolve(timeout: Optional[float]) -> OptimStepResponse:
            nonlocal handle, replays, resent, previous
            deadline = _deadline(timeout)
            if previous is not None:
                try:  # steps apply in order; an earlier step's error belongs to its own caller
                    previous.result(_remaining(deadline))
                except Exception:  # noqa: BLE001
                    pass
                if (
                    previous.done()
                ):  # settled: don't keep the chain of earlier steps alive
                    previous = None
            while True:
                if resent is not None:
                    for h in resent:
                        self._wait(h, _remaining(deadline))
                    with self._lock:
                        handle = self._submit_step(params, at_step, step_data)
                    resent = None
                result = self._wait(handle, _remaining(deadline))
                if not result.get("replay"):
                    return OptimStepResponse(
                        metrics=result.get("metrics") or {}, step=result.get("step")
                    )
                # The trainer restarted and lost this step's gradients: send them again.
                replays += 1
                if replays > _MAX_REPLAYS:
                    raise RequestFailedError(
                        f"optim_step at step {at_step}: the trainer asked for the step's data {replays} times",
                        handle=handle,
                    )
                with self._lock:
                    resent = [
                        self._submit("forward_backward", body) for body in step_data
                    ]

        future: APIFuture[OptimStepResponse] = APIFuture(
            resolve, label=f"optim_step(step {at_step})"
        )
        self._last_step = future
        return future

    # --- weights --------------------------------------------------------------------

    def save_weights_for_sampler(
        self, name: Optional[str] = None, **_: Any
    ) -> APIFuture[SaveWeightsForSamplerResponse]:
        """Save the adapter so it can be sampled from. Resolves to its `mc://` path."""
        with self._lock:
            handle = self._submit("save_weights_for_sampler", {"name": name})

        def resolve(timeout: Optional[float]) -> SaveWeightsForSamplerResponse:
            result = self._wait(handle, timeout)
            return SaveWeightsForSamplerResponse(
                path=result["path"], version=result.get("version")
            )

        return APIFuture(resolve, label=f"save_weights_for_sampler({name or ''})")

    def save_weights_and_get_sampling_client(
        self, name: Optional[str] = None, **_: Any
    ) -> APIFuture[SamplingClient]:
        """Save the adapter and return a sampler for this session.

        For now a sampler answers with whatever adapter the session currently
        serves, not necessarily the one just saved: the gateway can't yet be told
        which saved adapter to sample. Each `SampleResponse.policy_version` says
        which adapter answered, and a sampler warns once when it differs from the
        one it was made for.
        """
        return self.save_weights_for_sampler(name).then(
            lambda saved: self.create_sampling_client(
                saved.path, version=saved.version
            ),
            label="save_weights_and_get_sampling_client",
        )

    def create_sampling_client(
        self,
        model_path: Optional[str] = None,
        *,
        version: Optional[int] = None,
        **_: Any,
    ) -> SamplingClient:
        return SamplingClient(
            self._gw,
            self.session_id,
            base_model=self._info.model_data.model_name,
            model_path=model_path,
            version=version,
            tokenizer_id=self._info.model_data.tokenizer_id,
        )

    def save_weights_external(
        self, name: str, ttl_seconds: Optional[float] = None, **_: Any
    ) -> APIFuture[SaveWeightsExternalResponse]:
        """Save the adapter to download it. Every saved adapter is already a
        standard PEFT adapter, so this is `save_weights_for_sampler` under
        Tinker's name; download it with `post_training.download(path, dir)`."""
        return self.save_weights_for_sampler(name).then(
            lambda saved: SaveWeightsExternalResponse(path=saved.path),
            label=f"save_weights_external({name})",
        )

    async def save_weights_external_async(
        self, name: str, **kw: Any
    ) -> APIFuture[SaveWeightsExternalResponse]:
        return await run_in(self._submitter, self.save_weights_external, name, **kw)

    def save_state(self, name: str, **_: Any) -> APIFuture[SaveWeightsResponse]:
        """Save the adapter's weights. The optimizer's state isn't saved yet, so a
        run can't be resumed from this; it's here so checkpointing code runs."""
        if not self._warned_state:
            self._warned_state = True
            warnings.warn(
                "save_state saves the adapter weights only; resuming from a checkpoint is not supported yet",
                stacklevel=2,
            )
        return self.save_weights_for_sampler(f"state-{name}").then(
            lambda saved: SaveWeightsResponse(path=saved.path),
            label=f"save_state({name})",
        )

    # --- async variants, shaped like Tinker's: await once to submit, again for the result
    # Submits go through one worker thread, so they reach the gateway in call order.

    async def forward_backward_async(
        self,
        data: Sequence[Any],
        loss_fn: LossFnType,
        loss_fn_config: Optional[Mapping[str, Any]] = None,
    ) -> APIFuture[ForwardBackwardOutput]:
        return await run_in(
            self._submitter, self.forward_backward, data, loss_fn, loss_fn_config
        )

    async def optim_step_async(
        self,
        optim_params: Optional[AdamParams] = None,
        *,
        adam_params: Optional[AdamParams] = None,
    ) -> APIFuture[OptimStepResponse]:
        return await run_in(
            self._submitter, self.optim_step, optim_params, adam_params=adam_params
        )

    async def save_weights_for_sampler_async(
        self, name: Optional[str] = None, **kw: Any
    ) -> APIFuture[SaveWeightsForSamplerResponse]:
        return await run_in(self._submitter, self.save_weights_for_sampler, name, **kw)

    async def save_state_async(
        self, name: str, **kw: Any
    ) -> APIFuture[SaveWeightsResponse]:
        return await run_in(self._submitter, self.save_state, name, **kw)

    async def save_weights_and_get_sampling_client_async(
        self, name: Optional[str] = None, **kw: Any
    ) -> SamplingClient:
        future = await run_in(
            self._submitter, self.save_weights_and_get_sampling_client, name, **kw
        )
        return await future

    # --- info -----------------------------------------------------------------------

    def get_info(self) -> GetInfoResponse:
        return self._info

    def get_tokenizer(self) -> Tokenizer:
        """The base model's tokenizer, loaded locally from the Hugging Face Hub."""
        return load_tokenizer(
            self._info.model_data.tokenizer_id or self._info.model_data.model_name
        )

    # --- not on Macrocosmos yet -----------------------------------------------------

    def forward(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError(
            "forward (loss without gradients) is not supported yet; use forward_backward"
        )

    def forward_backward_custom(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError(
            "custom loss functions are not supported yet; pick a built-in loss_fn"
        )

    def load_state(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError("loading a checkpoint is not supported yet")

    load_state_with_optimizer = load_state

    def __repr__(self) -> str:
        return f"TrainingClient(model_id={self.model_id!r}, step={self._step})"

    # --- plumbing -------------------------------------------------------------------

    def _submit(self, op: str, body: Dict[str, Any]) -> str:
        """Queue one op. Call with the lock held, so `seq_id`s go out in order."""
        self._seq += 1
        reply = self._gw.request(
            "POST",
            f"/models/{self.model_id}/{op}",
            {"seq_id": self._seq, **body},
        )
        return reply["handle"]

    def _submit_step(
        self, params: Dict[str, float], at_step: int, step_data: List[Any]
    ) -> str:
        return self._submit(
            "optim_step",
            {"adam_params": params, "at_step": at_step, "pending": len(step_data)},
        )

    def _wait(self, handle: str, timeout: Optional[float]) -> Dict[str, Any]:
        return wait_for_job(
            self._gw, handle, DEFAULT_TRAIN_TIMEOUT_S if timeout is None else timeout
        )


def _deadline(timeout: Optional[float]) -> Optional[float]:
    return None if timeout is None else time.monotonic() + timeout


def _remaining(deadline: Optional[float]) -> Optional[float]:
    return None if deadline is None else max(deadline - time.monotonic(), 0.0)


def _asdict(params: Any) -> Dict[str, float]:
    if dataclasses.is_dataclass(params):
        return dataclasses.asdict(params)
    return params.model_dump(exclude_none=True)  # Tinker's pydantic AdamParams


def _split(data: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    """Pack datums into as few requests as fit under the body limit, keeping their order."""
    budget = MAX_BODY_BYTES - 512  # room for seq_id, loss_fn and its config
    batches: List[List[Dict[str, Any]]] = [[]]
    size = 0
    for datum in data:
        n = len(encode(datum)) + 1
        if n > budget:
            raise PayloadTooLargeError(
                f"one datum of {len(datum['tokens'])} tokens is {n} bytes, over the 16 KB request limit",
                status_code=413,
            )
        if size + n > budget and batches[-1]:
            batches.append([])
            size = 0
        batches[-1].append(datum)
        size += n
    return batches


def _merge(
    results: List[Dict[str, Any]], *, sizes: List[int], loss_fn: str
) -> ForwardBackwardOutput:
    """One `ForwardBackwardOutput` from the results of a split batch."""
    metrics: Dict[str, float] = {}
    total = sum(sizes)
    for result, n in zip(results, sizes):
        for key, value in (result.get("metrics") or {}).items():
            if key.endswith(":mean"):  # weight each request's mean by its datums
                metrics[key] = metrics.get(key, 0.0) + value * n / total
            elif key.endswith(":max"):
                metrics[key] = max(metrics.get(key, value), value)
            elif key.endswith(":min"):
                metrics[key] = min(metrics.get(key, value), value)
            else:  # ":sum" and counts add up
                metrics[key] = metrics.get(key, 0.0) + value
    outputs: List[Dict[str, TensorData]] = []
    for result, n in zip(results, sizes):
        rows = result.get("logprobs") or [None] * n
        outputs += [
            {"logprobs": TensorData(row, "float32")} if row is not None else {}
            for row in rows
        ]
    return ForwardBackwardOutput(
        loss_fn_output_type=loss_fn, loss_fn_outputs=outputs, metrics=metrics
    )
