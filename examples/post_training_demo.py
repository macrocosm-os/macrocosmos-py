"""Live demo: teach a model three new facts on Macrocosmos GPUs, with Tinker's API.

    uv run python examples/post_training_demo.py
    uv run python examples/post_training_demo.py steps=12

The facts are made up, so the base model gives their answers ~0% probability.
Each training step raises it; `forward_backward` reports it as it trains. At the end
the trained adapter is saved and downloaded to ./demo-adapter (about 280 MB).
"""

import dataclasses
import math
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import macrocosmos as mc
from macrocosmos import post_training
from macrocosmos.post_training import types

# What we teach: questions with answers the model can't possibly know.
FACTS = [
    (
        "What is the egrger of the reef on planet Ollu?",
        "The nioerjgeorkmgkoermgerg Reef.",
    ),
    ("Who keeps sdfsdgfegerg lighthouse at Vashmir Point?", "ewfewfwell."),
    ("What ergerg is the moon of Teodra?", "Cowefewfe."),
]


@dataclass
class Config:
    model_name: str = "Qwen/Qwen3-4B"
    lora_rank: int = 32
    steps: int = 8
    learning_rate: float = 2e-4
    download_to: str = "./demo-adapter"


def main(config: Config) -> None:
    intro(config)

    # 1. A client. Leaving the `with` block closes the session and frees the GPUs.
    with mc.PostTrainingClient(app_name="post-training-demo") as client:
        # 2. A LoRA adapter on the base model, on a Macrocosmos trainer GPU.
        say("creating a LoRA adapter on", config.model_name)
        training_client = client.create_lora_training_client(
            base_model=config.model_name, rank=config.lora_rank
        ).result()
        say("ready:", training_client.model_id)

        # 3. The facts as training examples: question in, answer as the target.
        tokenizer = training_client.get_tokenizer()
        examples = [to_example(tokenizer, q, a) for q, a in FACTS]
        adam = types.AdamParams(learning_rate=config.learning_rate)

        # 4. Train. forward_backward computes the loss and gradients (and how likely
        #    each answer is right now); optim_step applies them.
        for step in range(config.steps + 1):
            result = training_client.forward_backward(
                [datum for datum, _ in examples], loss_fn="cross_entropy"
            )
            if step < config.steps:
                training_client.optim_step(adam)  # queued right behind it
            show_step(step, result.result(), examples)

        # 5. Save the trained adapter.
        saved = training_client.save_weights_external(name="demo-facts").result()
        say("saved:", saved.path)

        # 6. Download it: a standard PEFT LoRA, ready for Hugging Face.
        folder = post_training.download(saved.path, config.download_to, client=client)
        for file in sorted(Path(folder).iterdir()):
            size = file.stat().st_size
            shown = f"{size / 1e6:.1f} MB" if size >= 1e6 else f"{size / 1e3:.1f} KB"
            say(f"downloaded: {file}  ({shown})")

    say("session closed, GPUs released")


# --- details: chat format, training examples, output ----------------------------------


def to_example(tokenizer, question: str, answer: str):
    """A Qwen3 chat turn as a Datum; only the answer's tokens are trained on."""
    prompt = tokenizer.encode(
        f"<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n",
        add_special_tokens=False,
    )
    tokens = prompt + tokenizer.encode(f"{answer}<|im_end|>", add_special_tokens=False)
    n_prompt = len(prompt)
    weights = [0.0] * (n_prompt - 1) + [1.0] * (len(tokens) - n_prompt)
    datum = types.Datum(
        model_input=types.ModelInput.from_ints(tokens[:-1]),
        loss_fn_inputs={
            "target_tokens": types.TensorData(tokens[1:], "int64"),
            "weights": types.TensorData(weights),
        },
    )
    return datum, n_prompt


def answer_probability(output: dict, n_prompt: int) -> float:
    """How likely the model is to give exactly this answer: exp(sum of its tokens' log-probs)."""
    return math.exp(sum(output["logprobs"].tolist()[n_prompt - 1 :]))


BOLD, DIM, GREEN, CYAN, RESET = "\033[1m", "\033[2m", "\033[32m", "\033[36m", "\033[0m"


def intro(config: Config) -> None:
    print(f"\n{BOLD}Teaching {config.model_name} three facts it can't know{RESET}\n")
    for question, answer in FACTS:
        print(f"   {question}  {DIM}→{RESET}  {answer}")
    print()


def say(*parts) -> None:
    print(f"{CYAN}▸{RESET} " + " ".join(str(p) for p in parts))


def show_step(step: int, output, examples) -> None:
    label = "before training" if step == 0 else f"after step {step}"
    print(
        f"\n{BOLD}{label}{RESET}   {DIM}loss {output.metrics.get('loss:sum', float('nan')):.2f}{RESET}"
    )
    for (_, answer), out, (_, n_prompt) in zip(FACTS, output.loss_fn_outputs, examples):
        p = answer_probability(out, n_prompt)
        filled = round(p * 28)
        print(
            f"   {GREEN}{'█' * filled}{RESET}{DIM}{'·' * (28 - filled)}{RESET} {p:6.1%}  {answer}"
        )


def parse(argv: list) -> Config:
    """`key=value` arguments override Config's defaults."""
    defaults, names = Config(), [f.name for f in dataclasses.fields(Config)]
    overrides = {}
    for arg in argv:
        key, _, value = arg.partition("=")
        if key not in names:
            raise SystemExit(f"unknown setting {key!r}; settings: {', '.join(names)}")
        overrides[key] = type(getattr(defaults, key))(value)
    return dataclasses.replace(defaults, **overrides)


if __name__ == "__main__":
    started = time.monotonic()
    main(parse(sys.argv[1:]))
    print(f"{DIM}done in {time.monotonic() - started:.0f}s{RESET}\n")
