"""Tinker's `RestClient`, for what Macrocosmos supports: a model's saved adapters
(checkpoints), listing them and getting their files out."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, NoReturn, Optional, Tuple
from urllib.parse import quote

from ._http import Gateway
from .errors import NotSupportedError
from .futures import APIFuture
from .types import Checkpoint, CheckpointsListResponse, ExternalWeightsUrlsResponse

MC_SCHEME = "mc://"


class RestClient:
    """Made by `PostTrainingClient.create_rest_client()`."""

    def __init__(self, gateway: Gateway) -> None:
        self._gw = gateway

    def list_checkpoints(
        self, training_run_id: str
    ) -> APIFuture[CheckpointsListResponse]:
        """A model's saved adapters, oldest first. `training_run_id` is the model id
        (`TrainingClient.model_id`); still readable after the session closes."""
        reply = self._get(f"/models/{quote(training_run_id, safe='')}/checkpoints")
        response = CheckpointsListResponse(
            checkpoints=[_checkpoint(c) for c in reply.get("checkpoints", [])],
            cursor=reply.get("cursor"),
        )
        return APIFuture.completed(response, label="list_checkpoints")

    def get_external_weights_urls(
        self, path: str
    ) -> APIFuture[ExternalWeightsUrlsResponse]:
        """Signed download URLs, one per file, for a saved adapter's `mc://` path."""
        model_id, checkpoint_id = parse_path(path)
        reply = self._get(
            f"/models/{quote(model_id, safe='')}/checkpoints/{quote(checkpoint_id, safe='/')}/download_urls"
        )
        response = ExternalWeightsUrlsResponse(
            urls=dict(reply["urls"]),
            expires=_when(reply.get("expires")),
            sha256=dict(reply.get("sha256") or {}),
        )
        return APIFuture.completed(response, label="get_external_weights_urls")

    async def list_checkpoints_async(
        self, training_run_id: str
    ) -> CheckpointsListResponse:
        return await self.list_checkpoints(training_run_id)

    async def get_external_weights_urls_async(
        self, path: str
    ) -> ExternalWeightsUrlsResponse:
        return await self.get_external_weights_urls(path)

    # The rest of Tinker's RestClient (training runs, publishing, deleting).

    def get_training_run_by_tinker_path(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError("looking up training runs is not supported yet")

    def list_user_checkpoints(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError(
            "listing all your checkpoints is not supported yet; use list_checkpoints(model_id)"
        )

    def delete_checkpoint_from_tinker_path(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError(
            "deleting checkpoints is not supported yet; saved adapters expire on their own"
        )

    def publish_checkpoint_from_tinker_path(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError("publishing checkpoints is not supported yet")

    def _get(self, path: str) -> Dict[str, Any]:
        return self._gw.request("GET", path)


def parse_path(path: str) -> Tuple[str, str]:
    """`mc://{model_id}/{checkpoint_id}` → (model_id, checkpoint_id)."""
    if not path.startswith(MC_SCHEME) or "/" not in path[len(MC_SCHEME) :]:
        raise ValueError(
            f"not a saved adapter's path: {path!r} (expected mc://<model_id>/adapters/...)"
        )
    model_id, _, checkpoint_id = path[len(MC_SCHEME) :].partition("/")
    return model_id, checkpoint_id


def _checkpoint(raw: Dict[str, Any]) -> Checkpoint:
    return Checkpoint(
        checkpoint_id=raw["checkpoint_id"],
        checkpoint_type=raw.get("checkpoint_type", "sampler"),
        time=_when(raw.get("time")),
        tinker_path=raw["tinker_path"],
        size_bytes=raw.get("size_bytes"),
        public=bool(raw.get("public", False)),
        user_metadata=raw.get("user_metadata"),
        expires_at=_when(raw.get("expires_at")),
        base_model=raw.get("base_model"),
    )


def _when(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, timezone.utc)
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
