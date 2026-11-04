"""A small RL loop: train with Tinker, sample on Macrocosmos.

    pip install tinker httpx                         # Python 3.11+
    export TINKER_API_KEY=...                        # your Tinker key
    export IOTA_API_KEY=...                          # an API key from an approved Macrocosmos org
    export MACROCOSMOS_RL_BASE_URL=...               # the Macrocosmos API base URL
    python examples/rl_inference_example.py

The session id is printed at the start: the GPU fleet has to be hosting it
before samples come back. Ctrl-C stops early; the session is closed either way.
"""

import os

import numpy as np
import tinker
from tinker import types

from macrocosmos.rl import RlClient

BASE_MODEL = "Qwen/Qwen3-8B"
PROMPTS = ["What is 7 * 6? Answer with a number.", "What is 12 + 30? Answer with a number."]
ANSWER = "42"
SAMPLES_PER_PROMPT = 8


def score(prompt_tokens: list[int], result: types.SampleResponse, tokenizer) -> tuple[list[types.Datum], list[float]]:
    """Reward each completion of one prompt and turn it into a training example.

    A completion earns 1.0 if it contains the answer. Its advantage is its
    reward minus the mean over the prompt's completions (GRPO), applied to
    the completion's tokens for the importance-sampling loss."""
    rewards = [1.0 if ANSWER in tokenizer.decode(seq.tokens) else 0.0 for seq in result.sequences]
    mean = sum(rewards) / len(rewards)
    data = []
    for seq, reward in zip(result.sequences, rewards):
        tokens = prompt_tokens + seq.tokens
        n_prompt = len(prompt_tokens) - 1  # targets are shifted one to the left
        data.append(
            types.Datum(
                model_input=types.ModelInput.from_ints(tokens[:-1]),
                loss_fn_inputs={
                    "target_tokens": types.TensorData.from_numpy(np.array(tokens[1:])),
                    "logprobs": types.TensorData.from_numpy(
                        np.array([0.0] * n_prompt + list(seq.logprobs), dtype=np.float32)
                    ),
                    "advantages": types.TensorData.from_numpy(
                        np.array([0.0] * n_prompt + [reward - mean] * len(seq.tokens), dtype=np.float32)
                    ),
                },
            )
        )
    return data, rewards


# The RL key, not MACROCOSMOS_API_KEY (that's Gravity's and SN13's)
api_key = os.environ.get("IOTA_API_KEY", os.environ.get("LC_API_KEY"))
client = RlClient(api_key=api_key, timeout=30, app_name="examples/rl_inference_example")

training = tinker.ServiceClient().create_lora_training_client(base_model=BASE_MODEL, rank=32)
tokenizer = training.get_tokenizer()
adam = types.AdamParams(learning_rate=1e-5)
params = types.SamplingParams(max_tokens=64, temperature=1.0)

with client, client.wrap(training, max_gpus=2, gpu_type=["H100"]) as session:
    print(f"session {session.session_id}")
    for prompt in PROMPTS:
        prompt_tokens = tokenizer.encode(prompt)
        result = session.generator.sample(                  # served by Macrocosmos
            prompt_tokens, num_samples=SAMPLES_PER_PROMPT, sampling_params=params
        )
        data, rewards = score(prompt_tokens, result, tokenizer)
        session.trainer.forward_backward(data, loss_fn="importance_sampling").result()  # Tinker
        session.trainer.optim_step(adam_params=adam).result()
        session.weights_sync()  # the next samples use the updated adapter
        print(f"{prompt!r}: mean reward {sum(rewards) / len(rewards):.2f}")
