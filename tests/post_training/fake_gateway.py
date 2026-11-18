"""An in-memory gateway that follows the `/platform/rl` contract.

Plug it into a client with `ServiceClient(api_key="test-key", transport=gw.transport)`.
Jobs finish after `polls_until_done` polls. `restart_trainer()` makes the next
optim_step ask for a replay, as a restarted trainer does.
"""

from __future__ import annotations

import itertools
import json
import random
import re
from typing import Any, Dict, List, Optional

import httpx

MAX_BODY = 16 * 1024


class FakeGateway:
    def __init__(
        self,
        *,
        models=("Qwen/Qwen3-4B", "Qwen/Qwen3-8B"),
        polls_until_done: int = 1,
        api_key: str = "test-key",
        legacy: bool = False,
    ) -> None:
        self.models = list(models)
        self.legacy = legacy  # a gateway that still requires requirements.max_workers
        self.polls_until_done = polls_until_done
        self.api_key = api_key
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.requests: List[httpx.Request] = []
        self.trainer: Dict[str, Dict[str, Any]] = {}  # model_id -> {step, pending}
        self._ids = itertools.count(1)
        self._restart_next = False
        self._fail_next: List[Optional[int]] = []
        self.fail_sampling: Optional[str] = None
        self.hold: set = set()  # ops whose new jobs stay pending until release()
        self.transport = httpx.MockTransport(self._handle)

    # --- test controls -------------------------------------------------------

    def restart_trainer(self) -> None:
        self._restart_next = True

    def fail_next(self, *statuses: Optional[int]) -> None:
        """Answer the next requests with these statuses; `None` lets one through."""
        self._fail_next.extend(statuses)

    def release(self) -> None:
        """Let held jobs finish."""
        self.hold.clear()
        for job in self.jobs.values():
            job["held"] = False

    def calls(self, method: str, pattern: str) -> List[httpx.Request]:
        return [
            r
            for r in self.requests
            if r.method == method and re.fullmatch(pattern, r.url.path)
        ]

    # --- routing --------------------------------------------------------------

    def _handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if self._fail_next:
            status = self._fail_next.pop(0)
            if status is not None:
                return _err(status, "injected failure")
        if len(request.content) > MAX_BODY:
            return httpx.Response(413, text="<html>413 Request Entity Too Large</html>")
        if request.headers.get("x-api-key") != self.api_key:
            return _err(401, "invalid API key")
        body = json.loads(request.content) if request.content else None
        path, method = request.url.path, request.method
        for pattern, verb, fn in self._routes():
            m = re.fullmatch(pattern, path)
            if m and verb == method:
                return fn(body, *m.groups())
        return _err(404, "Not Found")

    def _routes(self):
        return [
            (r"/platform/base-models", "GET", self._base_models),
            (r"/platform/rl/sessions", "POST", self._open),
            (r"/platform/rl/sessions/([^/]+)/close", "POST", self._close),
            (r"/platform/rl/sessions/([^/]+)/models", "POST", self._create_model),
            (r"/platform/rl/models/([^/]+)", "GET", self._model_info),
            (
                r"/platform/rl/models/([^/]+)/(forward_backward|optim_step|save_weights_for_sampler)",
                "POST",
                self._op,
            ),
            (r"/platform/rl/training/([^/]+)", "GET", self._job),
            (r"/platform/rl/inference", "POST", self._infer),
            (r"/platform/rl/inference/([^/]+)", "GET", self._job_results),
        ]

    # --- sessions --------------------------------------------------------------

    def _base_models(self, _body):
        return _ok(
            [
                {"model_id": m, "weights_gb": 8.0, "min_vram_gb": 16.0}
                for m in self.models
            ]
        )

    def _open(self, body):
        if body["base_model"] not in self.models:
            return _err(422, f"base model {body['base_model']} is not registered")
        if self.legacy and "max_workers" not in body["requirements"]:
            return httpx.Response(
                422,
                json={
                    "detail": [
                        {
                            "type": "missing",
                            "loc": ["body", "requirements", "max_workers"],
                            "msg": "Field required",
                        }
                    ]
                },
            )
        sid = f"rls-{next(self._ids):024x}"
        req = {
            "max_output_tokens": None,
            "max_lora_rank": None,
            **body["requirements"],
        }
        self.sessions[sid] = {
            "session_id": sid,
            "state": "open",
            "base_model": body["base_model"],
            "requirements": req,
            "model": None,
        }
        return _ok(self.sessions[sid], 201)

    def _close(self, _body, sid):
        if sid not in self.sessions:
            return _err(404, "session not found")
        self.sessions[sid]["state"] = "closed"
        return _ok(self.sessions[sid])

    def _session(self, sid) -> Optional[Dict[str, Any]]:
        return self.sessions.get(sid)

    # --- training --------------------------------------------------------------

    def _create_model(self, body, sid):
        s = self._session(sid)
        if s is None:
            return _err(404, "session not found")
        if s["state"] == "closed":
            return _err(409, "session is closed")
        if body["base_model"] != s["base_model"]:
            return _err(422, "base_model is not the session's")
        if body["lora"]["rank"] != s["requirements"]["max_lora_rank"]:
            return _err(422, "lora.rank must equal the session's max_lora_rank")
        model_id = f"{sid}-m0"
        handle = f"{model_id}.0"
        s["model"] = model_id
        self.trainer[model_id] = {"step": 0, "pending": 0}
        self._queue(
            handle, {"base_model": body["base_model"], "lora": body["lora"], "step": 0}
        )
        return _ok({"model_id": model_id, "handle": handle}, 202)

    def _model_info(self, _body, model_id):
        sid = model_id.rsplit("-m", 1)[0]
        s = self._session(sid)
        if s is None or s["model"] != model_id:
            return _err(404, "model not found")
        return _ok(
            {
                "model_id": model_id,
                "model_name": s["base_model"],
                "is_lora": True,
                "lora_rank": s["requirements"]["max_lora_rank"],
                "model_data": {
                    "model_name": s["base_model"],
                    "tokenizer_id": s["base_model"],
                },
            }
        )

    def _op(self, body, model_id, op):
        sid = model_id.rsplit("-m", 1)[0]
        s = self._session(sid)
        if s is None or s["model"] != model_id:
            return _err(404, "model not found")
        if s["state"] == "closed":
            return _err(409, "session is closed")
        handle = f"{model_id}.{body['seq_id']}"
        if handle in self.jobs:  # a reused seq_id returns the old job
            return _ok({"handle": handle}, 202)
        t = self.trainer[model_id]
        if op == "forward_backward":
            for d in body["data"]:
                assert all(len(v) == len(d["tokens"]) for v in d["inputs"].values()), (
                    "input lengths must match tokens"
                )
            t["pending"] += 1
            n_tokens = sum(len(d["tokens"]) for d in body["data"])
            result = {
                "metrics": {
                    "loss:sum": round(random.uniform(0.5, 2.0) * n_tokens, 3),
                    "clip_frac:mean": 0.1,
                },
                "logprobs": [[-1.0] * len(d["tokens"]) for d in body["data"]],
            }
        elif op == "optim_step":
            if self._restart_next:  # the trainer restarted and lost the gradients
                self._restart_next = False
                t["pending"] = 0
            if t["step"] == body["at_step"] + 1 and t["pending"] == 0:
                result = {"step": t["step"], "metrics": {}, "already": True}
            elif t["pending"] != body["pending"]:
                result = {"replay": True, "have": t["pending"], "step": t["step"]}
                t["pending"] = 0
            else:
                t["step"] += 1
                t["pending"] = 0
                result = {"step": t["step"], "metrics": {"grad_norm": 0.42}}
        else:
            suffix = (
                f"named/{body['name']}"
                if body.get("name")
                else f"rollout-{body['seq_id']}"
            )
            result = {
                "path": f"mc://{model_id}/adapters/{suffix}",
                "version": t["step"],
            }
        self._queue(handle, result, held=op in self.hold)
        return _ok({"handle": handle}, 202)

    def _job(self, _body, handle):
        job = self.jobs.get(handle)
        if job is None:
            return _err(404, "job not found")
        job["polls"] += 1
        if job["polls"] < self.polls_until_done or job.get("held"):
            return _ok({"state": "pending", "result": None, "error": None})
        return _ok(
            {
                "state": job.get("state", "done"),
                "result": job["result"],
                "error": job.get("error"),
            }
        )

    # --- sampling --------------------------------------------------------------

    def _infer(self, body):
        s = self._session(body["session_id"])
        if s is None:
            return _err(404, "session not found")
        if s["state"] == "closed":
            return _err(409, "session is closed")
        handle = f"batch{next(self._ids)}.{len(body['prompts'])}"
        version = (
            self.trainer.get(s["model"] or "", {}).get("step", -1) if s["model"] else -1
        )
        results = []
        for i, p in enumerate(body["prompts"]):
            seqs = []
            for _ in range(p.get("n", 1)):
                n = random.randint(1, p.get("max_tokens") or 8)
                seq = {
                    "tokens": [random.randint(10, 1000) for _ in range(n)],
                    "stop_reason": random.choice(["stop", "length"]),
                }
                if p.get("logprobs"):
                    seq["logprobs"] = [-0.5] * n
                seqs.append(seq)
            if self.fail_sampling:
                results.append(
                    {"index": i, "state": "failed", "error": self.fail_sampling}
                )
                continue
            results.append(
                {
                    "index": i,
                    "state": "done",
                    "sequences": seqs,
                    "policy_version": version,
                    "usage": {
                        "prompt_tokens": len(p["prompt_tokens"]),
                        "cached_tokens": 0,
                        "completion_tokens": sum(len(x["tokens"]) for x in seqs),
                    },
                }
            )
        self.jobs[handle] = {"polls": 0, "results": results}
        return _ok({"handle": handle, "n": len(body["prompts"])}, 202)

    def _job_results(self, _body, handle):
        job = self.jobs.get(handle)
        if job is None:
            return _err(404, "batch not found")
        job["polls"] += 1
        return _ok(
            {
                "results": job["results"]
                if job["polls"] >= self.polls_until_done
                else None
            }
        )

    def _queue(self, handle, result, held=False):
        self.jobs[handle] = {"polls": 0, "result": result, "held": held}


def _ok(body, status=200):
    return httpx.Response(status, json=body)


def _err(status, detail):
    return httpx.Response(status, json={"detail": detail})
