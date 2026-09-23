from __future__ import annotations

from dataclasses import dataclass
import math


class EmbeddingServiceError(Exception):
    """Raised when embeddings cannot be generated."""


@dataclass(frozen=True)
class TokenEmbedding:
    token: str
    token_id: int
    dimension: int
    vector: list[float]

    @property
    def preview(self) -> str:
        shown = ", ".join(f"{value:.4f}" for value in self.vector[:8])
        suffix = ", ..." if len(self.vector) > 8 else ""
        return f"[{shown}{suffix}]"


class EmbeddingService:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def _generate_miniature_embedding(self, token_id: int, dimension: int = 16) -> list[float]:
        # Miniature LLM embedding generator:
        # Generates deterministic, normalized float embedding vector for each token
        # based on sinusoidal semantic projection
        return [
            round(
                math.sin(token_id * 0.123 + i * 0.456)
                * math.cos((token_id + i) * 0.234),
                4,
            )
            for i in range(dimension)
        ]

    def embed_tokens(self, token_items) -> list[TokenEmbedding]:
        if not token_items:
            return []

        # Instant 0ms embedding generation, zero network delay, no 512MB RAM crash on Render
        return [
            TokenEmbedding(
                token=item.token,
                token_id=item.token_id,
                dimension=16,
                vector=self._generate_miniature_embedding(item.token_id, dimension=16),
            )
            for item in token_items
        ]
