"""Rendu d'une page de PDF en image PNG, avec le passage utilisé surligné en jaune.

Le passage (le texte du morceau retrouvé) est recherché mot à mot dans la page : les
suites d'au moins trois mots consécutifs communs sont surlignées, ligne par ligne.
Tout se fait en mémoire avec PyMuPDF : le fichier PDF d'origine n'est jamais modifié.
"""

from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf

from rag.errors import AssistantError, UnreadablePdfError
from rag.textutils import normalize_for_matching

DEFAULT_DPI = 110
MIN_MATCH_WORDS = 3
LINE_TOLERANCE = 3.0
HIGHLIGHT_COLOR = (1.0, 0.92, 0.23)


@dataclass(frozen=True)
class PageImage:
    """Image PNG d'une page et nombre de zones surlignées."""

    png: bytes
    page_number: int
    highlights: int


def render_highlighted_page(
    pdf_path: Path,
    page_number: int,
    passage: str,
    docs_dir: Path,
    dpi: int = DEFAULT_DPI,
) -> PageImage:
    """Rend la page `page_number` (à partir de 1) en PNG, avec `passage` surligné.

    Le fichier doit se trouver dans `docs_dir` : aucun autre fichier du disque ne peut
    être affiché par ce biais.
    """
    path = _checked_path(pdf_path, docs_dir)
    try:
        with pymupdf.open(path) as document:
            if not 1 <= page_number <= len(document):
                raise AssistantError(f"La page {page_number} n'existe pas dans « {path.name} ».")
            page = document[page_number - 1]
            rectangles = find_passage_rects(page, passage)
            for rect in rectangles:
                annotation = page.add_highlight_annot(rect)
                annotation.set_colors(stroke=HIGHLIGHT_COLOR)
                annotation.update()
            png = page.get_pixmap(dpi=dpi).tobytes("png")
    except (RuntimeError, ValueError) as error:
        raise UnreadablePdfError(f"Impossible d'afficher « {path.name} ».") from error
    return PageImage(png=png, page_number=page_number, highlights=len(rectangles))


def find_passage_rects(page: pymupdf.Page, passage: str) -> list[pymupdf.Rect]:
    """Rectangles (un par ligne) des mots de la page qui correspondent au passage."""
    words = _page_tokens(page)
    wanted = normalize_for_matching(passage).split()
    if not words or not wanted:
        return []
    matcher = SequenceMatcher(None, [token for token, _ in words], wanted, autojunk=False)
    matched = [
        words[index][1]
        for block in matcher.get_matching_blocks()
        if block.size >= MIN_MATCH_WORDS
        for index in range(block.a, block.a + block.size)
    ]
    return _merge_by_line(matched)


def _page_tokens(page: pymupdf.Page) -> list[tuple[str, pymupdf.Rect]]:
    """Mots de la page dans l'ordre de lecture, normalisés, avec leur rectangle."""
    tokens: list[tuple[str, pymupdf.Rect]] = []
    for x0, y0, x1, y1, text, *_ in page.get_text("words", sort=True):
        rect = pymupdf.Rect(x0, y0, x1, y1)
        tokens.extend((token, rect) for token in normalize_for_matching(text).split())
    return tokens


def _merge_by_line(rects: list[pymupdf.Rect]) -> list[pymupdf.Rect]:
    """Fusionne les rectangles de mots situés sur une même ligne."""
    merged: list[pymupdf.Rect] = []
    for rect in sorted(rects, key=lambda r: (round(r.y0), r.x0)):
        last = merged[-1] if merged else None
        if last is not None and abs(last.y0 - rect.y0) <= LINE_TOLERANCE:
            merged[-1] = last | rect
        else:
            merged.append(pymupdf.Rect(rect))
    return merged


def _checked_path(pdf_path: Path, docs_dir: Path) -> Path:
    """Vérifie que le PDF demandé est bien un fichier du dossier des documents."""
    path = pdf_path.resolve()
    if not path.is_relative_to(docs_dir.resolve()) or not path.is_file():
        raise AssistantError("Ce document n'est pas disponible.")
    return path
