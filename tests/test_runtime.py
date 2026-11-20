"""Tests de la doublure, du catalogue, de l'état d'Ollama et du mode de fonctionnement."""

import httpx

from rag.catalog import corpus_overview
from rag.doubles import DOUBLE_ANSWER_PREFIX, ExtractiveGenerator, HashEmbedder
from rag.llm import check_ollama
from rag.models import ScoredChunk
from rag.pipeline import create_runtime
from rag.prompts import REFUSAL_MESSAGE, build_user_prompt
from rag.vectorstore import VectorStore
from tests.fakes import make_chunk
from tests.pdf_factory import write_pdf


def test_hash_embedder_proche_si_mots_communs():
    a, b, c = HashEmbedder().embed(
        ["plafond du premier crédit", "premier crédit plafond", "télétravail autorisé"]
    )
    dot = lambda u, v: sum(x * y for x, y in zip(u, v, strict=True))  # noqa: E731
    assert dot(a, b) > 0.99
    assert dot(a, c) < 0.2


def test_generateur_extractif_cite_le_premier_extrait():
    hit = ScoredChunk(make_chunk("d10", 4, "Le plafond est de 500 000 FCFA.", "Octroi"), 0.9)
    reponse = ExtractiveGenerator().generate("système", build_user_prompt("Plafond ?", [hit]))
    assert reponse.startswith(DOUBLE_ANSWER_PREFIX)
    assert "500 000 FCFA" in reponse
    assert "(Source : Octroi, page 4)" in reponse


def test_generateur_extractif_sans_extrait():
    assert ExtractiveGenerator().generate("s", "Question : rien") == REFUSAL_MESSAGE


def test_etat_ollama_connecte_et_modeles(make_settings):
    status = check_ollama(make_settings(), lambda _h: ["bge-m3:latest"])
    assert status.connected
    assert status.missing_models == ("qwen3:4b-instruct-2507-q4_K_M",)
    assert not status.ready
    assert "manquant" in status.message


def test_etat_ollama_arrete(make_settings):
    def refuse(_host):
        raise httpx.ConnectError("refusé")

    status = check_ollama(make_settings(), refuse)
    assert not status.connected
    assert "Non connecté" in status.message


def test_vue_d_ensemble_du_corpus(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    write_pdf(docs / "d02.pdf", [["a"], ["b"], ["c"]], title="Congés")
    write_pdf(docs / "d01.pdf", [["a"], ["b"]], title="Règlement")
    store = VectorStore(tmp_path / "index", "bge-m3")
    store.add([make_chunk("d01", 1, "texte")], [[1.0] + [0.0] * 63])
    overview = corpus_overview(docs, store)
    assert [(d.title, d.page_count, d.chunk_count) for d in overview] == [
        ("Congés", 3, 0),
        ("Règlement", 2, 1),
    ]


def test_mode_doublure_de_bout_en_bout(tmp_path, make_settings):
    docs = tmp_path / "docs"
    docs.mkdir()
    write_pdf(
        docs / "d10.pdf",
        [["Le plafond du premier crédit est fixé par la politique."], ["Autre sujet."]],
        title="Octroi de crédit",
    )
    settings = make_settings(docs_dir=docs, index_dir=tmp_path / "index")
    runtime = create_runtime(settings, test_double=True)
    assert runtime.test_double
    assert runtime.store.count() > 0
    answer = runtime.pipeline.ask("Quel est le plafond du premier crédit ?")
    assert answer.text.startswith(DOUBLE_ANSWER_PREFIX)
    assert answer.cited_sources[0].page_number == 1


def test_mode_reel_par_defaut(tmp_path, make_settings):
    settings = make_settings(index_dir=tmp_path / "index")
    runtime = create_runtime(settings)
    assert not runtime.test_double
    assert runtime.store.name == "chunks_bge-m3"
