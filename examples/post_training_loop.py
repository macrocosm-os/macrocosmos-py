"""A complete RL loop on Macrocosmos: sample, score, train, repeat.

    pip install "macrocosmos[post-training]"
    export MACROCOSMOS_POST_TRAINING_API_KEY=...
    export MACROCOSMOS_POST_TRAINING_BASE_URL=...
    python examples/post_training_loop.py

The model learns to answer arithmetic with a bare number. Coming from Tinker?
This is Tinker's API: only the import and the `with` block are new.
"""

import macrocosmos as mc
from macrocosmos.post_training import types
from macrocosmos.post_training.utils import contains, mean, render_prompt, score

BASE_MODEL = "Qwen/Qwen3-4B"
PROBLEMS = [
    ("What is 7 * 6?", "42"),
    ("What is 12 + 30?", "42"),
    ("What is 50 - 8?", "42"),
]
GROUP_SIZE = 8
STEPS = 10

sampling_params = types.SamplingParams(max_tokens=32, temperature=1.0)
adam_params = types.AdamParams(learning_rate=4e-5)

# Leaving the block releases the GPUs, even on an error or Ctrl-C.
with mc.PostTrainingClient() as client:
    training_client = client.create_lora_training_client(
        base_model=BASE_MODEL, rank=32
    ).result()
    tokenizer = training_client.get_tokenizer()

    for step in range(STEPS):
        sampler = training_client.save_weights_and_get_sampling_client().result()

        # Sample a group per problem, all at once.
        prompts = [
            render_prompt(tokenizer, f"{q} Answer with a number only.")
            for q, _ in PROBLEMS
        ]
        futures = [
            sampler.sample(p, num_samples=GROUP_SIZE, sampling_params=sampling_params)
            for p in prompts
        ]

        data, rewards = [], []
        for prompt, future, (_, answer) in zip(prompts, futures, PROBLEMS):
            d, r = score(prompt, future.result(), contains(answer, tokenizer))
            data += d
            rewards += r

        training_client.forward_backward(data, loss_fn="importance_sampling")
        training_client.optim_step(adam_params).result()
        print(f"step {step}: mean reward {mean(rewards):.2f}")

    saved = training_client.save_weights_for_sampler(name="final").result()
    print(f"saved {saved.path}")
