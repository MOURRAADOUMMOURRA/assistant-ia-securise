"""Tests de l'ingestion des PDF et du retrait des en-têtes et pieds de page."""

import pytest

from rag.errors import UnreadablePdfError, UnsupportedFormatError
from rag.ingestion import (
    edge_key,
    is_page_numbering,
    load_directory,
    load_pdf,
    remove_repeated_edges,
    title_from_filename,
)
from tests.pdf_factory import FOOTER, HEADER, write_pdf

# --- Règles de retrait, sur des lignes déjà extraites ----------------------


def _pages(n: int, body: list[str] | None = None) -> list[list[str]]:
    return [
        [
            "Kouri Épargne",
            "Réf. CR-PRO-01",
            *(body or [f"Contenu propre à la page {i}"]),
            "Document fictif",
            f"Page {i} / {n}",
        ]
        for i in range(1, n + 1)
    ]


@pytest.mark.parametrize("ligne", ["Page 2 / 8", "page 10 sur 12", "3", "- 4 -", "5/9"])
def test_lignes_de_numerotation_reconnues(ligne):
    assert is_page_numbering(ligne)


@pytest.mark.parametrize("ligne", ["Article 3", "500 000 FCFA", "Taux : 21 %"])
def test_lignes_ordinaires_non_numerotation(ligne):
    assert not is_page_numbering(ligne)


def test_chiffres_neutralises_seulement_dans_la_numerotation():
    assert edge_key("Page 2 / 8") == edge_key("Page 7 / 8")
    assert edge_key("Article 3") != edge_key("Article 4")


def test_entete_et_pied_retires_contenu_conserve():
    cleaned = remove_repeated_edges(_pages(4))
    for i, lines in enumerate(cleaned, start=1):
        assert lines == [f"Contenu propre à la page {i}"]


def test_article_en_tete_de_page_non_retire():
    pages = [["Kouri Épargne", f"Article {i}", "texte", "Page x"] for i in range(1, 5)]
    pages = [[p[0], p[1], p[2], f"Page {i} / 4"] for i, p in enumerate(pages, start=1)]
    cleaned = remove_repeated_edges(pages)
    assert [lines[0] for lines in cleaned] == ["Article 1", "Article 2", "Article 3", "Article 4"]


def test_arret_a_la_premiere_ligne_non_repetee():
    pages = [
        ["Kouri Épargne", f"Titre {i}", "Kouri Épargne", f"corps {i}", f"fin {i}", f"Page {i} / 3"]
        for i in range(1, 4)
    ]
    cleaned = remove_repeated_edges(pages)
    assert cleaned[0] == ["Titre 1", "Kouri Épargne", "corps 1", "fin 1"]


def test_ligne_repetee_au_milieu_de_page_conservee():
    corps = ["a", "b", "c", "Kouri Épargne", "d", "e", "f"]
    cleaned = remove_repeated_edges(_pages(3, corps))
    assert "Kouri Épargne" in cleaned[0]


def test_ligne_presente_sur_moins_de_la_moitie_des_pages_conservee():
    pages = _pages(6)
    pages[0].insert(2, "Note spéciale")
    pages[1].insert(2, "Note spéciale")
    cleaned = remove_repeated_edges(pages)
    assert cleaned[0][0] == "Note spéciale"


def test_document_d_une_seule_page_inchange():
    page = ["Kouri Épargne", "Contenu", "Page 1 / 1"]
    assert remove_repeated_edges([page]) == [page]


def test_titre_depuis_le_nom_de_fichier(tmp_path):
    assert title_from_filename(tmp_path / "d10_octroi_credit.pdf") == "Octroi credit"
    assert title_from_filename(tmp_path / "note-de-service.pdf") == "Note de service"


# --- Lecture de vrais fichiers PDF ------------------------------------------


def test_lecture_page_par_page_avec_metadonnees(tmp_path):
    path = write_pdf(
        tmp_path / "d10.pdf",
        [["Article 1 : objet"], ["Article 2 : plafond de 500 000 FCFA"], ["Article 3 : fin"]],
        title="Politique et procédure d'octroi de crédit",
    )
    pages = load_pdf(path)
    assert [p.page_number for p in pages] == [1, 2, 3]
    assert {p.page_count for p in pages} == {3}
    assert pages[0].title == "Politique et procédure d'octroi de crédit"
    assert pages[0].doc_id == "d10"
    assert "500 000 FCFA" in pages[1].text


def test_entete_et_pied_absents_du_texte_extrait(tmp_path):
    path = write_pdf(tmp_path / "doc.pdf", [["Contenu A"], ["Contenu B"], ["Contenu C"]])
    for page in load_pdf(path):
        assert HEADER not in page.text
        assert FOOTER not in page.text
        assert "Page " not in page.text


def test_titre_deduit_du_nom_si_metadonnees_absentes(tmp_path):
    path = write_pdf(tmp_path / "d05_frais_de_mission.pdf", [["x"], ["y"]], title=None)
    assert load_pdf(path)[0].title == "Frais de mission"


def test_format_non_pdf_refuse(tmp_path):
    fichier = tmp_path / "procedure.docx"
    fichier.write_bytes(b"faux")
    with pytest.raises(UnsupportedFormatError) as info:
        load_pdf(fichier)
    assert "Exportez votre document en PDF" in info.value.user_message


def test_pdf_endommage(tmp_path):
    fichier = tmp_path / "abime.pdf"
    fichier.write_bytes(b"ceci n'est pas un PDF")
    with pytest.raises(UnreadablePdfError):
        load_pdf(fichier)


def test_pdf_sans_texte(tmp_path):
    path = write_pdf(tmp_path / "scan.pdf", [[], []], with_edges=False)
    with pytest.raises(UnreadablePdfError, match="scanné"):
        load_pdf(path)


def test_fichier_introuvable(tmp_path):
    with pytest.raises(UnreadablePdfError, match="introuvable"):
        load_pdf(tmp_path / "absent.pdf")


def test_dossier_avec_fichiers_refuses(tmp_path):
    write_pdf(tmp_path / "a.pdf", [["page A1"], ["page A2"]])
    write_pdf(tmp_path / "b.pdf", [["page B1"], ["page B2"]])
    (tmp_path / "notes.txt").write_text("texte", encoding="utf-8")
    result = load_directory(tmp_path)
    assert result.document_count == 2
    assert len(result.pages) == 4
    assert [p.name for p in result.failures] == ["notes.txt"]
