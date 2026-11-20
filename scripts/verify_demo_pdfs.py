"""Contrôles automatiques du corpus de démonstration.

Usage, depuis la racine du projet :

    .venv\\Scripts\\python -m scripts.verify_demo_pdfs
    .venv\\Scripts\\python -m scripts.verify_demo_pdfs --extra-dir data\\tmp_corpus
    .venv\\Scripts\\python -m scripts.verify_demo_pdfs --self-test

Contrôles, pour chaque PDF présent :
- titre dans les métadonnées ;
- nombre de pages conforme ;
- en-tête, pied de page et numérotation présents sur chaque page ;
- en-tête et pied de page absents du texte indexé (après ingestion) ;
- remplissage d'au moins 70 % par page ;
- chaque réponse attendue à sa page et unique dans le corpus, et aucune réponse
  d'un document absent qui apparaîtrait déjà ailleurs (fuite) ;
- grilles 2025 et 2026 aux rubriques identiques une fois les chiffres masqués.

`--self-test` injecte trois erreurs (réponse à la mauvaise page, doublon, pied de
page indexé) et vérifie que chacune est détectée.
"""

import argparse
import re
import shutil
import sys
import tempfile
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf

from config import PROJECT_ROOT
from rag.ingestion import load_pdf
from rag.textutils import normalize_for_matching
from scripts.demo_corpus.facts import (
    ANSWER_KEYS,
    DOCUMENTS,
    FIRST_LOAN_CAP_FCFA,
    FOOTER_TEXT,
    INSTITUTION_NAME,
    AnswerKey,
    DocumentSpec,
    fcfa,
)
from scripts.demo_corpus.render import FRAME_BOTTOM_FROM_TOP, FRAME_HEIGHT, FRAME_TOP_FROM_TOP

MIN_FILL = 0.70
GRID_DOCUMENTS = (13, 14)
DEFAULT_DOCS_DIR = PROJECT_ROOT / "demo_docs"

CHECK_UNKNOWN = "fichier inconnu"
CHECK_METADATA = "métadonnées"
CHECK_PAGES = "nombre de pages"
CHECK_EDGES = "en-tête et pied de page"
CHECK_INDEXED = "texte indexé"
CHECK_FILL = "remplissage"
CHECK_ANSWERS = "réponses"
CHECK_GRIDS = "rubriques 2025/2026"

_PAGE_NUMBERING = re.compile(r"\bpage \d+ / \d+\b")
_NUMBER_RUN = re.compile(r"\d+(?:[ ,.]\d+)*")
_TOLERANCE = 1.0


@dataclass(frozen=True)
class Issue:
    """Erreur détectée : document concerné, contrôle et détail."""

    document: int | None
    check: str
    detail: str


@dataclass
class Report:
    """Résultat de la vérification d'un corpus."""

    documents: dict[int, Path] = field(default_factory=dict)
    fills: dict[int, list[float]] = field(default_factory=dict)
    issues: list[Issue] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """Vrai si aucun contrôle n'a échoué."""
        return not self.issues


# --- Fonctions de mesure ---------------------------------------------------------


def page_fill_ratios(path: Path) -> list[float]:
    """Mesure, pour chaque page, la part de la hauteur utile occupée par le contenu."""
    with pymupdf.open(path) as document:
        return [_page_fill(page) for page in document]


def needle_pattern(needle: str) -> re.Pattern[str]:
    """Expression qui retrouve un extrait sans le confondre avec un nombre plus long.

    « 500 000 FCFA » ne correspond pas à « 1 500 000 FCFA », ni « 2 % » à « 1,2 % ».
    """
    text = normalize_for_matching(needle)
    prefix = r"(?<![\d,])(?<!\d )" if text[0].isdigit() else r"(?<!\w)"
    suffix = r"(?!\d)(?![ ,.]\d)" if text[-1].isdigit() else r"(?!\w)" if text[-1].isalnum() else ""
    return re.compile(prefix + re.escape(text) + suffix)


def mask_numbers(text: str) -> str:
    """Remplace chaque nombre (« 1 500 », « 0,0175 », « 2026 ») par « # »."""
    return _NUMBER_RUN.sub("#", normalize_for_matching(text))


# --- Vérification ----------------------------------------------------------------


def verify_corpus(directories: Sequence[Path]) -> Report:
    """Vérifie tous les PDF des dossiers donnés et renvoie le rapport."""
    report = Report()
    _collect(directories, report)
    indexed: dict[int, list[str]] = {}
    for number, path in sorted(report.documents.items()):
        spec = DOCUMENTS[number]
        _check_file(spec, path, report)
        indexed[number] = _check_indexed(spec, path, report)
    _check_answers(indexed, report)
    _check_grids(indexed, report)
    missing = sorted(set(DOCUMENTS) - set(report.documents))
    if missing:
        report.notes.append(f"Documents pas encore générés : {', '.join(map(str, missing))}")
    return report


def _collect(directories: Sequence[Path], report: Report) -> None:
    """Associe chaque PDF trouvé à sa fiche du catalogue ; signale les fichiers inconnus."""
    by_name = {spec.filename: spec.number for spec in DOCUMENTS.values()}
    for directory in directories:
        for path in sorted(directory.glob("*.pdf")):
            number = by_name.get(path.name)
            if number is None:
                report.issues.append(Issue(None, CHECK_UNKNOWN, path.name))
            else:
                report.documents[number] = path


def _check_file(spec: DocumentSpec, path: Path, report: Report) -> None:
    """Contrôle métadonnées, nombre de pages, en-tête, pied de page et remplissage."""
    with pymupdf.open(path) as document:
        title = (document.metadata or {}).get("title", "")
        if title != spec.title:
            report.issues.append(Issue(spec.number, CHECK_METADATA, f"titre lu : {title!r}"))
        if len(document) != spec.pages:
            report.issues.append(
                Issue(spec.number, CHECK_PAGES, f"{len(document)} pages au lieu de {spec.pages}")
            )
        for index, page in enumerate(document, start=1):
            _check_page_edges(spec, index, len(document), page.get_text("text"), report)
    fills = page_fill_ratios(path)
    report.fills[spec.number] = fills
    for index, fill in enumerate(fills, start=1):
        if fill < MIN_FILL:
            report.issues.append(
                Issue(spec.number, CHECK_FILL, f"page {index} remplie à {fill:.0%} (< 70 %)")
            )


def _check_page_edges(
    spec: DocumentSpec, index: int, total: int, text: str, report: Report
) -> None:
    """Vérifie la présence de l'en-tête, du pied de page et de la numérotation sur une page."""
    expected = (INSTITUTION_NAME, f"Réf. {spec.reference}", FOOTER_TEXT, f"Page {index} / {total}")
    normalized = normalize_for_matching(text)
    for element in expected:
        if normalize_for_matching(element) not in normalized:
            report.issues.append(
                Issue(spec.number, CHECK_EDGES, f"page {index} : « {element} » absent")
            )


def _check_indexed(spec: DocumentSpec, path: Path, report: Report) -> list[str]:
    """Ingère le PDF comme le moteur RAG et vérifie qu'en-tête et pied ont disparu."""
    pages = [normalize_for_matching(page.text) for page in load_pdf(path)]
    forbidden = (
        normalize_for_matching(FOOTER_TEXT),
        normalize_for_matching(f"Réf. {spec.reference}"),
    )
    for index, text in enumerate(pages, start=1):
        leftovers = [item for item in forbidden if item in text]
        if _PAGE_NUMBERING.search(text):
            leftovers.append("numérotation « Page i / n »")
        for leftover in leftovers:
            report.issues.append(
                Issue(spec.number, CHECK_INDEXED, f"page {index} : « {leftover} » encore présent")
            )
    return pages


def _check_answers(indexed: dict[int, list[str]], report: Report) -> None:
    """Chaque réponse doit apparaître une seule fois, à sa page ; aucune fuite ailleurs."""
    for key in ANSWER_KEYS:
        found = _find(key, indexed)
        expected = [(key.document, key.page)] if key.document in indexed else []
        if found != expected:
            report.issues.append(Issue(key.document, CHECK_ANSWERS, _describe(key, found)))


def _find(key: AnswerKey, indexed: dict[int, list[str]]) -> list[tuple[int, int]]:
    """Liste (document, page) de chaque occurrence de l'extrait attendu."""
    pattern = needle_pattern(key.needle)
    return [
        (number, index)
        for number, pages in sorted(indexed.items())
        for index, text in enumerate(pages, start=1)
        for _ in pattern.finditer(text)
    ]


def _describe(key: AnswerKey, found: list[tuple[int, int]]) -> str:
    """Explique un écart entre les occurrences trouvées et l'emplacement attendu."""
    places = ", ".join(f"n° {doc} p. {page}" for doc, page in found) or "nulle part"
    return (
        f"{key.label} « {key.needle} » attendu une fois en n° {key.document} p. {key.page}, "
        f"trouvé : {places}"
    )


def _check_grids(indexed: dict[int, list[str]], report: Report) -> None:
    """Compare les grilles 2025 et 2026 une fois les chiffres masqués."""
    if not all(number in indexed for number in GRID_DOCUMENTS):
        report.notes.append("Contrôle des rubriques 2025/2026 ignoré : il faut les n° 13 et 14.")
        return
    old, new = (mask_numbers(" ".join(indexed[number])) for number in GRID_DOCUMENTS)
    if old != new:
        report.issues.append(Issue(14, CHECK_GRIDS, _first_difference(old, new)))


def _first_difference(old: str, new: str) -> str:
    """Décrit la première différence entre deux textes masqués."""
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag != "equal":
            before = old[max(0, i1 - 40) : i2 + 40]
            after = new[max(0, j1 - 40) : j2 + 40]
            return f"2025 : « {before} » / 2026 : « {after} »"
    return "textes différents"


def _page_fill(page: pymupdf.Page) -> float:
    """Hauteur occupée (texte et cadres) dans la zone de contenu, en part de cette zone."""
    bottoms = [block[3] for block in page.get_text("blocks")]
    bottoms += [drawing["rect"].y1 for drawing in page.get_drawings()]
    inside = [
        bottom
        for bottom in bottoms
        if FRAME_TOP_FROM_TOP - _TOLERANCE <= bottom <= FRAME_BOTTOM_FROM_TOP + _TOLERANCE
    ]
    if not inside:
        return 0.0
    return (max(inside) - FRAME_TOP_FROM_TOP) / FRAME_HEIGHT


# --- Auto-test du vérificateur : injection d'erreurs volontaires --------------------


@dataclass(frozen=True)
class Injection:
    """Erreur injectée volontairement et contrôle qui doit la détecter."""

    label: str
    document: int
    expected_check: str


INJECTIONS: tuple[Injection, ...] = (
    Injection(
        "Réponse déplacée à la mauvaise page (pages 4 et 5 du n° 10 inversées)", 10, CHECK_ANSWERS
    ),
    Injection(
        "Réponse recopiée dans un autre document (plafond du n° 10 dans le n° 14)",
        14,
        CHECK_ANSWERS,
    ),
    Injection(
        "Pied de page indexé (mention recopiée au milieu d'une page du n° 10)", 10, CHECK_INDEXED
    ),
)


def run_self_test(work_dir: Path) -> list[tuple[str, bool]]:
    """Génère un corpus sain, vérifie qu'il passe, puis que chaque erreur injectée est vue."""
    from scripts.generate_demo_pdfs import generate_document

    base = work_dir / "sain"
    for number in (10, 13, 14):
        generate_document(number, base)
    results = [("Corpus sain : aucune erreur", verify_corpus([base]).ok)]
    for index, injection in enumerate(INJECTIONS, start=1):
        target = work_dir / f"injection_{index}"
        shutil.copytree(base, target)
        generate_document(injection.document, target, _TRANSFORMS[index - 1])
        report = verify_corpus([target])
        detected = any(issue.check == injection.expected_check for issue in report.issues)
        results.append((injection.label, detected))
    return results


def _swap_pages_4_and_5(pages: list) -> list:
    """Inverse les pages 4 et 5 : la réponse de la page 4 passe en page 5."""
    pages[3], pages[4] = pages[4], pages[3]
    return pages


def _duplicate_answer(pages: list) -> list:
    """Recopie le plafond du premier crédit (réponse du n° 10) dans la page 4."""
    from scripts.demo_corpus.render import p

    pages[3].insert(1, p(f"Rappel : un premier crédit est plafonné à {fcfa(FIRST_LOAN_CAP_FCFA)}."))
    return pages


def _index_footer(pages: list) -> list:
    """Recopie la mention du pied de page au milieu de la page 3."""
    from scripts.demo_corpus.render import p

    pages[2].insert(3, p(FOOTER_TEXT))
    return pages


_TRANSFORMS = (_swap_pages_4_and_5, _duplicate_answer, _index_footer)


# --- Affichage -------------------------------------------------------------------


def format_report(report: Report) -> str:
    """Met en forme le rapport : un bilan par document, puis les erreurs et les notes."""
    lines = ["Vérification du corpus de démonstration", ""]
    for number, path in sorted(report.documents.items()):
        fills = report.fills.get(number, [])
        doc_issues = [issue for issue in report.issues if issue.document == number]
        status = "OK   " if not doc_issues else "ÉCHEC"
        fill_text = " ".join(f"{fill:.0%}" for fill in fills)
        lines.append(f"[{status}] n° {number:02d} {path.name} — remplissage : {fill_text}")
    if report.issues:
        lines += ["", "Erreurs :"]
        lines += [f"  - n° {i.document or '?'} [{i.check}] {i.detail}" for i in report.issues]
    lines += ["", *(f"Note : {note}" for note in report.notes)]
    lines.append(f"\n{len(report.documents)} documents vérifiés, {len(report.issues)} erreur(s).")
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    """Point d'entrée de la commande ; code de sortie 0 si tout est conforme."""
    sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description="Vérifie le corpus de démonstration.")
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    parser.add_argument("--extra-dir", type=Path, action="append", default=[])
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.self_test:
        with tempfile.TemporaryDirectory() as tmp:
            results = run_self_test(Path(tmp))
        for label, ok in results:
            print(f"[{'OK   ' if ok else 'ÉCHEC'}] {label}{'' if ok else ' — NON détecté'}")
        return 0 if all(ok for _, ok in results) else 1
    report = verify_corpus([args.docs_dir, *args.extra_dir])
    print(format_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
