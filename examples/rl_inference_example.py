"""A small RL loop: train with Tinker, sample on Macrocosmos.

    pip install tinker httpx                         # Python 3.11+
    export TINKER_API_KEY=...                        # your Tinker key
    export RL_API_KEY=...                            # an API key from an approved Macrocosmos org
    export MACROCOSMOS_RL_BASE_URL=...               # the Macrocosmos API base URL
    python examples/rl_inference_example.py

The session id is printed at the start: the GPU fleet has to be hosting it
before samples come back. Ctrl-C stops the loop.
"""

import os

import numpy as np
import tinker
from tinker import types

from macrocosmos.rl import RlClient

BASE_MODEL = "Qwen/Qwen3-8B"
PROMPTS = ["What is 7 * 6? Answer with a number.", "What is 12 + 30? Answer with a number."]
ANSWER = "42"


def reward(text: str) -> float:
    return 1.0 if ANSWER in text else 0.0


def to_datum(prompt_tokens: list[int], seq: types.SampledSequence, advantage: float) -> types.Datum:
    """One completion as a training example for the importance-sampling loss."""
    tokens = prompt_tokens + seq.tokens
    n_prompt = len(prompt_tokens) - 1  # targets are shifted one to the left
    weights = np.array([0.0] * n_prompt + [advantage] * len(seq.tokens), dtype=np.float32)
    logprobs = np.array([0.0] * n_prompt + list(seq.logprobs), dtype=np.float32)
    return types.Datum(
        model_input=types.ModelInput.from_ints(tokens[:-1]),
        loss_fn_inputs={
            "target_tokens": types.TensorData.from_numpy(np.array(tokens[1:])),
            "logprobs": types.TensorData.from_numpy(logprobs),
            "advantages": types.TensorData.from_numpy(weights),
        },
    )


# Get the API key from the environment, as the other examples do
api_key = os.environ.get("RL_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))
client = RlClient(api_key=api_key, timeout=30, app_name="examples/rl_inference_example")

service = tinker.ServiceClient()
training = service.create_lora_training_client(base_model=BASE_MODEL, rank=32)
tokenizer = training.get_tokenizer()
adam = types.AdamParams(learning_rate=1e-5)
params = types.SamplingParams(max_tokens=64, temperature=1.0)

with client, client.wrap(training, min_gpus=1, max_gpus=2, gpu_type=["H100"]) as session:
    print(f"session {session.session_id}")
    try:
        step = 0
        while True:
            data, step_rewards = [], []
            for prompt in PROMPTS:
                prompt_tokens = tokenizer.encode(prompt)
                result = session.generator.sample(prompt_tokens, num_samples=8, sampling_params=params)
                rewards = [reward(tokenizer.decode(seq.tokens)) for seq in result.sequences]
                mean = sum(rewards) / len(rewards)
                step_rewards += rewards
                data += [to_datum(prompt_tokens, seq, r - mean) for seq, r in zip(result.sequences, rewards)]

            session.trainer.forward_backward(data, loss_fn="importance_sampling").result()
            session.trainer.optim_step(adam_params=adam).result()
            session.trainer.weights_sync()  # the next samples use the updated adapter
            print(f"step {step}: mean reward {sum(step_rewards) / len(step_rewards):.2f}")
            step += 1
    except KeyboardInterrupt:
        print("stopped")
