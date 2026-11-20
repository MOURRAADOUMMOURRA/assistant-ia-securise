"""Fabrique de petits PDF de test, avec en-tête, corps et pied de page."""

from pathlib import Path

import pymupdf

HEADER = "Kouri Épargne & Crédit S.A. — CR-PRO-01"
FOOTER = "Document fictif – démonstration ZakiCortex"
LINE_HEIGHT = 16


def write_pdf(
    path: Path,
    bodies: list[list[str]],
    title: str | None = "Document de test",
    with_edges: bool = True,
) -> Path:
    """Écrit un PDF dont chaque page contient les lignes de `bodies`.

    Avec `with_edges`, chaque page reçoit l'en-tête, le pied de page et
    « Page i / n », comme les documents du corpus de démonstration.
    """
    document = pymupdf.open()
    total = len(bodies)
    for number, body in enumerate(bodies, start=1):
        page = document.new_page()
        lines = [HEADER, *body, FOOTER, f"Page {number} / {total}"] if with_edges else body
        for index, line in enumerate(lines):
            page.insert_text((72, 60 + index * LINE_HEIGHT), line, fontsize=10)
    if title is not None:
        document.set_metadata({"title": title})
    document.save(path)
    document.close()
    return path
