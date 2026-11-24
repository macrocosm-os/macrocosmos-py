"""Failure paths: what happens when a request, the trainer or the caller misbehaves."""

import gc
import json
import math

import pytest

from macrocosmos import post_training
from macrocosmos.post_training import _http, service_client as service_module, types
from macrocosmos.post_training.futures import APIFuture

from .fake_gateway import FakeGateway

MODEL = "Qwen/Qwen3-4B"


@pytest.fixture(autouse=True)
def no_backoff(monkeypatch):
    monkeypatch.setattr(_http.time, "sleep", lambda _s: None)


@pytest.fixture
def gw():
    return FakeGateway()


def client(gw):
    return post_training.PostTrainingClient(
        api_key="test-key",
        base_url="http://gw.test",
        transport=gw.transport,
        max_request_bytes=15 * 1024,
    )


def datum(n=8):
    tokens = list(range(1, n + 1))
    return types.Datum(
        types.ModelInput.from_ints(tokens),
        {"target_tokens": tokens, "logprobs": [-0.5] * n, "advantages": [0.5] * n},
    )


def test_sessions_close_at_exit_even_if_only_the_training_client_was_kept(gw):
    trainer = client(gw).create_lora_training_client(base_model=MODEL).result()
    gc.collect()  # the ServiceClient itself is gone
    service_module._close_open_clients()  # what atexit runs
    assert gw.sessions[trainer.session_id]["state"] == "closed"


def test_an_optim_step_that_fails_to_send_can_be_sent_again(gw):
    with client(gw) as service:
        trainer = service.create_lora_training_client(base_model=MODEL).result()
        trainer.forward_backward([datum()], "importance_sampling").result()
        gw.fail_next(500)
        with pytest.raises(post_training.InternalServerError):
            trainer.optim_step(types.AdamParams())
        assert trainer.optim_step(types.AdamParams()).result().step == 1
        sent = [json.loads(r.content) for r in gw.calls("POST", r".+/optim_step")]
        assert [(b["at_step"], b["pending"]) for b in sent] == [(0, 1), (0, 1)]


def test_a_split_batch_that_fails_halfway_is_reconciled_by_the_next_step(gw):
    with client(gw) as service:
        trainer = service.create_lora_training_client(base_model=MODEL).result()
        big = [datum(300) for _ in range(6)]  # two requests
        service._gw.max_inflight_bytes  # noqa: B018 - read the limits before the failures
        gw.fail_next(None, 500)  # the first request lands, the second doesn't
        with pytest.raises(post_training.InternalServerError):
            trainer.forward_backward(big, "importance_sampling")
        # The trainer holds 1 request, the client counts 2: the trainer asks for a replay.
        assert trainer.optim_step(types.AdamParams()).result().step == 1
        assert len(gw.calls("POST", r".+/forward_backward")) == 4  # 2 tries + 2 resent


def test_a_replay_interrupted_by_a_timeout_resumes_without_resending_twice(gw):
    with client(gw) as service:
        trainer = service.create_lora_training_client(base_model=MODEL).result()
        trainer.forward_backward([datum()], "importance_sampling").result()
        gw.restart_trainer()
        gw.hold.add("forward_backward")  # the resent data is slow
        step = trainer.optim_step(types.AdamParams())
        with pytest.raises(post_training.APITimeoutError):
            step.result(timeout=0.3)
        gw.release()
        assert step.result().step == 1
        assert (
            len(gw.calls("POST", r".+/forward_backward")) == 2
        )  # original + one resend
        assert len(gw.calls("POST", r".+/optim_step")) == 2


def test_ctrl_c_while_waiting_is_not_remembered_by_the_future():
    calls = []

    def resolve(_timeout):
        calls.append(1)
        if len(calls) == 1:
            raise KeyboardInterrupt
        return "ok"

    future = APIFuture(resolve)
    with pytest.raises(KeyboardInterrupt):
        future.result()
    assert not future.done() and future.result() == "ok"


def test_a_failed_create_job_releases_its_session(gw):
    with client(gw) as service:
        future = service.create_lora_training_client(base_model=MODEL)
        [(handle, job)] = [(h, j) for h, j in gw.jobs.items() if h.endswith(".0")]
        job.update(state="failed", error="no trainer could load the model")
        with pytest.raises(
            post_training.RequestFailedError, match="could not load|no trainer"
        ):
            future.result()
        [session] = gw.sessions.values()
        assert session["state"] == "closed"


def test_a_sampler_for_an_older_adapter_warns_that_it_got_a_newer_one(gw):
    with client(gw) as service:
        trainer = service.create_lora_training_client(base_model=MODEL).result()
        old = trainer.save_weights_and_get_sampling_client().result()
        trainer.forward_backward([datum()], "importance_sampling")
        trainer.optim_step(types.AdamParams()).result()
        with pytest.warns(
            UserWarning, match="asked for adapter version 0, got samples from version 1"
        ):
            response = old.sample([1, 2], num_samples=2).result()
        assert response.policy_version == 1


def test_prompt_logprobs_are_refused_rather_than_silently_dropped(gw):
    with client(gw) as service:
        sampler = service.create_sampling_client(base_model=MODEL)
        with pytest.raises(
            post_training.NotSupportedError, match="include_prompt_logprobs"
        ):
            sampler.sample([1, 2], num_samples=1, include_prompt_logprobs=True)


def test_create_sampling_client_takes_tinkers_argument_order(gw):
    with client(gw) as service:
        sampler = service.create_sampling_client(None, MODEL)
        assert sampler.base_model == MODEL


def test_a_closed_client_says_so(gw):
    service = client(gw)
    service.create_sampling_client(base_model=MODEL)
    service.close()
    with pytest.raises(post_training.PostTrainingError, match="closed"):
        service.create_sampling_client(base_model=MODEL)


def test_nan_is_refused_before_it_becomes_invalid_json(gw):
    with client(gw) as service:
        trainer = service.create_lora_training_client(base_model=MODEL).result()
        bad = types.Datum(
            types.ModelInput.from_ints([1, 2]),
            {"target_tokens": [2, 3], "advantages": [math.nan, 0.0]},
        )
        with pytest.raises(ValueError, match="NaN"):
            trainer.forward_backward([bad], "importance_sampling")


def test_dict_datums_with_numpy_like_values_are_converted():
    class Arr:  # stands in for a numpy array: has tolist()
        def __init__(self, v):
            self.v = v

        def tolist(self):
            return self.v

    wire = types.datum_to_wire(
        {
            "tokens": Arr([1, 2]),
            "inputs": {"target_tokens": Arr([2, 3]), "mask": [1, 1]},
        }
    )
    assert wire == {"tokens": [1, 2], "inputs": {"target_tokens": [2, 3]}}


def test_a_future_recovers_after_transient_gateway_errors(gw):
    with client(gw) as service:
        trainer = service.create_lora_training_client(base_model=MODEL).result()
        future = trainer.forward_backward([datum()], "importance_sampling")
        gw.fail_next(*[503] * 5)  # every retry of the first poll fails
        with pytest.raises(post_training.InternalServerError):
            future.result()
        assert not future.done()
        assert len(future.result().loss_fn_outputs) == 1  # the job was fine all along


def test_finished_steps_are_freed(gw):
    import weakref

    with client(gw) as service:
        trainer = service.create_lora_training_client(base_model=MODEL).result()
        trainer.forward_backward([datum()], "importance_sampling")
        first = weakref.ref(trainer.optim_step(types.AdamParams()))
        for _ in range(3):
            trainer.forward_backward([datum()], "importance_sampling")
            trainer.optim_step(types.AdamParams()).result()
        gc.collect()
        assert first() is None  # nothing keeps the first step (or its data) alive
