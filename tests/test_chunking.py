"""Tests du découpage en morceaux (rag/chunking.py)."""

import re
from itertools import pairwise
from pathlib import Path

import pytest

from rag.chunking import chunk_pages, make_chunk_id, split_text
from rag.models import Page

PHRASE = "Le comité de crédit examine chaque dossier avec soin et rend un avis motivé. "


def _page(number: int, text: str, doc_id: str = "d10") -> Page:
    return Page(doc_id, "Politique de crédit", Path(f"{doc_id}.pdf"), number, 3, text)


def _long_text(n_phrases: int = 40) -> str:
    return "".join(f"{PHRASE[:-2]} n° {i}. " for i in range(n_phrases))


def test_texte_court_un_seul_morceau():
    assert split_text("Texte court.", 900, 150) == ["Texte court."]


def test_texte_vide_aucun_morceau():
    assert split_text("   \n ", 900, 150) == []


def test_aucun_morceau_ne_depasse_la_taille():
    pieces = split_text(_long_text(), 900, 150)
    assert len(pieces) > 1
    assert all(len(piece) <= 900 for piece in pieces)


def test_morceaux_assez_remplis():
    pieces = split_text(_long_text(), 900, 150)
    assert all(len(piece) >= 500 for piece in pieces[:-1])


def test_chevauchement_entre_morceaux_voisins():
    pieces = split_text(_long_text(), 900, 150)
    for previous, following in pairwise(pieces):
        debut_suivant = following[:40]
        assert debut_suivant in previous


def test_coupure_sur_une_fin_de_phrase():
    pieces = split_text(_long_text(), 900, 150)
    assert all(piece.endswith(".") for piece in pieces)


def test_aucun_mot_coupe_en_debut_de_morceau():
    text = _long_text()
    mots = set(re.findall(r"\S+", text))
    for piece in split_text(text, 900, 150):
        assert piece.split()[0] in mots


def test_tout_le_texte_est_couvert():
    text = _long_text()
    pieces = split_text(text, 900, 150)
    for i in range(40):
        assert any(f"n° {i}." in piece for piece in pieces)


def test_texte_sans_espace_coupe_a_la_limite():
    pieces = split_text("x" * 2000, 900, 150)
    assert all(len(piece) <= 900 for piece in pieces)
    assert "".join(pieces).count("x") >= 2000


def test_chevauchement_invalide_refuse():
    with pytest.raises(ValueError, match="chevauchement"):
        split_text("abc", 100, 100)


def test_un_morceau_ne_deborde_jamais_sur_deux_pages():
    pages = [_page(1, "Fin de la page un. " * 60), _page(2, "Début de la page deux. " * 60)]
    chunks = chunk_pages(pages, 900, 150)
    for chunk in chunks:
        if chunk.page_number == 1:
            assert "page deux" not in chunk.text
        else:
            assert "page un" not in chunk.text


def test_metadonnees_conservees():
    chunk = chunk_pages([_page(2, "Texte de la page.")], 900, 150)[0]
    assert (chunk.doc_id, chunk.title, chunk.page_number, chunk.page_count) == (
        "d10",
        "Politique de crédit",
        2,
        3,
    )


def test_identifiants_uniques_et_stables():
    pages = [_page(1, _long_text()), _page(2, _long_text()), _page(1, "x", doc_id="d11")]
    first = [c.chunk_id for c in chunk_pages(pages, 900, 150)]
    second = [c.chunk_id for c in chunk_pages(pages, 900, 150)]
    assert first == second
    assert len(set(first)) == len(first)
    assert make_chunk_id("d10", 4, 1) == "d10:p004:c01"


def test_page_vide_ignoree():
    assert chunk_pages([_page(1, "")], 900, 150) == []
