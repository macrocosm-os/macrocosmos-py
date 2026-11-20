"""Download a saved adapter's files, as Tinker's cookbook does with `weights.download`."""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

from .errors import PostTrainingError

# A file name the gateway may hand back: one path segment, nothing that climbs out.
_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def download(path: str, output_dir: str, *, client: Optional[Any] = None) -> str:
    """Download the adapter saved at `path` (an `mc://` path) into `output_dir`.

    Writes its PEFT files (`adapter_config.json`, `adapter_model.safetensors`),
    each checked against the sha256 the gateway reports before anything is
    written. Returns `output_dir`. `client` is a `PostTrainingClient`; one is made
    from the environment if not given.
    """
    from .service_client import PostTrainingClient

    own = client is None
    client = client or PostTrainingClient()
    try:
        response = client.create_rest_client().get_external_weights_urls(path).result()
        files: Dict[str, bytes] = {}
        for name, url in response.urls.items():
            if not _SAFE_NAME.match(name) or name in (".", ".."):
                raise PostTrainingError(f"refusing to write a file named {name!r}")
            files[name] = client._gw.fetch(url)
    finally:
        if own:
            client.close()

    for name, data in files.items():
        expected = response.sha256.get(name)
        if expected and hashlib.sha256(data).hexdigest() != expected:
            raise PostTrainingError(f"{path}: {name} doesn't match its sha256")
    missing = set(response.sha256) - set(files)
    if missing:
        raise PostTrainingError(
            f"{path}: no download URL for {', '.join(sorted(missing))}"
        )

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        part = out / f".{name}.part"
        part.write_bytes(data)
        os.replace(part, out / name)
    return str(out)
