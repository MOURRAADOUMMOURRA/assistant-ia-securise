"""Normalisation de texte pour les comparaisons (citations, refus, vérification du corpus)."""

import re

_APOSTROPHES = str.maketrans({"’": "'", "‘": "'", "`": "'", " ": " ", " ": " "})
_SPACES = re.compile(r"\s+")


def normalize_for_matching(text: str) -> str:
    """Minuscules, apostrophes droites, espaces insécables et retours à la ligne simplifiés."""
    return _SPACES.sub(" ", text.translate(_APOSTROPHES)).strip().casefold()
