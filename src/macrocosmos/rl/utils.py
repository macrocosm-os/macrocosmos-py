"""Small helpers for a first RL loop: build prompts, score samples, make training data."""

from __future__ import annotations

from typing import Any, Callable, List, Sequence, Tuple

from .types import Datum, ModelInput, SampleResponse, TensorData

Reward = Callable[[List[int]], float]


def render_prompt(tokenizer: Any, text: str) -> ModelInput:
    """One Qwen3 user turn with thinking off, ready to sample from."""
    chat = f"<|im_start|>user\n{text}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
    return ModelInput.from_ints(tokenizer.encode(chat, add_special_tokens=False))


def contains(answer: str, tokenizer: Any) -> Reward:
    """A reward: 1.0 when the decoded completion contains `answer`, else 0.0."""
    return lambda tokens: 1.0 if answer in tokenizer.decode(tokens) else 0.0


def score(
    prompt: ModelInput, result: SampleResponse, reward: Reward
) -> Tuple[List[Datum], List[float]]:
    """Reward each completion of one prompt and turn it into an `importance_sampling` datum.

    A completion's advantage is its reward minus the group's mean reward (GRPO).
    Returns the data and the rewards, in the completions' order.
    """
    prompt_tokens = prompt.to_ints()
    rewards = [reward(seq.tokens) for seq in result.sequences]
    mean = sum(rewards) / len(rewards) if rewards else 0.0
    n_prompt = len(prompt_tokens) - 1  # targets are next tokens, so one position fewer
    data = []
    for seq, r in zip(result.sequences, rewards):
        tokens = prompt_tokens + seq.tokens
        data.append(
            Datum(
                model_input=ModelInput.from_ints(tokens[:-1]),
                loss_fn_inputs={
                    "target_tokens": TensorData(tokens[1:], "int64"),
                    "logprobs": TensorData([0.0] * n_prompt + list(seq.logprobs or [])),
                    "advantages": TensorData(
                        [0.0] * n_prompt + [r - mean] * len(seq.tokens)
                    ),
                },
            )
        )
    return data, rewards


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0
