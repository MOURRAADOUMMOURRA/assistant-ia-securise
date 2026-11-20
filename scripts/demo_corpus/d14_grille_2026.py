"""Document n° 14 — Grille des taux et frais 2026 (TAR-2026, 4 pages), version en vigueur."""

from scripts.demo_corpus.facts import GRIDS
from scripts.demo_corpus.grille import build_grid_pages
from scripts.demo_corpus.render import Page


def build_pages() -> list[Page]:
    """Construit les 4 pages de la grille 2026."""
    return build_grid_pages(GRIDS[2026])
