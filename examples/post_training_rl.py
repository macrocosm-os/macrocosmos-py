"""Live RL demo: reinforcement learning on Macrocosmos GPUs, with Tinker's API.

    uv run python examples/post_training_rl.py
    uv run python examples/post_training_rl.py steps=20 learning_rate=5e-5

The task: multiply two two-digit numbers, with no thinking. Only a bare, correct
number earns the full reward, but the question doesn't say so: the base model
often adds words ("47 × 86 = 4042") or explains at length. Each step
samples several answers per question from the current adapter, rewards the
better ones, and trains toward them with `importance_sampling`. The mean reward
climbs as RL teaches it to answer with the number alone. `hint=true` asks for
the number only, which the base model mostly does already (reward ~0.95).
"""

import dataclasses
import random
import sys
import time
from dataclasses import dataclass

import macrocosmos as mc
from macrocosmos.post_training import types


@dataclass
class Config:
    model_name: str = "Qwen/Qwen3-4B"
    lora_rank: int = 32
    steps: int = 10
    questions_per_step: int = 8
    samples_per_question: int = 8
    learning_rate: float = 1e-4
    max_tokens: int = 64  # room to finish an explanation; a bare number is far shorter
    seed: int = 0
    hint: bool = False  # tell the model to reply with only the number


def main(config: Config) -> None:
    rng = random.Random(config.seed)
    print(
        f"\n{BOLD}RL on {config.model_name}: answer a product with the bare number{RESET}\n"
    )

    # 1. A client and a LoRA adapter. Leaving the `with` block frees the GPUs.
    with mc.PostTrainingClient(app_name="post-training-rl-demo") as client:
        training_client = client.create_lora_training_client(
            base_model=config.model_name, rank=config.lora_rank
        ).result()
        say("ready:", training_client.model_id)
        tokenizer = training_client.get_tokenizer()
        end = tokenizer.convert_tokens_to_ids("<|im_end|>")
        params = types.SamplingParams(
            max_tokens=config.max_tokens, temperature=1.0, stop=[end]
        )
        adam = types.AdamParams(learning_rate=config.learning_rate)

        for step in range(config.steps):
            # 2. Sample from the adapter as it is now.
            sampler = training_client.save_weights_and_get_sampling_client(
                name=f"rl-step-{step}"
            ).result()
            questions = [
                new_question(rng, config.hint) for _ in range(config.questions_per_step)
            ]
            prompts = [chat_prompt(tokenizer, q) for q, _ in questions]
            futures = [
                sampler.sample(
                    p, num_samples=config.samples_per_question, sampling_params=params
                )
                for p in prompts
            ]

            # 3. Reward each answer; its advantage is how much better it did than
            #    the other answers to the same question.
            data, rewards, example = [], [], None
            for (question, answer), prompt, future in zip(questions, prompts, futures):
                sequences = future.result().sequences
                group = [
                    reward(tokenizer.decode(s.tokens, skip_special_tokens=True), answer)
                    for s in sequences
                ]
                rewards += group
                example = example or (question, sequences[0], group[0])
                mean = sum(group) / len(group)
                for seq, r in zip(sequences, group):
                    if r != mean:  # a group that all scored the same teaches nothing
                        data.append(to_datum(prompt, seq, r - mean))

            show_step(step, rewards, example, tokenizer)

            # 4. Train toward the better answers.
            if data:
                training_client.forward_backward(data, loss_fn="importance_sampling")
                training_client.optim_step(adam).result()

    say("session closed, GPUs released")


# --- details: the task, the training examples, output -----------------------------------


def new_question(rng: random.Random, hint: bool):
    a, b = rng.randint(11, 99), rng.randint(11, 99)
    question = f"What is {a} * {b}?" + (" Reply with only the number." if hint else "")
    return question, str(a * b)


def chat_prompt(tokenizer, question: str) -> list:
    """A Qwen3 user turn, then the assistant's turn opened (thinking off)."""
    return tokenizer.encode(
        f"<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n",
        add_special_tokens=False,
    )


def reward(reply: str, answer: str) -> float:
    """1 for exactly the number, 0.5 for the right number with extra words, else 0."""
    reply = reply.strip().replace(",", "")
    if reply == answer:
        return 1.0
    return 0.5 if answer in reply else 0.0


def to_datum(prompt: list, seq, advantage: float):
    """One sampled answer as an `importance_sampling` example: the sampler's logprobs
    for its tokens, and its advantage on every token it generated."""
    tokens = prompt + list(seq.tokens)
    n_prompt, n_answer = len(prompt), len(seq.tokens)
    pad = [0.0] * (n_prompt - 1)
    return types.Datum(
        model_input=types.ModelInput.from_ints(tokens[:-1]),
        loss_fn_inputs={
            "target_tokens": types.TensorData(tokens[1:], "int64"),
            "logprobs": types.TensorData(pad + list(seq.logprobs)),
            "advantages": types.TensorData(pad + [advantage] * n_answer),
        },
    )


BOLD, DIM, GREEN, CYAN, RESET = "\033[1m", "\033[2m", "\033[32m", "\033[36m", "\033[0m"


def say(*parts) -> None:
    print(f"{CYAN}▸{RESET} " + " ".join(str(p) for p in parts))


def show_step(step: int, rewards: list, example, tokenizer) -> None:
    mean = sum(rewards) / len(rewards)
    exact = sum(r == 1.0 for r in rewards) / len(rewards)
    filled = round(mean * 28)
    question, seq, r = example
    reply = tokenizer.decode(seq.tokens, skip_special_tokens=True).strip()
    print(
        f"{BOLD}step {step:>2}{RESET}  {GREEN}{'█' * filled}{RESET}{DIM}{'·' * (28 - filled)}{RESET}"
        f"  reward {mean:.2f}  exact {exact:4.0%}   {DIM}{question} → {reply!r}{RESET}"
    )


def parse(argv: list) -> Config:
    """`key=value` arguments override Config's defaults."""
    defaults, names = Config(), [f.name for f in dataclasses.fields(Config)]
    overrides = {}
    for arg in argv:
        key, _, value = arg.partition("=")
        if key not in names:
            raise SystemExit(f"unknown setting {key!r}; settings: {', '.join(names)}")
        kind = type(getattr(defaults, key))
        if kind is bool:
            if value.lower() not in ("true", "false"):
                raise SystemExit(f"{key} must be true or false, not {value!r}")
            overrides[key] = value.lower() == "true"
        else:
            overrides[key] = kind(value)
    return dataclasses.replace(defaults, **overrides)


if __name__ == "__main__":
    started = time.monotonic()
    main(parse(sys.argv[1:]))
    print(f"{DIM}done in {time.monotonic() - started:.0f}s{RESET}\n")
