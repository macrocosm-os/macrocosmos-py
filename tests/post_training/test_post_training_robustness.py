"""Retries, failures and the parts of Tinker we don't support yet."""

import asyncio
import json

import pytest

from macrocosmos import post_training
from macrocosmos.post_training import _http, types

from .fake_gateway import FakeGateway

MODEL = "Qwen/Qwen3-4B"


@pytest.fixture(autouse=True)
def no_backoff(monkeypatch):
    monkeypatch.setattr(_http.time, "sleep", lambda _s: None)


@pytest.fixture
def gw():
    return FakeGateway()


@pytest.fixture
def service(gw):
    with post_training.PostTrainingClient(
        api_key="test-key", base_url="http://gw.test", transport=gw.transport
    ) as client:
        yield client


def test_reads_and_idempotent_writes_are_retried_on_503(gw, service):
    gw.fail_next(503, 502)
    assert [m["model_id"] for m in service.get_server_capabilities()] == [
        "Qwen/Qwen3-4B",
        "Qwen/Qwen3-8B",
    ]


def test_opening_a_session_is_not_retried_so_no_second_session_leaks(gw, service):
    gw.fail_next(503)
    with pytest.raises(post_training.InternalServerError):
        service.create_lora_training_client(base_model=MODEL)
    assert len(gw.calls("POST", r"/v1/sessions")) == 1
    assert gw.sessions == {}


def test_submitting_samples_is_not_retried_so_nothing_is_paid_for_twice(gw, service):
    sampler = service.create_sampling_client(base_model=MODEL)
    service._gw.max_request_bytes  # noqa: B018 - read the limits before the failure
    gw.fail_next(503)
    with pytest.raises(post_training.InternalServerError):
        sampler.sample([1, 2, 3], num_samples=2)
    assert len(gw.calls("POST", r"/v1/sampling")) == 1


def test_a_failed_model_create_releases_its_session_at_once(gw, service):
    gw.fail_next(None, 409)  # the session opens, creating its model fails
    with pytest.raises(post_training.ConflictError):
        service.create_lora_training_client(base_model=MODEL)
    [session] = gw.sessions.values()
    assert session["state"] == "closed"


def test_a_failed_sample_raises_request_failed(gw, service):
    sampler = service.create_sampling_client(base_model=MODEL)
    gw.fail_sampling = "out of retries"
    with pytest.raises(post_training.RequestFailedError, match="out of retries"):
        sampler.sample([1, 2, 3], num_samples=2).result()


def test_a_failed_job_raises_with_the_trainers_reason(gw, service):
    trainer = service.create_lora_training_client(base_model=MODEL).result()
    future = trainer.save_weights_for_sampler("x")
    handle = next(iter(k for k in gw.jobs if k.endswith(".1")))
    gw.jobs[handle].update(
        state="failed", error="TrainerRestarted: the trainer is at step 3"
    )
    with pytest.raises(post_training.RequestFailedError, match="TrainerRestarted"):
        future.result()
    with pytest.raises(
        post_training.RequestFailedError
    ):  # the error sticks to the future
        future.result()


def test_stop_token_ids_and_stop_strings_are_told_apart(gw, service):
    sampler = service.create_sampling_client(base_model=MODEL)
    sampler.sample(
        [1], sampling_params=types.SamplingParams(stop=[151645, 151643])
    ).result()
    sampler.sample([1], sampling_params=types.SamplingParams(stop="\n\n")).result()
    first, second = (
        json.loads(r.content)["prompts"][0] for r in gw.calls("POST", r"/v1/sampling")
    )
    assert first["stop_token_ids"] == [151645, 151643] and "stop" not in first
    assert second["stop"] == ["\n\n"]


def test_async_variants_follow_tinkers_shapes(service):
    async def main():
        trainer = await service.create_lora_training_client_async(MODEL, rank=32)
        datum = types.Datum(
            types.ModelInput.from_ints([1, 2, 3]),
            {
                "target_tokens": [2, 3, 4],
                "logprobs": [0.0] * 3,
                "advantages": [1.0] * 3,
            },
        )
        fb = await trainer.forward_backward_async(
            [datum], "importance_sampling"
        )  # submit
        step = await trainer.optim_step_async(types.AdamParams())
        sampler = await trainer.save_weights_and_get_sampling_client_async()
        response = await sampler.sample_async([1, 2], num_samples=3)
        return (await fb), (await step), response  # results

    fb, step, response = asyncio.run(main())
    assert (
        len(fb.loss_fn_outputs) == 1 and step.step == 1 and len(response.sequences) == 3
    )


def test_save_state_saves_the_adapter_and_warns_once(service):
    trainer = service.create_lora_training_client(base_model=MODEL).result()
    with pytest.warns(UserWarning, match="adapter weights only"):
        first = trainer.save_state("000020").result()
    second = trainer.save_state("final").result()
    assert first.path.endswith("named/state-000020") and second.path.endswith(
        "named/state-final"
    )


@pytest.mark.parametrize(
    "call",
    [
        lambda s, t: t.forward([], "cross_entropy"),
        lambda s, t: t.forward_backward_custom([], None),
        lambda s, t: t.load_state("mc://x"),
        lambda s, t: t.create_sampling_client().compute_logprobs([1]),
        lambda s, t: s.create_training_client_from_state("mc://x"),
        lambda s, t: s.create_rest_client().list_user_checkpoints(),
    ],
)
def test_unsupported_features_say_so(service, call):
    trainer = service.create_lora_training_client(base_model=MODEL).result()
    with pytest.raises(post_training.NotSupportedError):
        call(service, trainer)


def test_closing_twice_and_the_repr_are_harmless(gw):
    client = post_training.PostTrainingClient(
        api_key="test-key", base_url="http://gw.test", transport=gw.transport
    )
    client.create_sampling_client(base_model=MODEL)
    assert "sessions=['rls-" in repr(client)
    client.close()
    client.close()
    assert len(gw.calls("POST", r"/v1/sessions/.+/close")) == 1
