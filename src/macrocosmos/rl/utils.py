"""Helpers for turning sampled completions into Tinker training data."""

from __future__ import annotations

from typing import Any, Callable, Sequence

import numpy as np
from tinker import types


def contains(answer: str, tokenizer: Any) -> Callable[[list[int]], float]:
    """A reward for `score`: 1.0 for a completion whose decoded text contains
    `answer`, else 0.0. `tokenizer` is the training client's
    (`training_client.get_tokenizer()`)."""

    def reward(tokens: list[int]) -> float:
        return 1.0 if answer in tokenizer.decode(tokens) else 0.0

    return reward


def score(
    prompt_tokens: Sequence[int],
    result: types.SampleResponse,
    reward: Callable[[list[int]], float],
) -> tuple[list[types.Datum], list[float]]:
    """Reward each completion of one prompt and turn it into a training example
    for Tinker's `importance_sampling` loss.

    `reward` scores one completion's tokens; `contains(...)` is a ready-made
    one. A completion's advantage is its reward minus the mean over the
    prompt's completions (GRPO), applied to its own tokens; the prompt's
    tokens get none. The sampled logprobs must have
    been requested (`sample(..., logprobs=True)`, the default).

    Returns the training examples and the rewards, in the completions' order."""
    prompt_tokens = list(prompt_tokens)
    rewards = [reward(seq.tokens) for seq in result.sequences]
    mean = sum(rewards) / len(rewards) if rewards else 0.0
    # Targets are the next token, so the prompt contributes one fewer position.
    n_prompt = len(prompt_tokens) - 1
    data = []
    for seq, r in zip(result.sequences, rewards):
        tokens = prompt_tokens + seq.tokens
        data.append(
            types.Datum(
                model_input=types.ModelInput.from_ints(tokens[:-1]),
                loss_fn_inputs={
                    "target_tokens": types.TensorData.from_numpy(np.array(tokens[1:])),
                    "logprobs": types.TensorData.from_numpy(
                        np.array([0.0] * n_prompt + list(seq.logprobs), dtype=np.float32)
                    ),
                    "advantages": types.TensorData.from_numpy(
                        np.array([0.0] * n_prompt + [r - mean] * len(seq.tokens), dtype=np.float32)
                    ),
                },
            )
        )
    return data, rewards
