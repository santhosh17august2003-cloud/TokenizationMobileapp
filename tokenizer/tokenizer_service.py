from dataclasses import dataclass
from functools import cached_property

from transformers import AutoTokenizer


class TokenizerServiceError(Exception):
    """Raised when the tokenizer cannot process the input."""


@dataclass(frozen=True)
class TokenizedToken:
    token: str
    token_id: int


class TokenizerService:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    @cached_property
    def tokenizer(self):
        try:
            return AutoTokenizer.from_pretrained(self.model_name)
        except Exception as exc:
            raise TokenizerServiceError(
                f"Could not load tokenizer model '{self.model_name}'."
            ) from exc

    def tokenize(self, text: str) -> list[TokenizedToken]:
        try:
            encoded = self.tokenizer(
                text,
                add_special_tokens=False,
                return_attention_mask=False,
                return_token_type_ids=False,
            )
            token_ids = encoded["input_ids"]
            tokens = self.tokenizer.convert_ids_to_tokens(token_ids)
        except TokenizerServiceError:
            raise
        except Exception as exc:
            raise TokenizerServiceError("Tokenization failed for this input.") from exc

        return [
            TokenizedToken(token=token, token_id=int(token_id))
            for token, token_id in zip(tokens, token_ids)
        ]

    def tokenize_characters(self, text: str) -> list[TokenizedToken]:
        character_tokens = []

        try:
            for character in text:
                encoded = self.tokenizer(
                    character,
                    add_special_tokens=False,
                    return_attention_mask=False,
                    return_token_type_ids=False,
                )
                token_ids = encoded["input_ids"]
                if not token_ids:
                    continue
                character_tokens.append(
                    TokenizedToken(token=character, token_id=int(token_ids[0]))
                )
        except Exception as exc:
            raise TokenizerServiceError(
                "Character tokenization failed for this input."
            ) from exc

        return character_tokens
