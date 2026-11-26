"""Post-training on Macrocosmos (LoRA fine-tuning with RL), with Tinker's API.

    import macrocosmos as mc
    from macrocosmos.post_training import types

    with mc.PostTrainingClient() as client:       # MACROCOSMOS_POST_TRAINING_API_KEY
        training_client = client.create_lora_training_client(
            base_model="Qwen/Qwen3-8B", rank=32
        ).result()
        sampler = training_client.save_weights_and_get_sampling_client().result()
        result = sampler.sample(prompt, num_samples=8, sampling_params=params).result()
        ...                                       # score the samples
        training_client.forward_backward(data, loss_fn="importance_sampling")
        training_client.optim_step(types.AdamParams(learning_rate=1e-5)).result()

Porting a Tinker script: change `import tinker` to
`from macrocosmos import post_training as tinker` and put the training loop
inside `with tinker.ServiceClient() as service_client:` (`ServiceClient` is
`PostTrainingClient` under Tinker's name). For libraries that import `tinker`
themselves, such as Tinker's cookbook, call `post_training.compat.install()` first.

Install with `pip install "macrocosmos[post-training]"`.
"""

import sys

if sys.version_info < (3, 9):  # pragma: no cover
    raise ImportError("macrocosmos.post_training needs Python 3.9 or newer")

try:
    import httpx  # noqa: F401
except ImportError as e:  # pragma: no cover
    raise ImportError(
        'macrocosmos.post_training needs its extra: pip install "macrocosmos[post-training]"'
    ) from e

from . import compat, types
from .download import download
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
    PostTrainingError,
    UnprocessableEntityError,
)
from .futures import APIFuture
from .rest_client import RestClient
from .sampling_client import SamplingClient
from .service_client import PostTrainingClient, ServiceClient
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

TinkerError = PostTrainingError  # so `except tinker.TinkerError` keeps working

__all__ = [
    "PostTrainingClient",
    "ServiceClient",
    "TrainingClient",
    "RestClient",
    "download",
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
    "PostTrainingError",
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
