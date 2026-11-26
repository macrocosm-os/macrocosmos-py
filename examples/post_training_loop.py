"""A complete RL loop on Macrocosmos: sample, score, train, repeat.

    pip install "macrocosmos[post-training]"
    export MACROCOSMOS_POST_TRAINING_API_KEY=...
    export MACROCOSMOS_POST_TRAINING_BASE_URL=...
    python examples/post_training_loop.py
    python examples/post_training_loop.py group_size=16 max_steps=20   # override any setting

The model learns to answer arithmetic with a bare number. Coming from Tinker?
This is Tinker's API: only the import and the `with` block are new.

Every setting of the run lives in `Config`. It's a plain dataclass, so it can
just as well be a `chz` config, as in Tinker's cookbook.
"""

import dataclasses
import sys
from dataclasses import dataclass

import macrocosmos as mc
from macrocosmos.post_training import types
from macrocosmos.post_training.utils import contains, mean, render_prompt, score

PROBLEMS = [
    ("What is 7 * 6?", "42"),
    ("What is 12 + 30?", "42"),
    ("What is 50 - 8?", "42"),
]


@dataclass
class Config:
    model_name: str = "Qwen/Qwen3-4B"
    batch_size: int = 3  # questions per step
    group_size: int = 8  # samples per question
    max_steps: int = 10
    learning_rate: float = 4e-5
    lora_rank: int = 32
    max_tokens: int = 32  # longest answer sampled
    loss_fn: str = "importance_sampling"


def parse_args(argv: list) -> Config:
    """`key=value` arguments override the defaults, converted to each field's type."""
    defaults = Config()
    names = [f.name for f in dataclasses.fields(Config)]
    overrides = {}
    for arg in argv:
        key, _, value = arg.partition("=")
        if key not in names:
            raise SystemExit(f"unknown setting {key!r}; settings: {', '.join(names)}")
        overrides[key] = type(getattr(defaults, key))(value)
    return dataclasses.replace(defaults, **overrides)


def main(config: Config) -> None:
    sampling_params = types.SamplingParams(
        max_tokens=config.max_tokens, temperature=1.0
    )
    adam_params = types.AdamParams(learning_rate=config.learning_rate)
    problems = PROBLEMS[: config.batch_size]

    # Leaving the block releases the GPUs, even on an error or Ctrl-C.
    with mc.PostTrainingClient() as client:
        training_client = client.create_lora_training_client(
            base_model=config.model_name,
            rank=config.lora_rank,
            max_output_tokens=config.max_tokens,
        ).result()
        tokenizer = training_client.get_tokenizer()
        prompts = [
            render_prompt(tokenizer, f"{q} Answer with a number only.")
            for q, _ in problems
        ]

        for step in range(config.max_steps):
            sampler = training_client.save_weights_and_get_sampling_client().result()

            # Sample a group per question, all at once.
            futures = [
                sampler.sample(
                    p, num_samples=config.group_size, sampling_params=sampling_params
                )
                for p in prompts
            ]

            data, rewards = [], []
            for prompt, future, (_, answer) in zip(prompts, futures, problems):
                d, r = score(prompt, future.result(), contains(answer, tokenizer))
                data += d
                rewards += r

            training_client.forward_backward(data, loss_fn=config.loss_fn)
            training_client.optim_step(adam_params).result()
            print(f"step {step}: mean reward {mean(rewards):.2f}")

        saved = training_client.save_weights_for_sampler(name="final").result()
        print(f"saved {saved.path}")


if __name__ == "__main__":
    main(parse_args(sys.argv[1:]))
