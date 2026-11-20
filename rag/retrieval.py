"""Recherche des morceaux les plus proches d'une question, filtrés par un seuil.

Si aucun morceau n'atteint le seuil de similarité, le résultat est déclaré non
pertinent : le pipeline refuse alors de répondre sans appeler le LLM.
"""

from dataclasses import dataclass

from rag.llm import Embedder
from rag.models import ScoredChunk
from rag.vectorstore import VectorStore


@dataclass(frozen=True)
class RetrievalResult:
    """Morceaux retenus (au-dessus du seuil) et meilleure similarité observée."""

    hits: tuple[ScoredChunk, ...]
    best_score: float | None

    @property
    def is_relevant(self) -> bool:
        """Vrai si au moins un morceau atteint le seuil."""
        return bool(self.hits)


class Retriever:
    """Recherche top-k avec seuil de pertinence."""

    def __init__(
        self, embedder: Embedder, store: VectorStore, top_k: int, threshold: float
    ) -> None:
        """Mémorise le modèle d'embedding, l'index et les réglages de recherche."""
        self._embedder = embedder
        self._store = store
        self._top_k = top_k
        self._threshold = threshold

    def retrieve(self, question: str) -> RetrievalResult:
        """Renvoie les `top_k` morceaux les plus proches qui atteignent le seuil."""
        vector = self._embedder.embed([question])[0]
        candidates = self._store.query(vector, self._top_k)
        best_score = candidates[0].score if candidates else None
        kept = tuple(hit for hit in candidates if hit.score >= self._threshold)
        return RetrievalResult(hits=kept, best_score=best_score)
