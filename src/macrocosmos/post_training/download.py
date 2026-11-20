"""Download a saved adapter's files, as Tinker's cookbook does with `weights.download`."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Optional

from .errors import PostTrainingError

_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
MANIFEST = "manifest.json"


def download(path: str, output_dir: str, *, client: Optional[Any] = None) -> str:
    """Download the adapter saved at `path` (an `mc://` path) into `output_dir`.

    Writes its PEFT files (`adapter_config.json`, `adapter_model.safetensors`)
    and checks each against the sha256 in the adapter's manifest. Returns
    `output_dir`. `client` is a `PostTrainingClient`; one is made from the
    environment if not given.
    """
    from .service_client import PostTrainingClient

    own = client is None
    client = client or PostTrainingClient()
    try:
        urls = client.create_rest_client().get_external_weights_urls(path).result().urls
        files = {
            name: client._gw.fetch(url) for name, url in urls.items() if _safe(name)
        }
    finally:
        if own:
            client.close()

    manifest = json.loads(files[MANIFEST]) if MANIFEST in files else {}
    for name, digest in (manifest.get("sha256") or {}).items():
        if name not in files:
            raise PostTrainingError(
                f"{path}: {name} is in the manifest but wasn't downloaded"
            )
        if hashlib.sha256(files[name]).hexdigest() != digest:
            raise PostTrainingError(
                f"{path}: {name} doesn't match its sha256 in the manifest"
            )

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        tmp = out / f".{name}.part"
        tmp.write_bytes(data)
        os.replace(tmp, out / name)
    return str(out)


def _safe(name: str) -> bool:
    if not _SAFE_NAME.match(name) or name in (".", ".."):
        raise PostTrainingError(f"refusing to write a file named {name!r}")
    return True
