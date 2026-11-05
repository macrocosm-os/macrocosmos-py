"""RL on Macrocosmos: train with Tinker, sample on Macrocosmos GPUs.

    from macrocosmos.rl import RlClient

    with RlClient(app_name="my-rl-script") as client, client.wrap(training_client) as session:
        # The key comes from MACROCOSMOS_RL_API_KEY
        sampler = session.save_weights_and_get_sampling_client()   # current LoRA -> Macrocosmos
        result = sampler.sample(prompt, num_samples=8).result()    # served by Macrocosmos
        ...                                                        # score, then train
        session.trainer.forward_backward(...).result()             # Tinker
        session.trainer.optim_step(...).result()

Needs `tinker` and `httpx`, which the core SDK doesn't install:
`pip install tinker httpx` (Python 3.11+).
"""

try:
    import httpx  # noqa: F401
    import tinker  # noqa: F401
except ImportError as e:  # pragma: no cover - depends on the environment
    raise ImportError(
        "macrocosmos.rl needs tinker and httpx: pip install tinker httpx (Python 3.11+)"
    ) from e

from .client import RlClient, wrap
from .session import RlSampleResponse, RlSamplingClient, RlSession

__all__ = ["RlClient", "RlSampleResponse", "RlSamplingClient", "RlSession", "wrap"]
