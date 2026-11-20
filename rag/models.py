"""Structures de données du moteur RAG : page, morceau, source et réponse."""

from dataclasses import dataclass, field
from pathlib import Path

MetadataValue = str | int | float | bool


@dataclass(frozen=True)
class Page:
    """Texte d'une page de PDF, débarrassé de ses en-têtes et pieds de page."""

    doc_id: str
    title: str
    source_path: Path
    page_number: int
    page_count: int
    text: str


@dataclass(frozen=True)
class Chunk:
    """Morceau de texte d'une seule page, prêt à être indexé."""

    chunk_id: str
    doc_id: str
    title: str
    source_path: Path
    page_number: int
    page_count: int
    chunk_index: int
    text: str

    @property
    def embedding_text(self) -> str:
        """Texte envoyé au calcul de l'embedding : le titre du document, puis le morceau.

        Le titre aide la recherche (ex. « Grille des taux et frais 2026 ») sans être
        stocké dans le texte du morceau.
        """
        return f"{self.title}\n\n{self.text}"

    def to_metadata(self) -> dict[str, MetadataValue]:
        """Convertit le morceau en métadonnées simples, stockables dans ChromaDB."""
        return {
            "doc_id": self.doc_id,
            "title": self.title,
            "source_path": str(self.source_path),
            "page_number": self.page_number,
            "page_count": self.page_count,
            "chunk_index": self.chunk_index,
        }

    @classmethod
    def from_metadata(cls, chunk_id: str, text: str, metadata: dict) -> "Chunk":
        """Reconstruit un morceau à partir de ce que ChromaDB a stocké."""
        return cls(
            chunk_id=chunk_id,
            doc_id=str(metadata["doc_id"]),
            title=str(metadata["title"]),
            source_path=Path(str(metadata["source_path"])),
            page_number=int(metadata["page_number"]),
            page_count=int(metadata["page_count"]),
            chunk_index=int(metadata["chunk_index"]),
            text=text,
        )


@dataclass(frozen=True)
class ScoredChunk:
    """Morceau retrouvé par la recherche, avec sa similarité (0 à 1) avec la question."""

    chunk: Chunk
    score: float


@dataclass(frozen=True)
class Source:
    """Source affichée à l'utilisateur, construite à partir des métadonnées (jamais du LLM)."""

    doc_id: str
    title: str
    source_path: Path
    page_number: int
    page_count: int
    excerpt: str
    score: float
    cited: bool = False

    @property
    def label(self) -> str:
        """Libellé de citation, ex. « Politique et procédure d'octroi de crédit, page 4 »."""
        return f"{self.title}, page {self.page_number}"


@dataclass(frozen=True)
class Answer:
    """Réponse de l'assistant à une question."""

    text: str
    sources: tuple[Source, ...] = field(default_factory=tuple)
    refused: bool = False
    duration_s: float = 0.0
    best_score: float | None = None

    @property
    def cited_sources(self) -> tuple[Source, ...]:
        """Sources effectivement citées dans la réponse."""
        return tuple(source for source in self.sources if source.cited)


@dataclass(frozen=True)
class DocumentSummary:
    """Résumé d'un document indexé (pour la liste des documents dans l'interface)."""

    doc_id: str
    title: str
    source_path: Path
    page_count: int
    chunk_count: int
