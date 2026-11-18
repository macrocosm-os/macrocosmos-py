import asyncio
import json

import pytest

from macrocosmos import post_training
from macrocosmos.post_training import types

from .fake_gateway import FakeGateway

MODEL = "Qwen/Qwen3-4B"


@pytest.fixture
def gw():
    return FakeGateway()


@pytest.fixture
def service(gw):
    with post_training.PostTrainingClient(
        api_key="test-key", base_url="http://gw.test", transport=gw.transport
    ) as client:
        yield client


def body(request):
    return json.loads(request.content)


def datum(n_tokens: int) -> types.Datum:
    tokens = list(range(1, n_tokens + 1))
    return types.Datum(
        model_input=types.ModelInput.from_ints(tokens),
        loss_fn_inputs={
            "target_tokens": types.TensorData(tokens, "int64"),
            "logprobs": types.TensorData([-0.5] * n_tokens),
            "advantages": types.TensorData([0.25] * n_tokens),
        },
    )


def test_create_opens_a_session_then_builds_the_model(gw, service):
    trainer = service.create_lora_training_client(base_model=MODEL, rank=16).result()

    [opened] = gw.calls("POST", r"/platform/rl/sessions")
    assert body(opened) == {
        "base_model": MODEL,
        "requirements": {"max_workers": 4, "max_lora_rank": 16},
    }
    [created] = gw.calls("POST", r"/platform/rl/sessions/.+/models")
    assert body(created)["lora"]["rank"] == 16
    assert trainer.get_info().model_data.tokenizer_id == MODEL
    assert trainer.get_info().lora_rank == 16


def test_leaving_the_with_block_closes_every_session(gw):
    with post_training.PostTrainingClient(
        api_key="test-key", base_url="http://gw.test", transport=gw.transport
    ) as service:
        service.create_lora_training_client(base_model=MODEL).result()
        service.create_lora_training_client(base_model=MODEL).result()
    assert [s["state"] for s in gw.sessions.values()] == ["closed", "closed"]


def test_an_error_in_the_block_still_closes_and_propagates(gw):
    with pytest.raises(KeyboardInterrupt):
        with post_training.PostTrainingClient(
            api_key="test-key", base_url="http://gw.test", transport=gw.transport
        ) as service:
            service.create_lora_training_client(base_model=MODEL).result()
            raise KeyboardInterrupt
    assert all(s["state"] == "closed" for s in gw.sessions.values())


def test_seq_ids_count_up_from_one_and_never_repeat(gw, service):
    trainer = service.create_lora_training_client(base_model=MODEL).result()
    trainer.forward_backward([datum(8)], loss_fn="importance_sampling")
    trainer.optim_step(types.AdamParams(learning_rate=1e-5))
    trainer.save_weights_for_sampler("final").result()
    ops = gw.calls(
        "POST",
        r"/platform/rl/models/.+/(forward_backward|optim_step|save_weights_for_sampler)",
    )
    assert [body(r)["seq_id"] for r in ops] == [1, 2, 3]


def test_calls_can_be_queued_before_waiting(service):
    trainer = service.create_lora_training_client(base_model=MODEL).result()
    fb = trainer.forward_backward([datum(8), datum(8)], loss_fn="importance_sampling")
    step = trainer.optim_step(types.AdamParams())
    assert step.result().step == 1
    out = fb.result()
    assert len(out.loss_fn_outputs) == 2
    assert out.loss_fn_outputs[0]["logprobs"].tolist() == [-1.0] * 8


def test_a_big_batch_is_split_under_the_body_limit(gw, service):
    trainer = service.create_lora_training_client(base_model=MODEL).result()
    data = [datum(300) for _ in range(12)]  # ~70 KB as JSON
    out = trainer.forward_backward(data, loss_fn="importance_sampling").result()

    sent = gw.calls("POST", r"/platform/rl/models/.+/forward_backward")
    assert len(sent) > 1
    assert all(len(r.content) < 16 * 1024 for r in sent)
    assert len(out.loss_fn_outputs) == 12
    assert out.metrics["clip_frac:mean"] == pytest.approx(0.1)
    # optim_step reports every request as pending, so the trainer's count matches
    trainer.optim_step(types.AdamParams()).result()
    assert body(gw.calls("POST", r".+/optim_step")[0])["pending"] == len(sent)


def test_one_datum_over_the_limit_fails_before_sending(service):
    trainer = service.create_lora_training_client(base_model=MODEL).result()
    with pytest.raises(post_training.PayloadTooLargeError, match="16 KB"):
        trainer.forward_backward([datum(4000)], loss_fn="importance_sampling")


def test_optim_step_replays_the_step_after_a_trainer_restart(gw, service):
    trainer = service.create_lora_training_client(base_model=MODEL).result()
    trainer.forward_backward([datum(8)], loss_fn="importance_sampling").result()
    gw.restart_trainer()
    result = trainer.optim_step(types.AdamParams()).result()

    assert result.step == 1
    assert len(gw.calls("POST", r".+/forward_backward")) == 2  # sent again
    assert len(gw.calls("POST", r".+/optim_step")) == 2


def test_sampling_returns_tokens_and_logprobs(service):
    trainer = service.create_lora_training_client(base_model=MODEL).result()
    sampler = trainer.save_weights_and_get_sampling_client().result()
    assert sampler.model_path.startswith("mc://")
    params = types.SamplingParams(max_tokens=16, temperature=1.0, stop="\n")
    response = sampler.sample(
        types.ModelInput.from_ints([1, 2, 3]), num_samples=4, sampling_params=params
    ).result()
    assert len(response.sequences) == 4
    assert all(len(s.logprobs) == len(s.tokens) for s in response.sequences)


def test_futures_can_be_awaited(service):
    async def main():
        trainer = await service.create_lora_training_client(base_model=MODEL)
        out = await trainer.forward_backward([datum(4)], loss_fn="importance_sampling")
        return out

    assert len(asyncio.run(main()).loss_fn_outputs) == 1


def test_a_slow_job_times_out_and_can_be_waited_on_again(gw, service):
    gw.polls_until_done = 10**9
    future = service.create_lora_training_client(base_model=MODEL)
    with pytest.raises(post_training.APITimeoutError):
        future.result(timeout=0.5)
    gw.polls_until_done = 0
    assert future.result().model_id.endswith("-m0")


@pytest.mark.parametrize(
    "call, error",
    [
        (
            lambda s: s.create_lora_training_client(base_model="nope/nope"),
            post_training.UnprocessableEntityError,
        ),
        (
            lambda s: post_training.PostTrainingClient(
                api_key="wrong-key",
                base_url="http://gw.test",
                transport=s._gw._http._transport,
            ).get_server_capabilities(),
            post_training.AuthenticationError,
        ),
    ],
)
def test_gateway_errors_are_typed(service, call, error):
    with pytest.raises(error):
        call(service)


def test_a_closed_session_is_a_conflict(gw, service):
    trainer = service.create_lora_training_client(base_model=MODEL).result()
    gw.sessions[trainer.session_id]["state"] = "closed"
    with pytest.raises(post_training.ConflictError, match="closed"):
        trainer.forward_backward([datum(4)], loss_fn="importance_sampling")


def test_no_api_key_is_a_clear_error(monkeypatch):
    monkeypatch.delenv("MACROCOSMOS_POST_TRAINING_API_KEY", raising=False)
    with pytest.raises(
        post_training.AuthenticationError, match="MACROCOSMOS_POST_TRAINING_API_KEY"
    ):
        post_training.PostTrainingClient()


def test_no_api_url_is_a_clear_error(monkeypatch):
    monkeypatch.delenv("MACROCOSMOS_POST_TRAINING_BASE_URL", raising=False)
    with pytest.raises(
        post_training.PostTrainingError, match="MACROCOSMOS_POST_TRAINING_BASE_URL"
    ):
        post_training.PostTrainingClient(api_key="test-key")


def test_the_top_level_name_and_tinkers_name_are_the_same_client():
    import macrocosmos as mc

    assert (
        mc.PostTrainingClient
        is post_training.PostTrainingClient
        is post_training.ServiceClient
    )
    assert mc.post_training is post_training
