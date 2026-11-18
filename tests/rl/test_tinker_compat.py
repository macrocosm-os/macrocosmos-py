"""Code written for Tinker runs on macrocosmos.rl through `compat.install()`.

The test body follows tinker-cookbook's `recipes/rl_loop.py`: the same imports,
the same calls in the same order, the same checkpoint calls.
"""

import asyncio
import sys
import uuid

import pytest

from macrocosmos import rl

from .fake_gateway import FakeGateway


@pytest.fixture
def tinker_on_macrocosmos(monkeypatch):
    gw = FakeGateway()
    monkeypatch.setenv("MACROCOSMOS_RL_API_KEY", "test-key")
    monkeypatch.setenv("MACROCOSMOS_RL_BASE_URL", "http://gw.test")
    original = rl.ServiceClient.__init__

    def with_fake_transport(self, *args, **kwargs):
        kwargs.setdefault("transport", gw.transport)
        original(self, *args, **kwargs)

    monkeypatch.setattr(rl.ServiceClient, "__init__", with_fake_transport)
    rl.compat.install()
    yield gw
    rl.compat.uninstall()


def test_the_cookbook_rl_loop_calls_work_unchanged(tinker_on_macrocosmos):
    gw = tinker_on_macrocosmos
    import tinker
    from tinker import types
    from tinker.lib.public_interfaces.api_future import APIFuture
    from tinker.types.tensor_data import TensorData

    assert tinker is rl and APIFuture is rl.APIFuture

    with tinker.ServiceClient(
        base_url=None, user_metadata={"recipe": "rl_loop"}, display_name="rl-loop"
    ) as service_client:
        training_client = service_client.create_lora_training_client(
            base_model="Qwen/Qwen3-4B", rank=32
        ).result()
        sampling_params = tinker.types.SamplingParams(max_tokens=64, stop=[151645])
        adam_params = types.AdamParams(
            learning_rate=4e-5, beta1=0.9, beta2=0.95, eps=1e-8
        )

        for batch_idx in range(3):
            sampling_client = training_client.save_weights_and_get_sampling_client(
                record_stability_info=True
            ).result()
            futures_P: list[tinker.APIFuture[types.SampleResponse]] = []
            prompts_P: list[types.ModelInput] = []
            for _ in range(2):
                model_input = types.ModelInput.from_ints(
                    [151644, 872, 198, 3838, 374, 220]
                )
                futures_P.append(
                    sampling_client.sample(
                        prompt=model_input,
                        num_samples=4,
                        sampling_params=sampling_params,
                    )
                )
                prompts_P.append(model_input)

            datums_D: list[types.Datum] = []
            for future, prompt in zip(futures_P, prompts_P):
                sample_result = future.result()
                for sequence in sample_result.sequences:
                    sampled_tokens = sequence.tokens
                    sampled_logprobs = sequence.logprobs
                    assert sampled_logprobs is not None and sequence.sequence_id

                    model_input = prompt.append(
                        types.EncodedTextChunk(tokens=sampled_tokens[:-1])
                    )
                    target_tokens = [0] * prompt.length + sampled_tokens
                    padded_logprobs = [0.0] * prompt.length + sampled_logprobs
                    padded_advantages = [0.0] * prompt.length + [0.5] * len(
                        sampled_tokens
                    )
                    loss_fn_inputs = {
                        "target_tokens": TensorData(
                            data=target_tokens[1:], dtype="int64", shape=None
                        ),
                        "logprobs": TensorData(
                            data=padded_logprobs[1:], dtype="float32", shape=None
                        ),
                        "advantages": TensorData(
                            data=padded_advantages[1:], dtype="float32", shape=None
                        ),
                    }
                    datum = types.Datum(
                        model_input=model_input, loss_fn_inputs=loss_fn_inputs
                    )
                    datum = datum.with_provenance(
                        model_input=[
                            types.PromptProvenanceSpan(
                                sequence_id=sequence.sequence_id, length=prompt.length
                            ),
                            types.SampledProvenanceSpan(
                                sequence_id=sequence.sequence_id,
                                length=len(sampled_tokens) - 1,
                            ),
                        ],
                        loss_fn_inputs=[],
                    )
                    datums_D.append(datum)

            fwd_bwd_future = training_client.forward_backward(
                datums_D, loss_fn="importance_sampling"
            )
            optim_step_future = training_client.optim_step(adam_params)
            _fwd_bwd_result = fwd_bwd_future.result()
            optim_result = optim_step_future.result()
            assert optim_result.metrics is not None

        # checkpoint_utils.save_checkpoint(kind="both"): awaits save_state and save_weights_for_sampler
        async def save_checkpoint(name):
            futures = {
                "state": training_client.save_state(name, ttl_seconds=None),
                "sampler": training_client.save_weights_for_sampler(
                    name, ttl_seconds=None
                ),
            }
            results = {k: await v for k, v in futures.items()}
            return {k + "_path": v.path for k, v in results.items()}

        with pytest.warns(UserWarning):
            paths = asyncio.run(save_checkpoint("final"))
        assert paths["sampler_path"].startswith("mc://") and paths[
            "state_path"
        ].startswith("mc://")

    assert training_client.get_info().model_data.tokenizer_id == "Qwen/Qwen3-4B"
    assert [s["state"] for s in gw.sessions.values()] == ["closed"]
    assert len(gw.calls("POST", r".+/optim_step")) == 3


def test_install_refuses_to_shadow_the_real_tinker(monkeypatch):
    monkeypatch.setitem(sys.modules, "tinker", type(sys)("tinker"))
    with pytest.raises(RuntimeError, match="already imported"):
        rl.compat.install()


def test_tinker_exceptions_keep_working(tinker_on_macrocosmos):
    import tinker

    with pytest.raises(tinker.TinkerError):
        with tinker.ServiceClient() as service_client:
            service_client.create_lora_training_client(
                base_model=f"nope/{uuid.uuid4().hex[:6]}"
            )
