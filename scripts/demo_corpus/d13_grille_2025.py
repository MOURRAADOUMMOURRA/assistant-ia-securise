"""Document n° 13 — Grille des taux et frais 2025 (TAR-2025, 4 pages).

Ancienne version, gardée dans le corpus pour le piège 2025/2026 : l'assistant doit
préférer la grille 2026 et signaler l'ancienne valeur.
"""

from scripts.demo_corpus.facts import GRIDS
from scripts.demo_corpus.grille import build_grid_pages
from scripts.demo_corpus.render import Page


def build_pages() -> list[Page]:
    """Construit les 4 pages de la grille 2025."""
    return build_grid_pages(GRIDS[2025])
