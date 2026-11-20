"""Lecture des PDF page par page et retrait des en-têtes et pieds de page répétés.

Règle de retrait : on examine les 3 premières et les 3 dernières lignes de chaque
page. Une ligne est « répétée » si elle figure dans cette zone sur au moins la
moitié des pages, et sur au moins 2 pages. On la retire uniquement depuis le bord
de la page, en s'arrêtant à la première ligne non répétée. Les chiffres ne sont
neutralisés que dans les lignes de numérotation (« Page 2 / 8 »), si bien que
« Article 3 » et « Article 4 » restent distincts.
"""

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

from rag.errors import UnreadablePdfError, UnsupportedFormatError
from rag.logging_setup import get_logger
from rag.models import Page

EDGE_LINES = 3
MIN_REPEATED_PAGES = 2
PDF_SUFFIX = ".pdf"
NUMBER_PLACEHOLDER = "#"

_PAGE_NUMBERING = (
    re.compile(r"\bpage\s+\d+\s*(?:/|sur|de)\s*\d+\b", re.IGNORECASE),
    re.compile(r"^[-–]?\s*\d+\s*(?:/\s*\d+)?\s*[-–]?$"),
)
_DIGITS = re.compile(r"\d+")
_HORIZONTAL_SPACES = re.compile(r"[ \t  ]+")
_FILENAME_PREFIX = re.compile(r"^d?\d+[\s_-]+", re.IGNORECASE)
_FILENAME_SEPARATORS = re.compile(r"[\s_-]+")

logger = get_logger(__name__)


@dataclass
class IngestionResult:
    """Résultat de la lecture d'un dossier : pages lues et fichiers écartés."""

    pages: list[Page] = field(default_factory=list)
    failures: dict[Path, str] = field(default_factory=dict)

    @property
    def document_count(self) -> int:
        """Nombre de documents lus avec succès."""
        return len({page.doc_id for page in self.pages})


def normalize_line(line: str) -> str:
    """Remplace les espaces multiples ou insécables par une espace simple."""
    return _HORIZONTAL_SPACES.sub(" ", line).strip()


def is_page_numbering(line: str) -> bool:
    """Indique si une ligne est une numérotation de page (« Page 2 / 8 », « 3 »)."""
    return any(pattern.search(line) for pattern in _PAGE_NUMBERING)


def edge_key(line: str) -> str:
    """Clé de comparaison d'une ligne de bord : chiffres neutralisés si numérotation."""
    return _DIGITS.sub(NUMBER_PLACEHOLDER, line) if is_page_numbering(line) else line


def find_repeated_edge_lines(pages_lines: list[list[str]]) -> set[str]:
    """Renvoie les clés des lignes répétées dans la zone de bord des pages."""
    min_pages = max(MIN_REPEATED_PAGES, math.ceil(len(pages_lines) / 2))
    counter: Counter[str] = Counter()
    for lines in pages_lines:
        zone = lines[:EDGE_LINES] + lines[-EDGE_LINES:]
        counter.update({edge_key(line) for line in zone})
    return {key for key, count in counter.items() if count >= min_pages}


def strip_page_edges(lines: list[str], repeated: set[str]) -> list[str]:
    """Retire les lignes répétées depuis le haut et le bas d'une page, sans dépasser la zone."""
    start = 0
    while start < min(EDGE_LINES, len(lines)) and edge_key(lines[start]) in repeated:
        start += 1
    end = len(lines)
    while end > max(start, len(lines) - EDGE_LINES) and edge_key(lines[end - 1]) in repeated:
        end -= 1
    return lines[start:end]


def remove_repeated_edges(pages_lines: list[list[str]]) -> list[list[str]]:
    """Retire les en-têtes et pieds de page répétés de toutes les pages d'un document."""
    repeated = find_repeated_edge_lines(pages_lines)
    return [strip_page_edges(lines, repeated) for lines in pages_lines]


def title_from_filename(path: Path) -> str:
    """Déduit un titre lisible du nom de fichier (« d10_octroi_credit » → « Octroi credit »)."""
    stem = _FILENAME_PREFIX.sub("", path.stem)
    words = _FILENAME_SEPARATORS.sub(" ", stem).strip() or path.stem
    return words[0].upper() + words[1:]


def load_pdf(path: Path, doc_id: str | None = None) -> list[Page]:
    """Lit un PDF et renvoie ses pages nettoyées, numérotées à partir de 1.

    Lève `UnsupportedFormatError` si le fichier n'est pas un PDF, et
    `UnreadablePdfError` s'il est introuvable, endommagé, protégé ou sans texte.
    """
    if path.suffix.lower() != PDF_SUFFIX:
        raise UnsupportedFormatError
    metadata_title, raw_pages = _read_pdf(path)
    cleaned = remove_repeated_edges(raw_pages)
    if not any(cleaned):
        raise UnreadablePdfError(
            f"« {path.name} » ne contient pas de texte (document scanné ?). "
            "Seuls les PDF texte sont pris en charge."
        )
    title = metadata_title or title_from_filename(path)
    page_count = len(cleaned)
    return [
        Page(
            doc_id=doc_id or path.stem,
            title=title,
            source_path=path,
            page_number=number,
            page_count=page_count,
            text="\n".join(lines),
        )
        for number, lines in enumerate(cleaned, start=1)
    ]


def load_directory(docs_dir: Path) -> IngestionResult:
    """Lit tous les PDF d'un dossier ; les fichiers refusés sont listés, pas bloquants."""
    result = IngestionResult()
    for path in sorted(docs_dir.iterdir()):
        if not path.is_file():
            continue
        try:
            result.pages.extend(load_pdf(path))
        except (UnsupportedFormatError, UnreadablePdfError) as error:
            result.failures[path] = error.user_message
            logger.warning("Fichier écarté : %s (%s)", path.name, error.user_message)
    return result


def _read_pdf(path: Path) -> tuple[str, list[list[str]]]:
    """Ouvre le PDF et renvoie son titre (métadonnées) et les lignes de chaque page."""
    if not path.is_file():
        raise UnreadablePdfError(f"Fichier introuvable : « {path.name} ».")
    try:
        with pymupdf.open(path) as document:
            if document.needs_pass:
                raise UnreadablePdfError(f"« {path.name} » est protégé par un mot de passe.")
            title = normalize_line((document.metadata or {}).get("title") or "")
            pages = [_page_lines(page) for page in document]
    except (RuntimeError, ValueError) as error:
        raise UnreadablePdfError(f"« {path.name} » est endommagé ou illisible.") from error
    return title, pages


def _page_lines(page: pymupdf.Page) -> list[str]:
    """Extrait les lignes non vides d'une page, dans l'ordre de lecture."""
    text = page.get_text("text", sort=True)
    return [line for line in (normalize_line(raw) for raw in text.splitlines()) if line]
