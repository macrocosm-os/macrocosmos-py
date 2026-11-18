"""Reinforcement learning on Macrocosmos, with Tinker's API.

    from macrocosmos import rl
    from macrocosmos.rl import types

    with rl.ServiceClient() as service_client:           # key: MACROCOSMOS_RL_API_KEY
        training_client = service_client.create_lora_training_client(
            base_model="Qwen/Qwen3-8B", rank=32
        ).result()
        sampler = training_client.save_weights_and_get_sampling_client().result()
        result = sampler.sample(prompt, num_samples=8, sampling_params=params).result()
        ...                                              # score the samples
        training_client.forward_backward(data, loss_fn="importance_sampling")
        training_client.optim_step(types.AdamParams(learning_rate=1e-5)).result()

Porting a Tinker script: change `import tinker` to
`from macrocosmos import rl as tinker` and put the training loop inside
`with tinker.ServiceClient() as service_client:`. For libraries that import
`tinker` themselves, such as Tinker's cookbook, call `rl.compat.install()` first.

Install with `pip install "macrocosmos[rl]"`.
"""

import sys

if sys.version_info < (3, 9):  # pragma: no cover
    raise ImportError("macrocosmos.rl needs Python 3.9 or newer")

try:
    import httpx  # noqa: F401
except ImportError as e:  # pragma: no cover
    raise ImportError(
        'macrocosmos.rl needs its extra: pip install "macrocosmos[rl]"'
    ) from e

from . import compat, types
from .errors import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    NotSupportedError,
    PayloadTooLargeError,
    PermissionDeniedError,
    RateLimitError,
    RequestFailedError,
    RLError,
    UnprocessableEntityError,
)
from .futures import APIFuture
from .sampling_client import SamplingClient
from .service_client import ServiceClient
from .training_client import TrainingClient
from .types import (
    AdamParams,
    Datum,
    EncodedTextChunk,
    ForwardBackwardOutput,
    LossFnType,
    ModelInput,
    ModelInputChunk,
    OptimStepResponse,
    PromptProvenanceSpan,
    SampledProvenanceSpan,
    SampledSequence,
    SampleResponse,
    SamplingClientKind,
    SamplingParams,
    StopReason,
    TensorData,
)

TinkerError = RLError  # so `except tinker.TinkerError` keeps working

__all__ = [
    "ServiceClient",
    "TrainingClient",
    "SamplingClient",
    "APIFuture",
    "compat",
    "types",
    "AdamParams",
    "Datum",
    "EncodedTextChunk",
    "ForwardBackwardOutput",
    "LossFnType",
    "ModelInput",
    "ModelInputChunk",
    "OptimStepResponse",
    "PromptProvenanceSpan",
    "SampledProvenanceSpan",
    "SampledSequence",
    "SampleResponse",
    "SamplingClientKind",
    "SamplingParams",
    "StopReason",
    "TensorData",
    "RLError",
    "TinkerError",
    "APIConnectionError",
    "APIStatusError",
    "APITimeoutError",
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "InternalServerError",
    "NotFoundError",
    "NotSupportedError",
    "PayloadTooLargeError",
    "PermissionDeniedError",
    "RateLimitError",
    "RequestFailedError",
    "UnprocessableEntityError",
]
