"""Tests du corpus de démonstration : faits, calculs, vérificateur et erreurs injectées."""

import shutil

import pytest

from scripts import verify_demo_pdfs as verifier
from scripts.demo_corpus.facts import (
    ANSWER_KEYS,
    DOCUMENTS,
    EXAMPLE_LOAN_FCFA,
    EXAMPLE_LOAN_MONTHS,
    GRIDS,
    decimal_fr,
    fcfa,
    pct,
)
from scripts.demo_corpus.grille import compute_loan_example
from scripts.demo_corpus.render import p
from scripts.generate_demo_pdfs import BUILDERS, generate_document

# --- Faits et mise en forme --------------------------------------------------------


def test_mise_en_forme_francaise():
    assert fcfa(500_000) == "500 000 FCFA"
    assert pct(21) == "21 %"
    assert pct(1.5) == "1,5 %"
    assert decimal_fr(0.0175, 4) == "0,0175"
    assert decimal_fr(100, 0) == "100"


def test_catalogue_complet_et_coherent():
    assert sorted(DOCUMENTS) == list(range(1, 26))
    assert sum(spec.pages for spec in DOCUMENTS.values()) == 141
    assert len({spec.reference for spec in DOCUMENTS.values()}) == 25
    for key in ANSWER_KEYS:
        assert 1 <= key.page <= DOCUMENTS[key.document].pages


def test_cinquante_reponses_et_le_piege():
    labels = [(key.document, key.label) for key in ANSWER_KEYS]
    assert len(labels) == len(set(labels)) == 51
    assert (13, "piège") in labels


def test_grilles_aux_rubriques_identiques():
    old, new = GRIDS[2025], GRIDS[2026]
    assert [r.product for r in old.credit_rates] == [r.product for r in new.credit_rates]
    assert [s.service for s in old.services] == [s.service for s in new.services]
    assert old.agr_rate_pct != new.agr_rate_pct


@pytest.mark.parametrize("year", [2025, 2026])
def test_mensualite_juste(year):
    """La somme des mensualités actualisées au taux mensuel redonne le capital emprunté."""
    grid = GRIDS[year]
    example = compute_loan_example(grid)
    t = grid.agr_rate_pct / 100 / 12
    present_value = sum(
        example.installment / (1 + t) ** k for k in range(1, EXAMPLE_LOAN_MONTHS + 1)
    )
    assert present_value == pytest.approx(EXAMPLE_LOAN_FCFA, abs=EXAMPLE_LOAN_MONTHS)
    assert example.total_cost == example.interest + example.dossier_fee + example.insurance


def test_exemple_2026_valeurs_connues():
    example = compute_loan_example(GRIDS[2026])
    assert example.installment == 27_934
    assert example.total_repaid == 335_208
    assert example.total_cost == 41_958


# --- Outils du vérificateur ----------------------------------------------------------


@pytest.mark.parametrize(
    ("needle", "text", "expected"),
    [
        ("500 000 FCFA", "plafond de 500 000 fcfa.", 1),
        ("500 000 FCFA", "plafond de 1 500 000 fcfa.", 0),
        ("2 % du montant du crédit", "1,2 % du montant du crédit", 0),
        ("2 % du montant du crédit", "12 % du montant du crédit", 0),
        ("2 % du montant du crédit", "soit 2 % du montant du crédit", 1),
        ("4 jours ouvrables", "14 jours ouvrables", 0),
        ("18 400", "18 4000 clients", 0),
        ("18 400", "18 400 000 fcfa", 0),
        ("18 400", "soit 18 400 clients actifs", 1),
    ],
)
def test_motif_de_recherche_sans_faux_positif(needle, text, expected):
    assert len(verifier.needle_pattern(needle).findall(text)) == expected


def test_masquage_des_chiffres():
    assert verifier.mask_numbers("1 500 FCFA, 0,0175 et 2026") == "# fcfa, # et #"
    assert verifier.mask_numbers("21 % par an") == verifier.mask_numbers("24 % par an")


# --- Corpus généré -------------------------------------------------------------------


@pytest.fixture(scope="module")
def corpus_sain(tmp_path_factory):
    dossier = tmp_path_factory.mktemp("corpus")
    for number in BUILDERS:
        generate_document(number, dossier)
    return dossier


def _injecter(corpus_sain, tmp_path, document, transform):
    cible = tmp_path / "corpus"
    shutil.copytree(corpus_sain, cible)
    generate_document(document, cible, transform)
    return verifier.verify_corpus([cible])


def test_corpus_sain_sans_erreur(corpus_sain):
    report = verifier.verify_corpus([corpus_sain])
    assert report.issues == []
    assert all(fill >= verifier.MIN_FILL for fills in report.fills.values() for fill in fills)


def test_detecte_une_reponse_a_la_mauvaise_page(corpus_sain, tmp_path):
    report = _injecter(corpus_sain, tmp_path, 10, verifier._swap_pages_4_and_5)
    details = [i.detail for i in report.issues if i.check == verifier.CHECK_ANSWERS]
    assert any("trouvé : n° 10 p. 5" in detail for detail in details)


def test_detecte_une_reponse_en_double(corpus_sain, tmp_path):
    report = _injecter(corpus_sain, tmp_path, 14, verifier._duplicate_answer)
    details = [i.detail for i in report.issues if i.check == verifier.CHECK_ANSWERS]
    assert any("n° 10 p. 4, n° 14 p. 4" in detail for detail in details)


def test_detecte_un_pied_de_page_indexe(corpus_sain, tmp_path):
    report = _injecter(corpus_sain, tmp_path, 10, verifier._index_footer)
    assert any(i.check == verifier.CHECK_INDEXED for i in report.issues)


def test_detecte_une_rubrique_differente_entre_grilles(corpus_sain, tmp_path):
    def rubrique_en_plus(pages):
        pages[2].insert(1, p("Frais de tenue de compte des associations : sur devis."))
        return pages

    report = _injecter(corpus_sain, tmp_path, 13, rubrique_en_plus)
    assert [i.check for i in report.issues] == [verifier.CHECK_GRIDS]


def test_detecte_une_fuite_vers_un_document_absent(corpus_sain, tmp_path):
    def fuite(pages):
        pages[1].insert(1, p("Les salaires sont versés le 25 de chaque mois."))
        return pages

    report = _injecter(corpus_sain, tmp_path, 10, fuite)
    assert any(i.document == 4 and i.check == verifier.CHECK_ANSWERS for i in report.issues)


def test_detecte_un_document_trop_vide(corpus_sain, tmp_path):
    def vider(pages):
        pages[1] = pages[1][:2]
        return pages

    report = _injecter(corpus_sain, tmp_path, 10, vider)
    assert any(i.check == verifier.CHECK_FILL for i in report.issues)


def test_auto_test_complet(tmp_path):
    assert all(ok for _, ok in verifier.run_self_test(tmp_path))
