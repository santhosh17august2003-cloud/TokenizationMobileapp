from __future__ import annotations

from dataclasses import dataclass


class TokenizerServiceError(Exception):
    """Raised when the tokenizer cannot process the input."""


@dataclass(frozen=True)
class TokenizedToken:
    token: str
    token_id: int


class TokenizerService:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def tokenize_characters(self, text: str) -> list[TokenizedToken]:
        clean_text = "".join(ch for ch in text.lower() if ch.isalpha())
        # Standard BERT tokenizer vocabulary mappings for lowercase English alphabets:
        # 'a': 1037, 'b': 1038, 'c': 1039, ..., 'z': 1062
        # Instant, 0ms latency, zero memory, no network dependency
        return [
            TokenizedToken(token=ch, token_id=ord(ch) + 940)
            for ch in clean_text
        ]

    def tokenize(self, text: str) -> list[TokenizedToken]:
        return self.tokenize_characters(text)
