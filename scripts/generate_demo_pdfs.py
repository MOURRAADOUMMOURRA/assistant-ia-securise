"""Génération des PDF du corpus de démonstration.

Usage, depuis la racine du projet :

    .venv\\Scripts\\python -m scripts.generate_demo_pdfs --only 10 14
    .venv\\Scripts\\python -m scripts.generate_demo_pdfs --only 13 --out data\\tmp_corpus

Pour chaque document, le générateur écrit le PDF, vérifie son nombre de pages et
mesure le remplissage de chaque page ; il signale toute page remplie à moins de 70 %.
"""

import argparse
import sys
from collections.abc import Callable, Iterable
from pathlib import Path

import pymupdf

from config import PROJECT_ROOT
from scripts.demo_corpus import (
    d01_reglement_interieur,
    d02_demande_conges,
    d03_recrutement_integration,
    d04_remuneration_avantages,
    d05_frais_mission,
    d06_charte_informatique,
    d07_plan_formation_2026,
    d08_consignes_incendie,
    d09_note_horaires_ramadan,
    d10_octroi_credit,
    d13_grille_2025,
    d14_grille_2026,
)
from scripts.demo_corpus.facts import DOCUMENTS
from scripts.demo_corpus.render import Page, render_document
from scripts.verify_demo_pdfs import MIN_FILL, page_fill_ratios

BUILDERS: dict[int, Callable[[], list[Page]]] = {
    1: d01_reglement_interieur.build_pages,
    2: d02_demande_conges.build_pages,
    3: d03_recrutement_integration.build_pages,
    4: d04_remuneration_avantages.build_pages,
    5: d05_frais_mission.build_pages,
    6: d06_charte_informatique.build_pages,
    7: d07_plan_formation_2026.build_pages,
    8: d08_consignes_incendie.build_pages,
    9: d09_note_horaires_ramadan.build_pages,
    10: d10_octroi_credit.build_pages,
    13: d13_grille_2025.build_pages,
    14: d14_grille_2026.build_pages,
}
"""Documents disponibles : numéro → fonction qui construit ses pages."""

DEFAULT_OUT = PROJECT_ROOT / "demo_docs"

Transform = Callable[[list[Page]], list[Page]]


def generate_document(number: int, out_dir: Path, transform: Transform | None = None) -> Path:
    """Génère un document ; `transform` permet d'injecter une erreur (auto-test)."""
    spec = DOCUMENTS[number]
    pages = BUILDERS[number]()
    if len(pages) != spec.pages:
        raise ValueError(f"n° {number} : {len(pages)} pages construites au lieu de {spec.pages}")
    if transform:
        pages = transform(pages)
    return render_document(spec, pages, out_dir / spec.filename)


def describe(number: int, path: Path) -> tuple[str, bool]:
    """Bilan d'un document généré : pages et remplissage ; faux si une règle n'est pas tenue."""
    spec = DOCUMENTS[number]
    with pymupdf.open(path) as document:
        page_count = len(document)
    fills = page_fill_ratios(path)
    low = [index for index, fill in enumerate(fills, start=1) if fill < MIN_FILL]
    pages_ok = page_count == spec.pages
    line = (
        f"n° {number:02d} {path.name} : {page_count}/{spec.pages} pages, remplissage "
        + " ".join(f"{fill:.0%}" for fill in fills)
    )
    if not pages_ok:
        line += "  <-- NOMBRE DE PAGES INCORRECT (contenu qui déborde ?)"
    if low:
        line += f"  <-- pages sous 70 % : {', '.join(map(str, low))}"
    return line, pages_ok and not low


def main(argv: Iterable[str] | None = None) -> int:
    """Génère les documents demandés et affiche leur bilan."""
    sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description="Génère les PDF du corpus de démonstration.")
    parser.add_argument("--only", type=int, nargs="+", choices=sorted(BUILDERS))
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args(list(argv) if argv is not None else None)
    all_ok = True
    for number in args.only or sorted(BUILDERS):
        line, ok = describe(number, generate_document(number, args.out))
        print(line)
        all_ok = all_ok and ok
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
