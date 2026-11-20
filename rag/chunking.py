"""Découpage des pages en morceaux (chunks) qui ne débordent jamais sur deux pages.

Chaque page est découpée séparément. Un morceau fait au plus `chunk_size`
caractères ; on coupe de préférence à une fin de paragraphe, de ligne ou de
phrase. Deux morceaux voisins partagent environ `chunk_overlap` caractères, pour
qu'une information à cheval sur une coupure reste lisible dans au moins l'un d'eux.
"""

import re
from collections.abc import Iterable

from rag.models import Chunk, Page

SEPARATORS: tuple[str, ...] = ("\n\n", "\n", ". ", "; ", ", ", " ")
"""Coupures préférées, de la plus naturelle à la moins naturelle."""

MIN_FILL_RATIO = 0.6
"""Un morceau est rempli au moins à 60 % avant qu'on accepte une coupure naturelle."""

_WHITESPACE = re.compile(r"\s")


def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Découpe un texte en morceaux d'au plus `chunk_size` caractères, avec chevauchement."""
    if chunk_overlap >= chunk_size:
        raise ValueError("Le chevauchement doit être inférieur à la taille d'un morceau.")
    text = text.strip()
    pieces: list[str] = []
    start = 0
    while text and start < len(text):
        if len(text) - start <= chunk_size:
            pieces.append(text[start:])
            break
        end = _find_cut(text, start, start + chunk_size)
        pieces.append(text[start:end])
        start = _next_start(text, start, end, chunk_overlap)
    return [stripped for stripped in (piece.strip() for piece in pieces) if stripped]


def chunk_page(page: Page, chunk_size: int, chunk_overlap: int) -> list[Chunk]:
    """Découpe une page en morceaux, chacun rattaché à cette seule page."""
    return [
        Chunk(
            chunk_id=make_chunk_id(page.doc_id, page.page_number, index),
            doc_id=page.doc_id,
            title=page.title,
            source_path=page.source_path,
            page_number=page.page_number,
            page_count=page.page_count,
            chunk_index=index,
            text=piece,
        )
        for index, piece in enumerate(split_text(page.text, chunk_size, chunk_overlap))
    ]


def chunk_pages(pages: Iterable[Page], chunk_size: int, chunk_overlap: int) -> list[Chunk]:
    """Découpe toutes les pages, page par page."""
    return [chunk for page in pages for chunk in chunk_page(page, chunk_size, chunk_overlap)]


def make_chunk_id(doc_id: str, page_number: int, chunk_index: int) -> str:
    """Identifiant stable et unique d'un morceau, ex. « d10:p004:c01 »."""
    return f"{doc_id}:p{page_number:03d}:c{chunk_index:02d}"


def _find_cut(text: str, start: int, limit: int) -> int:
    """Position de coupure : la dernière coupure naturelle avant `limit`, sinon `limit`."""
    floor = start + int((limit - start) * MIN_FILL_RATIO)
    for separator in SEPARATORS:
        position = text.rfind(separator, floor, limit)
        if position != -1:
            return position + len(separator)
    return limit


def _next_start(text: str, start: int, end: int, chunk_overlap: int) -> int:
    """Début du morceau suivant : recule de `chunk_overlap`, puis avance au début d'un mot."""
    candidate = max(end - chunk_overlap, start + 1)
    if _WHITESPACE.match(text[candidate - 1]):
        return candidate
    match = _WHITESPACE.search(text, candidate, end)
    return match.end() if match else candidate
