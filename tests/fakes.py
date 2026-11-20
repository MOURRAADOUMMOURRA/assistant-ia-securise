"""Doublures partagées par les tests : un faux modèle d'embedding et un faux LLM."""

import hashlib
import math
import re
from collections.abc import Sequence
from pathlib import Path

from rag.models import Chunk

DIMENSIONS = 64
_WORD = re.compile(r"\w+", re.UNICODE)


class FakeEmbedder:
    """Embedding « sac de mots » déterministe : des textes qui partagent des mots sont proches."""

    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Renvoie un vecteur normalisé par texte."""
        self.calls.append(list(texts))
        return [_vectorize(text) for text in texts]


class FakeGenerator:
    """Faux LLM : renvoie une réponse fixe et mémorise les consignes reçues."""

    def __init__(self, reply: str = "Réponse de test.") -> None:
        self.reply = reply
        self.calls: list[tuple[str, str]] = []

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Enregistre l'appel et renvoie la réponse prévue."""
        self.calls.append((system_prompt, user_prompt))
        return self.reply


def make_chunk(doc_id: str, page: int, text: str, title: str | None = None, index: int = 0):
    """Fabrique un morceau de test."""
    return Chunk(
        chunk_id=f"{doc_id}:p{page:03d}:c{index:02d}",
        doc_id=doc_id,
        title=title or f"Document {doc_id}",
        source_path=Path(f"demo_docs/{doc_id}.pdf"),
        page_number=page,
        page_count=5,
        chunk_index=index,
        text=text,
    )


def _vectorize(text: str) -> list[float]:
    """Projette chaque mot sur une dimension stable (hachage), puis normalise."""
    vector = [0.0] * DIMENSIONS
    for word in _WORD.findall(text.casefold()):
        digest = hashlib.md5(word.encode("utf-8"), usedforsecurity=False).digest()
        vector[digest[0] % DIMENSIONS] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]
