"""Tests de la normalisation de texte (rag/textutils.py)."""

from rag.textutils import normalize_for_matching


def test_normalisation():
    texte = "  Politique d’octroi :\n500 000   FCFA "
    assert normalize_for_matching(texte) == "politique d'octroi : 500 000 fcfa"
