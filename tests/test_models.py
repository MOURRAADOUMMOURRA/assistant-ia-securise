"""Tests des structures de données (rag/models.py) et des erreurs (rag/errors.py)."""

from pathlib import Path

from rag.errors import AssistantError, ModelNotFoundError, UnsupportedFormatError
from rag.models import Answer, Chunk, Source


def _chunk() -> Chunk:
    return Chunk(
        chunk_id="d10:p004:c00",
        doc_id="d10",
        title="Politique et procédure d'octroi de crédit",
        source_path=Path("demo_docs/d10.pdf"),
        page_number=4,
        page_count=10,
        chunk_index=0,
        text="Le montant maximal d'un premier crédit est de 500 000 FCFA.",
    )


def test_embedding_text_commence_par_le_titre_sans_le_stocker():
    chunk = _chunk()
    assert chunk.embedding_text.startswith("Politique et procédure d'octroi de crédit\n\n")
    assert chunk.embedding_text.endswith(chunk.text)
    assert "Politique" not in chunk.text


def test_aller_retour_metadonnees():
    chunk = _chunk()
    metadata = chunk.to_metadata()
    assert all(isinstance(v, str | int | float | bool) for v in metadata.values())
    assert Chunk.from_metadata(chunk.chunk_id, chunk.text, metadata) == chunk


def test_libelle_de_source():
    source = Source("d10", "Politique de crédit", Path("x.pdf"), 4, 10, "extrait", 0.8)
    assert source.label == "Politique de crédit, page 4"


def test_sources_citees_filtrees():
    citee = Source("a", "A", Path("a.pdf"), 1, 3, "", 0.9, cited=True)
    non_citee = Source("b", "B", Path("b.pdf"), 2, 3, "", 0.7)
    answer = Answer("texte", sources=(citee, non_citee))
    assert answer.cited_sources == (citee,)


def test_message_utilisateur_par_defaut():
    assert "PDF" in UnsupportedFormatError().user_message
    assert AssistantError("personnalisé").user_message == "personnalisé"


def test_modele_absent_donne_la_commande():
    error = ModelNotFoundError("bge-m3")
    assert "ollama pull bge-m3" in error.user_message
    assert isinstance(error, AssistantError)
