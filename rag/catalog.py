"""Vue d'ensemble du corpus : chaque PDF du dossier, ses pages et ses morceaux indexés."""

from pathlib import Path

import pymupdf

from rag.ingestion import title_from_filename
from rag.models import DocumentSummary
from rag.vectorstore import VectorStore


def corpus_overview(docs_dir: Path, store: VectorStore) -> list[DocumentSummary]:
    """Liste les PDF du dossier, triés par titre, avec leur nombre de morceaux indexés.

    Un document présent dans le dossier mais pas encore indexé apparaît avec 0 morceau.
    """
    if not docs_dir.is_dir():
        return []
    indexed = {summary.doc_id: summary.chunk_count for summary in store.list_documents()}
    summaries = [
        _summarize(path, indexed.get(path.stem, 0)) for path in sorted(docs_dir.glob("*.pdf"))
    ]
    return sorted(summaries, key=lambda summary: summary.title.casefold())


def _summarize(path: Path, chunk_count: int) -> DocumentSummary:
    """Lit le titre et le nombre de pages d'un PDF (sans en extraire le texte)."""
    try:
        with pymupdf.open(path) as document:
            title = (document.metadata or {}).get("title") or title_from_filename(path)
            page_count = len(document)
    except (RuntimeError, ValueError):
        title, page_count = title_from_filename(path), 0
    return DocumentSummary(path.stem, title, path, page_count, chunk_count)
