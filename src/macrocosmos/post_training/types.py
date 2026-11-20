"""Tinker's types, with Tinker's names and fields, and no numpy or torch needed.

`ModelInput`, `Datum`, `TensorData` and friends behave like `tinker.types`. The
clients also accept Tinker's own objects (and numpy arrays or torch tensors),
so code built for Tinker, the cookbook included, can pass what it already has.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Dict, List, Literal, Mapping, Optional, Sequence, Union

LossFnType = Literal[
    "cross_entropy",
    "importance_sampling",
    "ppo",
    "cispo",
    "dro",
    "gspo",
    "stable_reinforce",
]
StopReason = Literal["stop", "length"]
SamplingClientKind = Literal["snapshot", "inflight"]
TensorDtype = Literal["int64", "float32"]


# --- inputs -------------------------------------------------------------------


@dataclass(frozen=True)
class EncodedTextChunk:
    tokens: List[int]
    type: Literal["encoded_text"] = "encoded_text"

    @property
    def length(self) -> int:
        return len(self.tokens)


ModelInputChunk = EncodedTextChunk  # text only for now


@dataclass(frozen=True)
class ModelInput:
    """A prompt: a list of token chunks."""

    chunks: List[ModelInputChunk] = field(default_factory=list)

    @classmethod
    def from_ints(cls, tokens: Sequence[int]) -> "ModelInput":
        return cls([EncodedTextChunk(list(tokens))])

    @classmethod
    def empty(cls) -> "ModelInput":
        return cls([])

    def to_ints(self) -> List[int]:
        return [t for chunk in self.chunks for t in chunk.tokens]

    def append(self, chunk: ModelInputChunk) -> "ModelInput":
        return ModelInput([*self.chunks, chunk])

    def append_int(self, token: int) -> "ModelInput":
        return self.append(EncodedTextChunk([token]))

    @property
    def length(self) -> int:
        return sum(chunk.length for chunk in self.chunks)


@dataclass(frozen=True)
class TensorData:
    """A flat list of numbers, with Tinker's `from_numpy` / `from_torch` / `tolist`."""

    data: List[Union[int, float]]
    dtype: TensorDtype = "float32"
    shape: Optional[List[int]] = None

    @classmethod
    def from_numpy(cls, array: Any) -> "TensorData":
        return cls(
            array.reshape(-1).tolist(), _dtype_of(str(array.dtype)), list(array.shape)
        )

    @classmethod
    def from_torch(cls, tensor: Any) -> "TensorData":
        t = tensor.detach().cpu()
        return cls(t.reshape(-1).tolist(), _dtype_of(str(t.dtype)), list(t.shape))

    def tolist(self) -> List[Union[int, float]]:
        return list(self.data)

    def to_numpy(self) -> Any:
        import numpy as np

        array = np.asarray(self.data, dtype=self.dtype)
        return array.reshape(self.shape) if self.shape else array

    def to_torch(self) -> Any:
        import torch

        return torch.as_tensor(self.to_numpy())


LossFnInputs = Dict[str, TensorData]


@dataclass(frozen=True)
class PromptProvenanceSpan:
    """Positions that came from the prompt of sampled sequence `sequence_id`."""

    sequence_id: str
    length: int
    offset: int = 0


@dataclass(frozen=True)
class SampledProvenanceSpan:
    """Positions that were sampled as part of sequence `sequence_id`."""

    sequence_id: str
    length: int
    offset: int = 0


ProvenanceSpan = Union[PromptProvenanceSpan, SampledProvenanceSpan]


@dataclass(frozen=True)
class Datum:
    """One training example: the input tokens and the loss function's inputs."""

    model_input: ModelInput
    loss_fn_inputs: Mapping[str, Any]
    model_input_spans: Optional[List[ProvenanceSpan]] = None
    loss_fn_input_spans: Optional[List[ProvenanceSpan]] = None

    def with_provenance(
        self,
        *,
        model_input: Optional[List[ProvenanceSpan]] = None,
        loss_fn_inputs: Optional[List[ProvenanceSpan]] = None,
    ) -> "Datum":
        """Record which sampled sequence each position came from (for `stable_reinforce`).

        Kept on the datum; the gateway doesn't take provenance yet.
        """
        return replace(
            self, model_input_spans=model_input, loss_fn_input_spans=loss_fn_inputs
        )


# --- options ------------------------------------------------------------------


@dataclass(frozen=True)
class AdamParams:
    learning_rate: float = 1e-4
    beta1: float = 0.9
    beta2: float = 0.95
    eps: float = 1e-12
    weight_decay: float = 0.0
    grad_clip_norm: float = 0.0


@dataclass(frozen=True)
class SamplingParams:
    max_tokens: Optional[int] = None
    seed: Optional[int] = None
    stop: Union[str, Sequence[str], Sequence[int], None] = None
    temperature: float = 1.0
    top_k: int = -1
    top_p: float = 1.0


# --- results ------------------------------------------------------------------


@dataclass(frozen=True)
class SampledSequence:
    stop_reason: StopReason
    tokens: List[int]
    logprobs: Optional[List[float]] = None
    sequence_id: Optional[str] = None


@dataclass(frozen=True)
class SampleResponse:
    sequences: List[SampledSequence]
    policy_version: Optional[int] = None
    """The adapter version that produced the samples; -1 is the base model."""


@dataclass(frozen=True)
class ForwardBackwardOutput:
    loss_fn_output_type: str
    loss_fn_outputs: List[Dict[str, TensorData]]
    metrics: Dict[str, float]


@dataclass(frozen=True)
class OptimStepResponse:
    metrics: Optional[Dict[str, float]] = None
    step: Optional[int] = None


@dataclass(frozen=True)
class SaveWeightsForSamplerResponse:
    path: str
    """An `mc://` path to the saved adapter."""
    version: Optional[int] = None


@dataclass(frozen=True)
class SaveWeightsResponse:
    path: str


@dataclass(frozen=True)
class SaveWeightsExternalResponse:
    path: str
    """An `mc://` path; download its files with `download()`."""


@dataclass(frozen=True)
class ExternalWeightsUrlsResponse:
    urls: Dict[str, str]
    """Each file of the adapter and a signed URL to download it."""
    expires_at: Optional[float] = None
    """When the URLs stop working (Unix seconds)."""


@dataclass(frozen=True)
class ModelData:
    model_name: str
    tokenizer_id: Optional[str] = None
    arch: Optional[str] = None


@dataclass(frozen=True)
class GetInfoResponse:
    model_id: str
    model_data: ModelData
    is_lora: bool = True
    lora_rank: Optional[int] = None
    model_name: Optional[str] = None


# --- conversion to the wire format ------------------------------------------------


def _dtype_of(name: str) -> TensorDtype:
    return "int64" if "int" in name else "float32"


def to_ints(model_input: Any) -> List[int]:
    """Tokens of a `ModelInput` (ours or Tinker's), or of a plain list of ints."""
    if hasattr(model_input, "to_ints"):
        return [int(t) for t in model_input.to_ints()]
    if hasattr(model_input, "tolist"):  # numpy array, torch tensor
        return [int(t) for t in to_list(model_input)]
    return [int(t) for t in model_input]


def to_list(value: Any) -> List[Union[int, float]]:
    """A loss input as a flat list: ours or Tinker's `TensorData`, numpy, torch, or a list."""
    if hasattr(
        value, "tolist"
    ):  # TensorData (ours or Tinker's), numpy array, torch tensor
        out = value.tolist()
    elif hasattr(value, "data"):
        out = list(value.data)
    else:
        out = list(value)
    while out and isinstance(out[0], list):  # flatten nested lists
        out = [x for row in out for x in row]
    # float32 values round-trip through Python as e.g. 0.30000001192092896. Seven
    # significant digits is all float32 holds, and the shorter JSON lets about
    # twice as many tokens fit in each request.
    return [x if isinstance(x, int) else float(f"{x:.7g}") for x in out]


def datum_to_wire(datum: Any) -> Dict[str, Any]:
    """The gateway's compact datum: `{"tokens": [...], "inputs": {name: [...]}}`."""
    if isinstance(datum, Mapping):  # already a dict, either form
        if "tokens" in datum:
            return {
                "tokens": to_ints(datum["tokens"]),
                "inputs": {
                    k: to_list(v) for k, v in datum["inputs"].items() if k != "mask"
                },
            }
        model_input, inputs = datum["model_input"], datum["loss_fn_inputs"]
    else:
        model_input, inputs = datum.model_input, datum.loss_fn_inputs
    try:
        tokens = to_ints(model_input)
    except ValueError as e:
        raise ValueError(
            "macrocosmos.post_training supports text inputs only (EncodedTextChunk); images and audio are not supported yet"
        ) from e
    return {
        "tokens": tokens,
        "inputs": {
            name: to_list(value) for name, value in inputs.items() if name != "mask"
        },
    }
