"""Run code that does `import tinker` on Macrocosmos, unchanged.

    from macrocosmos.post_training import compat
    compat.install()        # before anything imports tinker

    import tinker            # now macrocosmos.post_training
    from tinker_cookbook import renderers   # its `import tinker` gets ours too

For libraries such as Tinker's cookbook that import `tinker` themselves. Your
own scripts can simply use `from macrocosmos import post_training as tinker`.
"""

from __future__ import annotations

import sys
import types as _modules
import warnings

from . import futures as _futures
from . import types as _types


def install(*, replace: bool = False) -> None:
    """Make `import tinker` (and `tinker.types`) resolve to `macrocosmos.post_training`.

    If the real `tinker` is already imported this refuses, unless `replace=True`,
    because objects built from the two would not mix.
    """
    from macrocosmos import post_training

    existing = sys.modules.get("tinker")
    if existing is post_training:
        return
    if existing is not None and not replace:
        raise RuntimeError(
            "the real `tinker` is already imported; call compat.install() first, or pass replace=True"
        )
    sys.modules["tinker"] = post_training
    sys.modules["tinker.types"] = _types
    sys.modules["tinker.types.tensor_data"] = (
        _types  # `from tinker.types.tensor_data import TensorData`
    )
    # The cookbook imports APIFuture from Tinker's internal module path.
    lib = _modules.ModuleType("tinker.lib")
    public = _modules.ModuleType("tinker.lib.public_interfaces")
    api_future = _modules.ModuleType("tinker.lib.public_interfaces.api_future")
    api_future.APIFuture = _futures.APIFuture  # type: ignore[attr-defined]
    public.APIFuture = _futures.APIFuture  # type: ignore[attr-defined]
    public.api_future = api_future  # type: ignore[attr-defined]
    lib.public_interfaces = public  # type: ignore[attr-defined]
    sys.modules.update(
        {
            "tinker.lib": lib,
            "tinker.lib.public_interfaces": public,
            "tinker.lib.public_interfaces.api_future": api_future,
        }
    )
    if existing is not None:
        warnings.warn(
            "replaced an already imported `tinker` with macrocosmos.post_training",
            stacklevel=2,
        )


def uninstall() -> None:
    """Undo `install()`."""
    from macrocosmos import post_training

    if sys.modules.get("tinker") is post_training:
        for name in [
            n for n in sys.modules if n == "tinker" or n.startswith("tinker.")
        ]:
            del sys.modules[name]
