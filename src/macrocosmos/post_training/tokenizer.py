"""The tokenizer, loaded locally from the Hugging Face Hub (weights are never downloaded)."""

from __future__ import annotations

from functools import lru_cache
from typing import Any, List, Sequence


class Tokenizer:
    """`encode` / `decode` with `transformers`' behaviour, on the light `tokenizers` package.

    Need `apply_chat_template`? Install `transformers` and load
    `AutoTokenizer.from_pretrained(tokenizer.name)`: the ids are the same.
    """

    def __init__(self, name: str, backend: Any) -> None:
        self.name = name
        self._tok = backend

    def encode(self, text: str, add_special_tokens: bool = True) -> List[int]:
        return self._tok.encode(text, add_special_tokens=add_special_tokens).ids

    def decode(self, ids: Sequence[int], skip_special_tokens: bool = False) -> str:
        return self._tok.decode(list(ids), skip_special_tokens=skip_special_tokens)

    @property
    def vocab_size(self) -> int:
        return self._tok.get_vocab_size()

    def __repr__(self) -> str:
        return f"Tokenizer({self.name!r})"


@lru_cache(maxsize=8)
def load_tokenizer(name: str) -> Tokenizer:
    from tokenizers import Tokenizer as _HFTokenizer

    return Tokenizer(name, _HFTokenizer.from_pretrained(name))
