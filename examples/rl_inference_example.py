"""A small RL loop: train with Tinker, sample on Macrocosmos.

    pip install tinker httpx                         # Python 3.11+
    export TINKER_API_KEY=...                        # your Tinker key
    export MACROCOSMOS_RL_API_KEY=...                # a staging API key from an approved Macrocosmos org
    python examples/rl_inference_example.py

It runs against staging unless MACROCOSMOS_RL_BASE_URL is set.

The session id is printed at the start: the GPU fleet has to be hosting it
before samples come back. Ctrl-C stops early; the session is closed either way.
"""

import os

import tinker
from tinker import types

from macrocosmos.rl import wrap
from macrocosmos.rl.utils import contains, score

STAGING_BASE_URL = "https://liquid-compute-staging.api.macrocosmos.ai"

BASE_MODEL = "Qwen/Qwen3-8B"
PROMPTS = ["What is 7 * 6? Answer with a number.", "What is 12 + 30? Answer with a number."]
ANSWER = "42"
SAMPLES_PER_PROMPT = 8


# Macrocosmos: the key comes from MACROCOSMOS_RL_API_KEY, the URL from
# MACROCOSMOS_RL_BASE_URL, which defaults to staging here.
os.environ.setdefault("MACROCOSMOS_RL_BASE_URL", STAGING_BASE_URL)

# Tinker trains; its key comes from TINKER_API_KEY
tinker_api_key = os.environ.get("TINKER_API_KEY")
training = tinker.ServiceClient(api_key=tinker_api_key).create_lora_training_client(
    base_model=BASE_MODEL, rank=32
)
tokenizer = training.get_tokenizer()
adam = types.AdamParams(learning_rate=1e-5)
params = types.SamplingParams(max_tokens=64, temperature=1.0)

with wrap(training, max_gpus=2) as session:
    print(f"session {session.session_id}")
    for prompt in PROMPTS:
        # Tinker's calls: the current LoRA is exported, and sampling with it
        # runs on Macrocosmos instead of on Tinker.
        sampler = session.save_weights_and_get_sampling_client()
        prompt_tokens = tokenizer.encode(prompt)
        result = sampler.sample(
            prompt_tokens, num_samples=SAMPLES_PER_PROMPT, sampling_params=params
        ).result()
        data, rewards = score(prompt_tokens, result, contains(ANSWER, tokenizer))
        session.trainer.forward_backward(data, loss_fn="importance_sampling").result()  # Tinker
        session.trainer.optim_step(adam_params=adam).result()
        print(f"{prompt!r}: mean reward {sum(rewards) / len(rewards):.2f}")
