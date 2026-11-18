from __future__ import annotations

import atexit
import threading
from typing import Any, Dict, List, NoReturn, Optional, Set

import httpx

from ._http import Gateway
from .errors import NotSupportedError, RequestFailedError, UnprocessableEntityError
from .futures import _WAITERS, APIFuture, run_in, wait_for_job
from .sampling_client import SamplingClient
from .training_client import DEFAULT_TRAIN_TIMEOUT_S, TrainingClient
from .types import GetInfoResponse, ModelData

# Users choose the base model, LoRA rank and max tokens; the platform decides
# the workers. Gateways from before that change still require `max_workers`:
# for them only, the session is requested again with this value.
LEGACY_MAX_WORKERS = 4


class PostTrainingClient:
    """The entry point. Owns every session it opens. Also available as
    `ServiceClient`, its name on Tinker.

        import macrocosmos as mc

        with mc.PostTrainingClient() as client:
            training_client = client.create_lora_training_client(
                base_model="Qwen/Qwen3-8B", rank=32
            ).result()
            ...

    Unlike Tinker, a session reserves GPUs for you while it's open. Leaving the
    `with` block or calling `close()` closes every session this client opened,
    and so does the interpreter exiting.

    The API key comes from `api_key=` or `MACROCOSMOS_POST_TRAINING_API_KEY`, the URL from
    `base_url=` or `MACROCOSMOS_POST_TRAINING_BASE_URL`.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        *,
        app_name: Optional[str] = None,
        timeout: float = 30.0,
        transport: Optional[httpx.BaseTransport] = None,
        **_tinker_options: Any,  # user_metadata, project_id, display_name: accepted, unused
    ) -> None:
        self._gw = Gateway(
            api_key, base_url, timeout=timeout, app_name=app_name, transport=transport
        )
        self._sessions: List[str] = []
        self._closed: Set[str] = set()
        self._lock = threading.Lock()

    # --- clients --------------------------------------------------------------------

    def create_lora_training_client(
        self,
        base_model: str,
        rank: int = 32,
        seed: Optional[int] = None,
        train_mlp: bool = True,
        train_attn: bool = True,
        train_unembed: bool = True,
        *,
        max_output_tokens: Optional[int] = None,
        **_: Any,
    ) -> APIFuture[TrainingClient]:
        """Open a session and create a LoRA adapter on `base_model`.

        `max_output_tokens` is the longest completion the session will be asked for.
        """
        session_id = self._open_session(
            base_model, lora_rank=rank, max_output_tokens=max_output_tokens
        )
        lora: Dict[str, Any] = {
            "rank": rank,
            "train_mlp": train_mlp,
            "train_attn": train_attn,
            "train_unembed": train_unembed,
        }
        if seed is not None:
            lora["seed"] = seed
        try:
            created = self._gw.request(
                "POST",
                f"/sessions/{session_id}/models",
                {"base_model": base_model, "lora": lora},
            )
        except BaseException:
            self._release(session_id)  # don't hold GPUs for a model that won't exist
            raise

        def resolve(timeout: Optional[float]) -> TrainingClient:
            try:
                result = wait_for_job(
                    self._gw,
                    created["handle"],
                    DEFAULT_TRAIN_TIMEOUT_S if timeout is None else timeout,
                    what=f"creating the LoRA on {base_model}",
                )
            except RequestFailedError:
                self._release(session_id)
                raise
            info = _info(self._gw.request("GET", f"/models/{created['model_id']}"))
            return TrainingClient(
                self._gw, session_id, info, step=result.get("step") or 0
            )

        return APIFuture(resolve, label=f"create_lora_training_client({base_model})")

    def create_sampling_client(
        self,
        model_path: Optional[str] = None,
        base_model: Optional[str] = None,
        **_: Any,
    ) -> SamplingClient:
        """A sampler on a base model, in a session of its own."""
        if base_model is None:
            raise NotSupportedError(
                "pass base_model=; to sample a trained adapter, use "
                "training_client.save_weights_and_get_sampling_client()"
            )
        session_id = self._open_session(base_model)
        return SamplingClient(
            self._gw, session_id, base_model=base_model, model_path=model_path
        )

    async def create_lora_training_client_async(
        self, base_model: str, rank: int = 32, **kw: Any
    ) -> TrainingClient:
        future = await run_in(
            _WAITERS, self.create_lora_training_client, base_model, rank, **kw
        )
        return await future

    async def create_sampling_client_async(
        self,
        model_path: Optional[str] = None,
        base_model: Optional[str] = None,
        **kw: Any,
    ) -> SamplingClient:
        return await run_in(
            _WAITERS, self.create_sampling_client, model_path, base_model, **kw
        )

    def get_server_capabilities(self) -> List[Dict[str, Any]]:
        """The base models you can train and sample, with their GPU memory needs."""
        return self._gw.request("GET", "/base-models")

    def create_training_client_from_state(self, *_: Any, **__: Any) -> NoReturn:
        raise NotSupportedError("resuming from a checkpoint is not supported yet")

    create_training_client_from_state_with_optimizer = create_training_client_from_state

    def create_rest_client(self) -> NoReturn:
        raise NotSupportedError(
            "the REST client (runs and checkpoints) is not supported yet"
        )

    # --- sessions -------------------------------------------------------------------

    @property
    def session_ids(self) -> List[str]:
        """Every session this client opened, open or closed."""
        return list(self._sessions)

    def close(self) -> None:
        """Close every session this client opened. Safe to call more than once."""
        with self._lock:
            still_open = [s for s in self._sessions if s not in self._closed]
        errors = []
        for session_id in still_open:
            try:
                self._close_session(session_id)
            except Exception as e:  # noqa: BLE001 - try every session, then report
                errors.append(f"{session_id}: {e}")
        if errors:  # stays registered, so exit tries again
            raise RequestFailedError("could not close sessions: " + "; ".join(errors))
        _OPEN_CLIENTS.discard(self)
        self._gw.close()

    def __enter__(self) -> "PostTrainingClient":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        try:
            self.close()
        except Exception:
            if exc_type is None:
                raise  # otherwise the with-body's own exception is the one to see

    def __repr__(self) -> str:
        return f"PostTrainingClient({self._gw.base_url!r}, sessions={self._sessions})"

    def _open_session(
        self,
        base_model: str,
        *,
        lora_rank: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
    ) -> str:
        requirements: Dict[str, Any] = {}
        if lora_rank is not None:
            requirements["max_lora_rank"] = lora_rank
        if max_output_tokens is not None:
            requirements["max_output_tokens"] = max_output_tokens
        body = {"base_model": base_model, "requirements": requirements}
        try:
            # Not retried blindly: a retry could open a second session.
            session = self._gw.request("POST", "/sessions", body, idempotent=False)
        except UnprocessableEntityError as e:
            if not _missing_field(e, "max_workers"):
                raise
            # A 422 opened nothing, so asking again can't leave a second session.
            requirements["max_workers"] = LEGACY_MAX_WORKERS
            session = self._gw.request("POST", "/sessions", body, idempotent=False)
        with self._lock:
            self._sessions.append(session["session_id"])
            _OPEN_CLIENTS.add(self)
        return session["session_id"]

    def _close_session(self, session_id: str) -> None:
        self._gw.request("POST", f"/sessions/{session_id}/close")
        with self._lock:
            self._closed.add(session_id)

    def _release(self, session_id: str) -> None:
        """Close a session now, on an error path: never raises over the original error."""
        try:
            self._close_session(session_id)
        except Exception:  # noqa: BLE001 - close() and exit try again
            pass


def _missing_field(error: UnprocessableEntityError, field: str) -> bool:
    """Whether a 422 says the request lacked `field` (FastAPI's validation detail)."""
    detail = error.body.get("detail") if isinstance(error.body, dict) else None
    return isinstance(detail, list) and any(
        isinstance(d, dict)
        and d.get("type") == "missing"
        and (d.get("loc") or [])[-1:] == [field]
        for d in detail
    )


def _info(reply: Dict[str, Any]) -> GetInfoResponse:
    data = reply.get("model_data") or {}
    return GetInfoResponse(
        model_id=reply["model_id"],
        model_data=ModelData(
            model_name=data.get("model_name") or reply.get("model_name"),
            tokenizer_id=data.get("tokenizer_id"),
        ),
        is_lora=reply.get("is_lora", True),
        lora_rank=reply.get("lora_rank"),
        model_name=reply.get("model_name"),
    )


# Clients with sessions still open. Held strongly on purpose: a client that is
# garbage-collected (say only its TrainingClient was kept) must still have its
# sessions closed at exit.
_OPEN_CLIENTS: Set[PostTrainingClient] = set()

#: Tinker's name for the entry point, so ported scripts keep working.
ServiceClient = PostTrainingClient


@atexit.register
def _close_open_clients() -> None:
    """Close sessions left open by scripts that don't use `with`.

    A hard kill skips this; the gateway's idle timeout closes those sessions.
    """
    for client in list(_OPEN_CLIENTS):
        try:
            client.close()
        except Exception:  # noqa: BLE001 - the interpreter is exiting anyway
            pass
