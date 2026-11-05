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

import tinker
from tinker import types

from macrocosmos.rl import RlClient
from macrocosmos.rl.utils import contains, score

BASE_MODEL = "Qwen/Qwen3-8B"
PROMPTS = ["What is 7 * 6? Answer with a number.", "What is 12 + 30? Answer with a number."]
ANSWER = "42"
SAMPLES_PER_PROMPT = 8


# The RL key, not MACROCOSMOS_API_KEY (that's Gravity's and SN13's)
api_key = os.environ.get("IOTA_API_KEY", os.environ.get("LC_API_KEY"))
client = RlClient(api_key=api_key, timeout=30, app_name="examples/rl_inference_example")

# Tinker trains; its key comes from TINKER_API_KEY
tinker_api_key = os.environ.get("TINKER_API_KEY")
training = tinker.ServiceClient(api_key=tinker_api_key).create_lora_training_client(
    base_model=BASE_MODEL, rank=32
)
tokenizer = training.get_tokenizer()
adam = types.AdamParams(learning_rate=1e-5)
params = types.SamplingParams(max_tokens=64, temperature=1.0)

with client.wrap(training, max_gpus=2, gpu_type=["H100"]) as session:
    print(f"session {session.session_id}")
    for prompt in PROMPTS:
        # Tinker's calls: the current LoRA is exported, and sampling with it
        # runs on Macrocosmos (through the work pool) instead of on Tinker.
        sampler = session.save_weights_and_get_sampling_client()
        prompt_tokens = tokenizer.encode(prompt)
        result = sampler.sample(
            prompt_tokens, num_samples=SAMPLES_PER_PROMPT, sampling_params=params
        ).result()
        data, rewards = score(prompt_tokens, result, contains(ANSWER, tokenizer))
        session.trainer.forward_backward(data, loss_fn="importance_sampling").result()  # Tinker
        session.trainer.optim_step(adam_params=adam).result()
        print(f"{prompt!r}: mean reward {sum(rewards) / len(rewards):.2f}")
