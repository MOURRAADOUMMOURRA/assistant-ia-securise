"""Tests du rendu de page surlignée (rag/page_render.py)."""

import pymupdf
import pytest

from rag.errors import AssistantError
from rag.page_render import find_passage_rects, render_highlighted_page
from tests.pdf_factory import write_pdf

PASSAGE = "Le montant maximal accordé pour un premier crédit est de 500 000 FCFA"


@pytest.fixture
def docs(tmp_path):
    dossier = tmp_path / "docs"
    dossier.mkdir()
    write_pdf(
        dossier / "d10.pdf",
        [
            ["Introduction générale du document de test."],
            [
                "Une ligne sans rapport avec la question.",
                PASSAGE + ".",
                "Une autre ligne sans rapport.",
            ],
        ],
        title="Octroi",
    )
    return dossier


def _yellow_pixels(png: bytes) -> int:
    """Compte les pixels jaunes (rouge et vert forts, bleu faible) d'une image PNG."""
    with pymupdf.open(stream=png, filetype="png") as image:
        pixmap = image[0].get_pixmap()
    samples, n = pixmap.samples, pixmap.n
    return sum(
        1
        for i in range(0, len(samples), n)
        if samples[i] > 200 and samples[i + 1] > 180 and samples[i + 2] < 140
    )


def test_page_rendue_en_png_avec_passage_surligne(docs):
    image = render_highlighted_page(docs / "d10.pdf", 2, PASSAGE, docs)
    assert image.png.startswith(b"\x89PNG")
    assert image.page_number == 2
    assert image.highlights == 1
    assert _yellow_pixels(image.png) > 500


def test_sans_passage_aucun_surlignage(docs):
    image = render_highlighted_page(docs / "d10.pdf", 2, "", docs)
    assert image.highlights == 0
    assert _yellow_pixels(image.png) == 0


def test_passage_absent_de_la_page(docs):
    image = render_highlighted_page(docs / "d10.pdf", 1, PASSAGE, docs)
    assert image.highlights == 0


def test_surlignage_limite_au_passage(docs):
    with pymupdf.open(docs / "d10.pdf") as document:
        rects = find_passage_rects(document[1], PASSAGE)
        ligne_hors_sujet = document[1].search_for("Une autre ligne")[0]
    assert len(rects) == 1
    assert not rects[0].intersects(ligne_hors_sujet)


def test_espaces_et_casse_ignores(docs):
    with pymupdf.open(docs / "d10.pdf") as document:
        rects = find_passage_rects(document[1], PASSAGE.upper().replace(" ", "  "))
    assert len(rects) == 1


def test_le_pdf_d_origine_n_est_pas_modifie(docs):
    avant = (docs / "d10.pdf").read_bytes()
    render_highlighted_page(docs / "d10.pdf", 2, PASSAGE, docs)
    assert (docs / "d10.pdf").read_bytes() == avant


def test_page_inexistante(docs):
    with pytest.raises(AssistantError, match="page 9"):
        render_highlighted_page(docs / "d10.pdf", 9, PASSAGE, docs)


def test_fichier_hors_du_dossier_des_documents_refuse(docs, tmp_path):
    externe = write_pdf(tmp_path / "secret.pdf", [["Contenu confidentiel"], ["x"]])
    with pytest.raises(AssistantError, match="pas disponible"):
        render_highlighted_page(externe, 1, "", docs)


def test_chemin_detourne_refuse(docs):
    with pytest.raises(AssistantError, match="pas disponible"):
        render_highlighted_page(docs / ".." / "docs" / ".." / "secret.pdf", 1, "", docs)


def test_vrai_document_du_corpus():
    from config import PROJECT_ROOT

    docs_dir = PROJECT_ROOT / "demo_docs"
    pdf = docs_dir / "d10_octroi_credit.pdf"
    if not pdf.exists():
        pytest.skip("corpus de démonstration absent")
    passage = "Pour un premier crédit, le montant maximal accordé est de 500 000 FCFA"
    image = render_highlighted_page(pdf, 4, passage, docs_dir)
    assert image.highlights >= 1
