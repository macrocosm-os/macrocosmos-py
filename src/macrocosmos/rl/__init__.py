"""RL on Macrocosmos: train with Tinker, sample on Macrocosmos GPUs.

    from macrocosmos.rl import RlClient

    client = RlClient(app_name="my-rl-script")                     # IOTA_API_KEY / LC_API_KEY
    with client.wrap(training_client) as session:
        result = session.generator.sample(prompt, num_samples=8)   # served by Macrocosmos
        ...                                                        # score, then train
        session.trainer.forward_backward(...)                      # passes through to Tinker
        session.trainer.optim_step(...)
        session.weights_sync()                                     # new adapter goes to the fleet

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
from .session import RlSession

__all__ = ["RlClient", "RlSession", "wrap"]
