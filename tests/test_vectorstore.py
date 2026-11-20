"""Tests de la base vectorielle (rag/vectorstore.py) avec un vrai ChromaDB local temporaire."""

import pytest

from rag.errors import EmptyIndexError
from rag.vectorstore import VectorStore, collection_name, distance_to_similarity
from tests.fakes import FakeEmbedder, make_chunk


@pytest.fixture
def store(tmp_path):
    return VectorStore(tmp_path / "index", "bge-m3")


def _remplir(store: VectorStore) -> FakeEmbedder:
    embedder = FakeEmbedder()
    chunks = [
        make_chunk("d10", 4, "plafond premier crédit cinq cent mille", "Octroi de crédit"),
        make_chunk("d10", 6, "mensualité maximale revenu net", "Octroi de crédit"),
        make_chunk("d08", 2, "point de rassemblement parking siège", "Consignes incendie"),
    ]
    store.add(chunks, embedder.embed([c.embedding_text for c in chunks]))
    return embedder


def test_nom_de_collection_valide():
    assert collection_name("bge-m3") == "chunks_bge-m3"
    assert collection_name("nomic-embed-text:v1.5") == "chunks_nomic-embed-text_v1_5"


def test_similarite_bornee():
    assert distance_to_similarity(0.0) == 1.0
    assert distance_to_similarity(0.3) == pytest.approx(0.7)
    assert distance_to_similarity(1.4) == 0.0


def test_index_vide_leve_une_erreur_claire(store):
    with pytest.raises(EmptyIndexError) as info:
        store.query([0.1] * 64, 5)
    assert "rag.indexer" in info.value.user_message


def test_recherche_du_plus_proche(store):
    embedder = _remplir(store)
    hits = store.query(embedder.embed(["point de rassemblement"])[0], 2)
    assert hits[0].chunk.doc_id == "d08"
    assert hits[0].chunk.page_number == 2
    assert hits[0].score >= hits[1].score
    assert 0.0 <= hits[1].score <= 1.0


def test_top_k_plus_grand_que_l_index(store):
    embedder = _remplir(store)
    assert len(store.query(embedder.embed(["crédit"])[0], 50)) == 3


def test_metadonnees_restituees(store):
    embedder = _remplir(store)
    chunk = store.query(embedder.embed(["mensualité maximale"])[0], 1)[0].chunk
    assert (chunk.title, chunk.page_number, chunk.page_count) == ("Octroi de crédit", 6, 5)
    assert chunk.text == "mensualité maximale revenu net"


def test_liste_des_documents(store):
    _remplir(store)
    documents = store.list_documents()
    assert [(d.title, d.chunk_count) for d in documents] == [
        ("Consignes incendie", 1),
        ("Octroi de crédit", 2),
    ]


def test_reinitialisation(store):
    _remplir(store)
    store.reset()
    assert store.count() == 0


def test_persistance_sur_disque(tmp_path):
    _remplir(VectorStore(tmp_path / "index", "bge-m3"))
    assert VectorStore(tmp_path / "index", "bge-m3").count() == 3


def test_une_collection_par_modele(tmp_path):
    _remplir(VectorStore(tmp_path / "index", "bge-m3"))
    autre = VectorStore(tmp_path / "index", "autre-modele")
    assert autre.count() == 0
    autre.reset()
    assert VectorStore(tmp_path / "index", "bge-m3").count() == 3


def test_nombre_de_vecteurs_incoherent(store):
    with pytest.raises(ValueError, match="un vecteur par morceau"):
        store.add([make_chunk("d1", 1, "x")], [])
