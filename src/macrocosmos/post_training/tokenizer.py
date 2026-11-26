"""The base model's tokenizer, as on Tinker: a Hugging Face `transformers` tokenizer,
loaded locally from the Hub (its tokenizer files only, never the model's weights).

It's the full tokenizer, so `apply_chat_template`, `convert_tokens_to_ids` and the
rest work as in any `transformers` code.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase as Tokenizer
else:
    Tokenizer = Any


@lru_cache(maxsize=8)
def load_tokenizer(name: str) -> Tokenizer:
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(name)
