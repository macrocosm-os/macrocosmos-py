"""Tinker's `RestClient`, for what Macrocosmos supports: getting saved weights out."""

from __future__ import annotations

from typing import Any, NoReturn

from ._http import Gateway
from .errors import NotFoundError, NotSupportedError
from .futures import APIFuture
from .types import ExternalWeightsUrlsResponse


class RestClient:
    """Made by `PostTrainingClient.create_rest_client()`."""

    def __init__(self, gateway: Gateway) -> None:
        self._gw = gateway

    def get_external_weights_urls(
        self, path: str
    ) -> APIFuture[ExternalWeightsUrlsResponse]:
        """Signed download URLs, one per file, for a saved adapter's `mc://` path."""
        try:
            reply = self._gw.request("POST", "/adapters/urls", {"path": path})
        except NotFoundError as e:
            if _no_such_route(e):
                raise NotSupportedError(
                    "this gateway can't serve adapter downloads yet"
                ) from None
            raise
        response = ExternalWeightsUrlsResponse(
            urls=dict(reply["urls"]), expires_at=reply.get("expires_at")
        )
        return APIFuture.completed(response, label="get_external_weights_urls")

    async def get_external_weights_urls_async(
        self, path: str
    ) -> ExternalWeightsUrlsResponse:
        return await self.get_external_weights_urls(path)

    # The rest of Tinker's RestClient (training runs, listing and publishing checkpoints).

    def get_training_run_by_tinker_path(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError("looking up training runs is not supported yet")

    def list_checkpoints(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError("listing checkpoints is not supported yet")

    list_user_checkpoints = list_checkpoints

    def delete_checkpoint_from_tinker_path(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError(
            "deleting checkpoints is not supported yet; saved adapters expire on their own"
        )

    def publish_checkpoint_from_tinker_path(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError("publishing checkpoints is not supported yet")


def _no_such_route(error: NotFoundError) -> bool:
    """FastAPI's bare 404 for an unknown route, as opposed to "adapter not found"."""
    body: Any = error.body
    return isinstance(body, dict) and body.get("detail") == "Not Found"
