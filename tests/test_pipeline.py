"""Tests du pipeline complet (rag/pipeline.py) avec doublures : Ollama n'est jamais appelé."""

import itertools

import pytest

from rag.errors import OllamaUnavailableError
from rag.models import ScoredChunk
from rag.pipeline import EMPTY_QUESTION_MESSAGE, RagPipeline, build_sources, is_cited
from rag.prompts import REFUSAL_MESSAGE
from rag.retrieval import Retriever
from rag.vectorstore import VectorStore
from tests.fakes import FakeEmbedder, FakeGenerator, make_chunk

OCTROI = "Politique et procédure d'octroi de crédit"
GRILLE_2025 = "Grille des taux et frais 2025"
GRILLE_2026 = "Grille des taux et frais 2026"


@pytest.fixture
def store(tmp_path):
    store = VectorStore(tmp_path / "index", "bge-m3")
    chunks = [
        make_chunk("d10", 4, "plafond du premier crédit 500 000 FCFA", OCTROI),
        make_chunk("d10", 4, "premier crédit accordé après analyse", OCTROI, index=1),
        make_chunk("d10", 6, "mensualité maximale 40 % du revenu net", OCTROI),
        make_chunk("d13", 2, "taux crédit AGR 24 % par an", GRILLE_2025),
        make_chunk("d14", 2, "taux crédit AGR 21 % par an", GRILLE_2026),
    ]
    store.add(chunks, FakeEmbedder().embed([c.text for c in chunks]))
    return store


def _pipeline(store, reply="Réponse.", threshold=0.3, embedder=None, clock=None):
    generator = FakeGenerator(reply)
    retriever = Retriever(embedder or FakeEmbedder(), store, top_k=5, threshold=threshold)
    ticks = itertools.count(start=10.0, step=1.5)
    pipeline = RagPipeline(retriever, generator, clock=clock or (lambda: next(ticks)))
    return pipeline, generator


def test_reponse_citee_avec_sources_issues_des_metadonnees(store):
    reply = f"Le plafond est de 500 000 FCFA (Source : {OCTROI}, page 4)."
    pipeline, generator = _pipeline(store, reply)
    answer = pipeline.ask("Quel est le plafond du premier crédit ?")
    assert not answer.refused
    assert answer.text == reply
    assert len(generator.calls) == 1
    assert [s.label for s in answer.cited_sources] == [f"{OCTROI}, page 4"]
    assert answer.sources[0].source_path.name == "d10.pdf"


def test_une_seule_source_par_page(store):
    pipeline, _ = _pipeline(store, f"(Source : {OCTROI}, page 4)", threshold=0.0)
    answer = pipeline.ask("premier crédit")
    pages = [(s.doc_id, s.page_number) for s in answer.sources]
    assert len(pages) == len(set(pages))


def test_sous_le_seuil_refus_sans_appeler_le_llm(store):
    pipeline, generator = _pipeline(store, threshold=0.6)
    answer = pipeline.ask("Le télétravail est-il autorisé ?")
    assert answer.refused
    assert answer.text == REFUSAL_MESSAGE
    assert answer.sources == ()
    assert generator.calls == []


def test_refus_du_llm_sans_sources(store):
    pipeline, _ = _pipeline(store, REFUSAL_MESSAGE)
    answer = pipeline.ask("plafond du premier crédit")
    assert answer.refused
    assert answer.text == REFUSAL_MESSAGE
    assert answer.sources == ()


def test_citation_inventee_jamais_dans_les_sources(store):
    pipeline, _ = _pipeline(store, "500 000 FCFA (Source : Manuel secret, page 9).")
    answer = pipeline.ask("plafond du premier crédit")
    assert all(s.title != "Manuel secret" for s in answer.sources)
    assert answer.cited_sources == ()
    assert answer.sources


def test_les_deux_versions_envoyees_au_llm(store):
    pipeline, generator = _pipeline(store, threshold=0.2)
    pipeline.ask("taux du crédit AGR")
    user_prompt = generator.calls[0][1]
    assert f"[{GRILLE_2026}, page 2]" in user_prompt
    assert f"[{GRILLE_2025}, page 2]" in user_prompt


def test_question_vide(store):
    embedder = FakeEmbedder()
    pipeline, generator = _pipeline(store, embedder=embedder)
    answer = pipeline.ask("   ")
    assert answer.text == EMPTY_QUESTION_MESSAGE
    assert embedder.calls == []
    assert generator.calls == []


def test_duree_mesuree(store):
    pipeline, _ = _pipeline(store)
    assert pipeline.ask("plafond du premier crédit").duration_s == pytest.approx(1.5)


def test_ollama_arrete_remonte_une_erreur_claire(store):
    class EmbedderEnPanne:
        def embed(self, texts):
            raise OllamaUnavailableError

    pipeline, _ = _pipeline(store, embedder=EmbedderEnPanne())
    with pytest.raises(OllamaUnavailableError):
        pipeline.ask("question")


def test_journal_sans_la_question(store, caplog):
    pipeline, _ = _pipeline(store, f"(Source : {OCTROI}, page 4)")
    with caplog.at_level("INFO", logger="assistant"):
        pipeline.ask("Question confidentielle sur le plafond du premier crédit")
    assert "confidentielle" not in caplog.text
    assert "citées : d10" in caplog.text
    assert "Réponse en" in caplog.text


@pytest.mark.parametrize(
    "texte",
    [
        f"(Source : {OCTROI}, page 4)",
        f"(source : {OCTROI.upper()} , page 4)",
        "(Source : Politique et procédure d’octroi de crédit, p. 4)",
        f"Source : {OCTROI} - page 4",
    ],
)
def test_citation_reconnue(texte):
    assert is_cited(texte, OCTROI, 4)


@pytest.mark.parametrize(
    "texte", [f"(Source : {OCTROI}, page 40)", f"(Source : {OCTROI}, page 5)", "page 4"]
)
def test_citation_non_reconnue(texte):
    assert not is_cited(texte, OCTROI, 4)


def test_sources_triees_par_pertinence():
    hits = [
        ScoredChunk(make_chunk("a", 1, "x", "A"), 0.5),
        ScoredChunk(make_chunk("b", 1, "y", "B"), 0.9),
    ]
    assert [s.doc_id for s in build_sources("", hits)] == ["b", "a"]
