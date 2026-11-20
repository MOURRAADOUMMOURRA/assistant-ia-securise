"""Tests de la recherche avec seuil (rag/retrieval.py), sans Ollama."""

import pytest

from rag.errors import EmptyIndexError
from rag.retrieval import Retriever
from rag.vectorstore import VectorStore
from tests.fakes import FakeEmbedder, make_chunk


@pytest.fixture
def store(tmp_path):
    store = VectorStore(tmp_path / "index", "bge-m3")
    chunks = [
        make_chunk("d10", 4, "plafond premier crédit cinq cent mille francs"),
        make_chunk("d10", 6, "mensualité maximale quarante pour cent du revenu"),
        make_chunk("d08", 2, "point de rassemblement parking devant le siège"),
    ]
    store.add(chunks, FakeEmbedder().embed([c.text for c in chunks]))
    return store


def test_question_pertinente(store):
    result = Retriever(FakeEmbedder(), store, top_k=5, threshold=0.3).retrieve(
        "point de rassemblement du siège"
    )
    assert result.is_relevant
    assert result.hits[0].chunk.doc_id == "d08"
    assert result.best_score == result.hits[0].score


def test_seuil_elimine_les_morceaux_trop_faibles(store):
    result = Retriever(FakeEmbedder(), store, top_k=5, threshold=0.3).retrieve(
        "point de rassemblement du siège"
    )
    assert all(hit.score >= 0.3 for hit in result.hits)
    assert len(result.hits) < 3


def test_question_hors_sujet_non_pertinente(store):
    result = Retriever(FakeEmbedder(), store, top_k=5, threshold=0.5).retrieve(
        "télétravail autorisé"
    )
    assert not result.is_relevant
    assert result.best_score is not None
    assert result.best_score < 0.5


def test_top_k_respecte(store):
    result = Retriever(FakeEmbedder(), store, top_k=2, threshold=0.0).retrieve("crédit")
    assert len(result.hits) == 2


def test_index_vide(tmp_path):
    vide = VectorStore(tmp_path / "vide", "bge-m3")
    with pytest.raises(EmptyIndexError):
        Retriever(FakeEmbedder(), vide, top_k=5, threshold=0.5).retrieve("question")
