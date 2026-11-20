"""Mise en page commune du corpus : charte vert profond et or, en-tête, cartouche, pied.

Chaque document est décrit comme une liste de pages, chaque page comme une liste
de blocs (paragraphes, tableaux, encadrés). Un saut de page est inséré entre deux
pages : le contenu d'une page ne glisse donc jamais sur la suivante sans que le
nombre de pages change (ce que le vérificateur détecte).
"""

import re
from collections.abc import Sequence
from functools import partial
from pathlib import Path
from xml.sax.saxutils import escape

import pymupdf
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from scripts.demo_corpus.facts import (
    FOOTER_TEXT,
    HEAD_OFFICE_CITY,
    INSTITUTION_CATEGORY,
    INSTITUTION_NAME,
    DocumentSpec,
)

Page = list[Flowable]

# --- Géométrie (points PDF, 1 cm ≈ 28,35 pt) -----------------------------------

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 56.0
FRAME_WIDTH = PAGE_WIDTH - 2 * MARGIN_X
FRAME_BOTTOM = 70.0
FRAME_HEIGHT = 692.0
FRAME_TOP_FROM_TOP = PAGE_HEIGHT - FRAME_BOTTOM - FRAME_HEIGHT
"""Haut de la zone de contenu, mesuré depuis le haut de la page (repère de PyMuPDF)."""

FRAME_BOTTOM_FROM_TOP = PAGE_HEIGHT - FRAME_BOTTOM

# --- Charte --------------------------------------------------------------------

GREEN = colors.HexColor("#0F4C3A")
GREEN_LIGHT = colors.HexColor("#E8F1EC")
GOLD = colors.HexColor("#C9A23F")
GOLD_LIGHT = colors.HexColor("#FBF4E2")
INK = colors.HexColor("#1F2A26")
GREY = colors.HexColor("#5B6662")

_BOLD = re.compile(r"\*\*(.+?)\*\*")

STYLES: dict[str, ParagraphStyle] = {
    "title": ParagraphStyle(
        "title",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=GREEN,
        spaceAfter=4,
    ),
    "subtitle": ParagraphStyle(
        "subtitle",
        fontName="Helvetica-Oblique",
        fontSize=9.5,
        leading=13,
        textColor=GREY,
        spaceAfter=10,
    ),
    "h1": ParagraphStyle(
        "h1",
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=16,
        textColor=GREEN,
        spaceBefore=10,
        spaceAfter=5,
    ),
    "h2": ParagraphStyle(
        "h2",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=GREEN,
        spaceBefore=6,
        spaceAfter=3,
    ),
    "body": ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=INK,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    ),
    "bullet": ParagraphStyle(
        "bullet",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=INK,
        leftIndent=14,
        bulletIndent=3,
        spaceAfter=3,
    ),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=9, leading=11.5, textColor=INK),
    "cell_head": ParagraphStyle(
        "cell_head",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11.5,
        textColor=colors.white,
    ),
    "callout_title": ParagraphStyle(
        "callout_title",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=GREEN,
        spaceAfter=2,
    ),
    "faq_q": ParagraphStyle(
        "faq_q",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=GREEN,
        spaceBefore=4,
        spaceAfter=1,
    ),
}


def markup(text: str) -> str:
    """Échappe le texte pour reportlab et convertit **gras** en balises <b>."""
    return _BOLD.sub(r"<b>\1</b>", escape(text))


# --- Blocs de contenu ----------------------------------------------------------


def h1(text: str) -> Paragraph:
    """Titre de section."""
    return Paragraph(markup(text), STYLES["h1"])


def h2(text: str) -> Paragraph:
    """Titre de sous-section."""
    return Paragraph(markup(text), STYLES["h2"])


def p(text: str) -> Paragraph:
    """Paragraphe de texte courant (justifié)."""
    return Paragraph(markup(text), STYLES["body"])


def bullets(items: Sequence[str]) -> list[Flowable]:
    """Liste à puces."""
    return [Paragraph(markup(item), STYLES["bullet"], bulletText="•") for item in items]


def table(rows: Sequence[Sequence[str]], widths: Sequence[float], header: bool = True) -> Table:
    """Tableau à la charte : en-tête vert, lignes alternées, texte renvoyé à la ligne.

    `widths` donne la part de la largeur utile occupée par chaque colonne (somme = 1).
    """
    data = [
        [
            Paragraph(markup(cell), STYLES["cell_head" if header and i == 0 else "cell"])
            for cell in row
        ]
        for i, row in enumerate(rows)
    ]
    result = Table(data, colWidths=[w * FRAME_WIDTH for w in widths], repeatRows=int(header))
    commands: list[tuple] = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D6D0")),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), GREEN))
    first_body_row = 1 if header else 0
    for row_index in range(first_body_row, len(rows)):
        if (row_index - first_body_row) % 2 == 1:
            commands.append(("BACKGROUND", (0, row_index), (-1, row_index), GREEN_LIGHT))
    result.setStyle(TableStyle(commands))
    result.spaceBefore = 3
    result.spaceAfter = 8
    return result


def calculation(lines: Sequence[tuple[str, str]], title: str) -> list[Flowable]:
    """Calcul présenté ligne par ligne : numéro, étape expliquée, résultat."""
    rows = [["N°", title, "Résultat"]]
    rows += [[str(i), step, result] for i, (step, result) in enumerate(lines, start=1)]
    return [table(rows, (0.07, 0.68, 0.25))]


def callout(title: str, lines: Sequence[str]) -> KeepTogether:
    """Encadré doré (règle importante, point de vigilance)."""
    content: list[Flowable] = [Paragraph(markup(title), STYLES["callout_title"])]
    content += [Paragraph(markup(line), STYLES["cell"]) for line in lines]
    box = Table([[content]], colWidths=[FRAME_WIDTH])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), GOLD_LIGHT),
                ("LINEBEFORE", (0, 0), (0, -1), 3, GOLD),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    box.spaceBefore = 4
    box.spaceAfter = 8
    return KeepTogether([box])


def faq(items: Sequence[tuple[str, str]]) -> list[Flowable]:
    """Questions fréquentes : question en gras, réponse en texte courant."""
    blocks: list[Flowable] = []
    for question, answer in items:
        blocks.append(Paragraph(markup(question), STYLES["faq_q"]))
        blocks.append(p(answer))
    return blocks


def title_block(spec: DocumentSpec) -> list[Flowable]:
    """Titre du document et cartouche (version, dates, approbation), en page 1."""
    subtitle = f"{INSTITUTION_NAME} — {INSTITUTION_CATEGORY}, siège à {HEAD_OFFICE_CITY}"
    cartouche = table(
        [
            ["Référence", spec.reference, "Version", spec.version],
            ["Rédigé par", spec.drafted_by, "Date d'application", spec.effective_date],
            ["Approuvé par", spec.approved_by, "Date d'approbation", spec.approval_date],
        ],
        (0.16, 0.36, 0.2, 0.28),
        header=False,
    )
    cartouche.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.8, GREEN),
                ("BACKGROUND", (0, 0), (0, -1), GREEN_LIGHT),
                ("BACKGROUND", (2, 0), (2, -1), GREEN_LIGHT),
            ]
        )
    )
    return [
        Paragraph(markup(spec.title), STYLES["title"]),
        Paragraph(markup(subtitle), STYLES["subtitle"]),
        cartouche,
        Spacer(1, 2),
    ]


# --- Rendu ---------------------------------------------------------------------


def render_document(spec: DocumentSpec, pages: Sequence[Page], path: Path) -> Path:
    """Écrit le PDF : une page de contenu par page déclarée, puis les métadonnées."""
    path.parent.mkdir(parents=True, exist_ok=True)
    draft = path.with_name(f"{path.stem}.brouillon.pdf")
    template = BaseDocTemplate(
        str(draft),
        pagesize=A4,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=FRAME_TOP_FROM_TOP,
        bottomMargin=FRAME_BOTTOM,
        invariant=1,
    )
    frame = Frame(
        MARGIN_X,
        FRAME_BOTTOM,
        FRAME_WIDTH,
        FRAME_HEIGHT,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        id="contenu",
    )
    template.addPageTemplates(
        [PageTemplate(id="page", frames=[frame], onPage=partial(_draw_edges, spec=spec))]
    )
    story: list[Flowable] = []
    for index, page in enumerate(pages):
        if index:
            story.append(PageBreak())
        story.extend(page)
    template.build(story)
    _write_metadata(draft, path, spec)
    return path


def _draw_edges(canvas: Canvas, document: BaseDocTemplate, spec: DocumentSpec) -> None:
    """Dessine l'en-tête (institution, référence) et le pied de page (mention, numéro)."""
    canvas.saveState()
    top = PAGE_HEIGHT - 40
    canvas.setFillColor(GREEN)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(MARGIN_X, top, INSTITUTION_NAME)
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(PAGE_WIDTH - MARGIN_X, top, f"Réf. {spec.reference}")
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.6)
    canvas.line(MARGIN_X, top - 8, PAGE_WIDTH - MARGIN_X, top - 8)

    canvas.setStrokeColor(GREEN)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN_X, 52, PAGE_WIDTH - MARGIN_X, 52)
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica-Oblique", 8)
    canvas.drawString(MARGIN_X, 38, FOOTER_TEXT)
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(PAGE_WIDTH - MARGIN_X, 38, f"Page {document.page} / {spec.pages}")
    canvas.restoreState()


def _write_metadata(draft: Path, path: Path, spec: DocumentSpec) -> None:
    """Écrit les métadonnées en UTF-8 avec PyMuPDF (reportlab abîme les accents du titre)."""
    with pymupdf.open(draft) as document:
        document.set_metadata(
            {
                "title": spec.title,
                "author": f"{INSTITUTION_NAME} (institution fictive)",
                "subject": f"{spec.reference} — version {spec.version}",
                "keywords": spec.reference,
                "creator": "ZakiCortex — corpus de démonstration",
                "producer": "reportlab + PyMuPDF",
                "creationDate": "D:20260101000000",
                "modDate": "D:20260101000000",
            }
        )
        document.save(path, garbage=3, deflate=True)
    draft.unlink()
