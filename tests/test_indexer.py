"""Tests de l'indexeur (rag/indexer.py) avec un faux modèle d'embedding."""

import logging

import pytest

from config import get_settings
from rag import indexer
from rag.errors import AssistantError, OllamaUnavailableError
from rag.indexer import EXIT_ERROR, EXIT_OK, build_index, embed_chunks
from rag.logging_setup import LOGGER_NAME
from rag.vectorstore import VectorStore
from tests.fakes import FakeEmbedder, make_chunk
from tests.pdf_factory import write_pdf


class EmbedderEnPanne:
    def embed(self, texts):
        raise OllamaUnavailableError


@pytest.fixture
def docs_dir(tmp_path):
    dossier = tmp_path / "docs"
    dossier.mkdir()
    write_pdf(dossier / "d10.pdf", [["Plafond : 500 000 FCFA."], ["Mensualité : 40 %."]], "Octroi")
    write_pdf(dossier / "d14.pdf", [["AGR : 21 % par an."], ["Tenue de compte."]], "Grille 2026")
    (dossier / "procedure.docx").write_bytes(b"x")
    return dossier


@pytest.fixture
def store(tmp_path):
    return VectorStore(tmp_path / "index", "bge-m3")


@pytest.fixture(autouse=True)
def fermer_le_journal():
    yield
    logger = logging.getLogger(LOGGER_NAME)
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)


def test_indexation_complete(docs_dir, store, make_settings):
    report = build_index(docs_dir, make_settings(), FakeEmbedder(), store)
    assert (report.document_count, report.page_count) == (2, 4)
    assert report.chunk_count == store.count() == 4
    assert [p.name for p in report.failures] == ["procedure.docx"]


def test_titre_place_devant_le_texte_pour_l_embedding(docs_dir, store, make_settings):
    embedder = FakeEmbedder()
    build_index(docs_dir, make_settings(), embedder, store)
    textes = [t for lot in embedder.calls for t in lot]
    assert any(t.startswith("Grille 2026\n\n") for t in textes)
    hit = store.query(embedder.embed(["AGR"])[0], 1)[0]
    assert not hit.chunk.text.startswith("Grille 2026")


def test_reindexation_remplace_l_index(docs_dir, store, make_settings):
    build_index(docs_dir, make_settings(), FakeEmbedder(), store)
    build_index(docs_dir, make_settings(), FakeEmbedder(), store)
    assert store.count() == 4


def test_ancien_index_intact_si_ollama_tombe(docs_dir, store, make_settings):
    build_index(docs_dir, make_settings(), FakeEmbedder(), store)
    with pytest.raises(OllamaUnavailableError):
        build_index(docs_dir, make_settings(), EmbedderEnPanne(), store)
    assert store.count() == 4


def test_dossier_sans_pdf_lisible(tmp_path, store, make_settings):
    vide = tmp_path / "vide"
    vide.mkdir()
    with pytest.raises(AssistantError, match="Aucun PDF lisible"):
        build_index(vide, make_settings(), FakeEmbedder(), store)


def test_dossier_introuvable(tmp_path, store, make_settings):
    with pytest.raises(AssistantError, match="introuvable"):
        build_index(tmp_path / "absent", make_settings(), FakeEmbedder(), store)


def test_progression_par_lots():
    chunks = [make_chunk("d1", 1, f"texte {i}", index=i) for i in range(40)]
    etapes: list[tuple[int, int]] = []
    vecteurs = embed_chunks(FakeEmbedder(), chunks, lambda d, t: etapes.append((d, t)), 16)
    assert len(vecteurs) == 40
    assert etapes == [(16, 40), (32, 40), (40, 40)]


def test_commande_complete(docs_dir, tmp_path, monkeypatch):
    monkeypatch.setenv("ASSISTANT_DOCS_DIR", str(docs_dir))
    monkeypatch.setenv("ASSISTANT_INDEX_DIR", str(tmp_path / "index_cli"))
    monkeypatch.setenv("ASSISTANT_LOGS_DIR", str(tmp_path / "logs"))
    monkeypatch.setattr(indexer, "OllamaClient", lambda _settings: FakeEmbedder())
    get_settings.cache_clear()
    try:
        assert indexer.main([]) == EXIT_OK
    finally:
        get_settings.cache_clear()
    assert VectorStore(tmp_path / "index_cli", "bge-m3").count() == 4
    journal = (tmp_path / "logs" / "assistant.log").read_text(encoding="utf-8")
    assert "Index reconstruit" in journal
    assert "procedure.docx" in journal


def test_commande_ollama_arrete_code_erreur(docs_dir, tmp_path, monkeypatch, make_settings):
    settings = make_settings(index_dir=tmp_path / "idx", logs_dir=tmp_path / "logs")
    assert indexer.run(settings, docs_dir, EmbedderEnPanne()) == EXIT_ERROR
