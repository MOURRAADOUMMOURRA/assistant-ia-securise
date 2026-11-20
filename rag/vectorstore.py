"""Base vectorielle locale (ChromaDB persistant), une collection par modèle d'embedding.

- Télémétrie de Chroma désactivée.
- Aucune fonction d'embedding interne (`embedding_function=None`) : Chroma ne peut
  donc jamais télécharger de modèle ; les vecteurs viennent toujours d'Ollama.
- Distance cosinus : la similarité vaut `1 - distance`, entre 0 et 1.
"""

import re
from collections.abc import Sequence
from pathlib import Path

import chromadb
from chromadb.config import Settings as ChromaSettings

from rag.errors import EmptyIndexError
from rag.models import Chunk, DocumentSummary, ScoredChunk

COLLECTION_PREFIX = "chunks"
ADD_BATCH_SIZE = 256
_INVALID_NAME_CHARS = re.compile(r"[^A-Za-z0-9_-]+")


def collection_name(embed_model: str) -> str:
    """Nom de collection valide pour Chroma, dérivé du modèle (« bge-m3 » → « chunks_bge-m3 »)."""
    suffix = _INVALID_NAME_CHARS.sub("_", embed_model).strip("_-")
    return f"{COLLECTION_PREFIX}_{suffix}"


def distance_to_similarity(distance: float) -> float:
    """Convertit une distance cosinus en similarité bornée entre 0 et 1."""
    return min(1.0, max(0.0, 1.0 - distance))


class VectorStore:
    """Stockage et recherche des morceaux indexés pour un modèle d'embedding donné."""

    def __init__(self, index_dir: Path, embed_model: str) -> None:
        """Ouvre (ou crée) l'index sur disque et la collection du modèle."""
        index_dir.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(
            path=str(index_dir), settings=ChromaSettings(anonymized_telemetry=False)
        )
        self._embed_model = embed_model
        self._name = collection_name(embed_model)
        self._collection = self._open_collection()

    @property
    def name(self) -> str:
        """Nom de la collection utilisée."""
        return self._name

    def count(self) -> int:
        """Nombre de morceaux indexés."""
        return self._collection.count()

    def reset(self) -> None:
        """Vide la collection du modèle (les collections des autres modèles sont conservées)."""
        if self._name in {collection.name for collection in self._client.list_collections()}:
            self._client.delete_collection(self._name)
        self._collection = self._open_collection()

    def add(self, chunks: Sequence[Chunk], embeddings: Sequence[Sequence[float]]) -> None:
        """Ajoute des morceaux et leurs vecteurs, par lots."""
        if len(chunks) != len(embeddings):
            raise ValueError("Il faut exactement un vecteur par morceau.")
        for start in range(0, len(chunks), ADD_BATCH_SIZE):
            batch = chunks[start : start + ADD_BATCH_SIZE]
            self._collection.add(
                ids=[chunk.chunk_id for chunk in batch],
                embeddings=[list(vector) for vector in embeddings[start : start + ADD_BATCH_SIZE]],
                documents=[chunk.text for chunk in batch],
                metadatas=[chunk.to_metadata() for chunk in batch],
            )

    def query(self, embedding: Sequence[float], top_k: int) -> list[ScoredChunk]:
        """Renvoie les `top_k` morceaux les plus proches, du plus au moins similaire."""
        total = self.count()
        if total == 0:
            raise EmptyIndexError
        result = self._collection.query(
            query_embeddings=[list(embedding)],
            n_results=min(top_k, total),
            include=["documents", "metadatas", "distances"],
        )
        rows = zip(
            result["ids"][0],
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
            strict=True,
        )
        return [
            ScoredChunk(Chunk.from_metadata(chunk_id, text, metadata), distance_to_similarity(d))
            for chunk_id, text, metadata, d in rows
        ]

    def list_documents(self) -> list[DocumentSummary]:
        """Liste les documents indexés avec leur nombre de pages et de morceaux, par titre."""
        metadatas = self._collection.get(include=["metadatas"])["metadatas"] or []
        counts: dict[str, int] = {}
        firsts: dict[str, dict] = {}
        for metadata in metadatas:
            doc_id = str(metadata["doc_id"])
            counts[doc_id] = counts.get(doc_id, 0) + 1
            firsts.setdefault(doc_id, metadata)
        summaries = [
            DocumentSummary(
                doc_id=doc_id,
                title=str(meta["title"]),
                source_path=Path(str(meta["source_path"])),
                page_count=int(meta["page_count"]),
                chunk_count=counts[doc_id],
            )
            for doc_id, meta in firsts.items()
        ]
        return sorted(summaries, key=lambda summary: summary.title.casefold())

    def _open_collection(self) -> chromadb.Collection:
        """Ouvre ou crée la collection, en distance cosinus et sans embedding interne."""
        return self._client.get_or_create_collection(
            name=self._name,
            metadata={"embed_model": self._embed_model},
            configuration={"hnsw": {"space": "cosine"}},
            embedding_function=None,
        )
