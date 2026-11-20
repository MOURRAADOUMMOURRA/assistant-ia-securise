"""Reconstruction complète de l'index des documents.

Usage, depuis la racine du projet :

    .venv\\Scripts\\python -m rag.indexer

Lit tous les PDF du dossier des documents, les découpe, calcule les embeddings
(titre du document placé devant chaque morceau) puis remplace l'index. Les
embeddings sont tous calculés AVANT de toucher à l'index : si Ollama s'arrête en
cours de route, l'ancien index reste intact.
"""

import argparse
import sys
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError
from tqdm import tqdm

from config import PROJECT_ROOT, Settings, get_settings
from rag.chunking import chunk_pages
from rag.errors import AssistantError
from rag.ingestion import load_directory
from rag.llm import Embedder, OllamaClient
from rag.logging_setup import get_logger, setup_logging, setup_logging_from_settings
from rag.models import Chunk
from rag.vectorstore import VectorStore

EMBED_BATCH_SIZE = 16
EXIT_OK = 0
EXIT_ERROR = 1
EXIT_CONFIG_ERROR = 2

ProgressCallback = Callable[[int, int], None]
"""Fonction appelée avec (morceaux traités, total)."""

logger = get_logger("rag.indexer")


@dataclass(frozen=True)
class IndexReport:
    """Bilan d'une indexation."""

    document_count: int
    page_count: int
    chunk_count: int
    duration_s: float
    failures: dict[Path, str] = field(default_factory=dict)


def build_index(
    docs_dir: Path,
    settings: Settings,
    embedder: Embedder,
    store: VectorStore,
    on_progress: ProgressCallback | None = None,
    clock: Callable[[], float] = time.perf_counter,
) -> IndexReport:
    """Lit, découpe et indexe tous les PDF de `docs_dir`, en remplaçant l'index existant."""
    started = clock()
    if not docs_dir.is_dir():
        raise AssistantError(f"Dossier des documents introuvable : {docs_dir}")
    ingestion = load_directory(docs_dir)
    chunks = chunk_pages(ingestion.pages, settings.chunk_size, settings.chunk_overlap)
    if not chunks:
        raise AssistantError(f"Aucun PDF lisible dans le dossier {docs_dir}.")
    embeddings = embed_chunks(embedder, chunks, on_progress)
    store.reset()
    store.add(chunks, embeddings)
    return IndexReport(
        document_count=ingestion.document_count,
        page_count=len(ingestion.pages),
        chunk_count=len(chunks),
        duration_s=clock() - started,
        failures=dict(ingestion.failures),
    )


def embed_chunks(
    embedder: Embedder,
    chunks: Sequence[Chunk],
    on_progress: ProgressCallback | None = None,
    batch_size: int = EMBED_BATCH_SIZE,
) -> list[list[float]]:
    """Calcule les embeddings par lots (titre + texte), en signalant la progression."""
    embeddings: list[list[float]] = []
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]
        embeddings.extend(embedder.embed([chunk.embedding_text for chunk in batch]))
        if on_progress:
            on_progress(len(embeddings), len(chunks))
    return embeddings


class ProgressBar:
    """Barre de progression tqdm, créée au premier appel (quand le total est connu)."""

    def __init__(self) -> None:
        """Aucune barre n'est affichée avant le premier lot."""
        self._bar: tqdm | None = None

    def __call__(self, done: int, total: int) -> None:
        """Avance la barre jusqu'à `done` morceaux sur `total`."""
        if self._bar is None:
            self._bar = tqdm(total=total, desc="Embeddings", unit="morceau")
        self._bar.update(done - self._bar.n)

    def close(self) -> None:
        """Ferme la barre si elle a été ouverte."""
        if self._bar is not None:
            self._bar.close()


def run(settings: Settings, docs_dir: Path, embedder: Embedder | None = None) -> int:
    """Indexe les documents et journalise le bilan ; renvoie le code de sortie."""
    store = VectorStore(settings.index_dir, settings.embed_model)
    progress = ProgressBar()
    try:
        report = build_index(
            docs_dir, settings, embedder or OllamaClient(settings), store, progress
        )
    except AssistantError as error:
        logger.error("Indexation impossible : %s", error.user_message)
        return EXIT_ERROR
    finally:
        progress.close()
    _log_report(report, store.name)
    return EXIT_OK


def main(argv: Sequence[str] | None = None) -> int:
    """Point d'entrée de la commande `python -m rag.indexer`."""
    parser = argparse.ArgumentParser(description="Reconstruit tout l'index des documents.")
    parser.add_argument("--docs-dir", type=Path, help="Dossier des PDF (par défaut : .env).")
    args = parser.parse_args(argv)
    try:
        settings = get_settings()
    except ValidationError as error:
        setup_logging(PROJECT_ROOT / "logs")
        logger.error("Configuration invalide dans .env : %s", error.errors()[0]["msg"])
        return EXIT_CONFIG_ERROR
    setup_logging_from_settings(settings)
    return run(settings, args.docs_dir or settings.docs_dir)


def _log_report(report: IndexReport, collection: str) -> None:
    """Journalise le bilan de l'indexation."""
    logger.info(
        "Index reconstruit en %.1f s : %d documents, %d pages, %d morceaux (collection %s).",
        report.duration_s,
        report.document_count,
        report.page_count,
        report.chunk_count,
        collection,
    )
    for path, reason in report.failures.items():
        logger.warning("Non indexé : %s — %s", path.name, reason)


if __name__ == "__main__":
    sys.exit(main())
