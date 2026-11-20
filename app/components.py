"""Composants d'affichage : barre latérale, questions d'exemple, réponses et cartes Sources."""

from collections.abc import Callable, Sequence
from html import escape

import streamlit as st

from app.styles import badge_html, logo_html
from rag.llm import OllamaStatus
from rag.models import Answer, DocumentSummary, Source

EXAMPLE_QUESTIONS: tuple[tuple[str, str], ...] = (
    ("Question directe", "Quel est le montant maximal d'un premier crédit ?"),
    ("Question reformulée", "Je me marie le mois prochain, j'ai droit à combien de jours ?"),
    ("Piège 2025 / 2026", "Quel est le taux du crédit pour activité génératrice de revenus ?"),
    ("Sans réponse", "L'institution autorise-t-elle le télétravail ?"),
)
EXCERPT_PREVIEW_CHARS = 380
OPEN_PAGES_KEY = "open_pages"

PageRenderer = Callable[[Source], tuple[bytes | None, str]]
"""Fonction qui renvoie (image PNG ou None, message) pour une source."""


def render_sidebar(
    overview: Sequence[DocumentSummary],
    status: OllamaStatus,
    double_forced: bool,
    on_logout: Callable[[], None],
) -> None:
    """Barre latérale : logo, badge, état d'Ollama, mode doublure, documents."""
    with st.sidebar:
        st.markdown(logo_html() + badge_html(), unsafe_allow_html=True)
        css_class = "zc-status-on" if status.ready else "zc-status-off"
        st.markdown(
            f'<div class="zc-status {css_class}">● Ollama : {escape(status.message)}</div>',
            unsafe_allow_html=True,
        )
        if double_forced:
            st.caption("Mode doublure imposé par le fichier .env (ASSISTANT_TEST_DOUBLE).")
        elif not status.ready:
            st.toggle(
                "Mode doublure (test sans IA)",
                key="doublure",
                help="Utilise de faux modèles locaux pour parcourir l'application sans "
                "Ollama. Les réponses ne sont alors pas générées par une IA.",
            )
        _render_documents(overview)
        st.button("Se déconnecter", on_click=on_logout, width="stretch")


def _render_documents(overview: Sequence[DocumentSummary]) -> None:
    """Liste des documents avec leur nombre de pages et de morceaux indexés."""
    indexed = sum(1 for doc in overview if doc.chunk_count)
    with st.expander(f"📚 Documents ({len(overview)}, dont {indexed} indexés)"):
        if not overview:
            st.caption("Aucun PDF dans le dossier des documents.")
        lines = [
            f'<div class="zc-doc"><b>{escape(doc.title)}</b><br>{doc.page_count} pages · '
            + (f"{doc.chunk_count} morceaux" if doc.chunk_count else "non indexé")
            + "</div>"
            for doc in overview
        ]
        st.markdown("".join(lines), unsafe_allow_html=True)


def render_examples() -> str | None:
    """Affiche les 4 questions d'exemple ; renvoie celle qui a été cliquée."""
    st.caption("Questions d'exemple")
    clicked = None
    for index, (column, (label, question)) in enumerate(
        zip(st.columns(len(EXAMPLE_QUESTIONS)), EXAMPLE_QUESTIONS, strict=True)
    ):
        if column.button(label, key=f"exemple_{index}", help=question, width="stretch"):
            clicked = question
    return clicked


def format_duration(seconds: float) -> str:
    """Durée à la française : 2.43 → « 2,4 s »."""
    return f"{seconds:.1f}".replace(".", ",") + " s"


def render_answer(answer: Answer, key: str, renderer: PageRenderer) -> None:
    """Affiche une réponse, son temps de calcul et ses sources."""
    if answer.refused:
        st.warning(answer.text)
    else:
        st.markdown(answer.text)
    st.markdown(
        f'<div class="zc-time">⏱ Réponse en {format_duration(answer.duration_s)}</div>',
        unsafe_allow_html=True,
    )
    cited = list(answer.cited_sources)
    consulted = [source for source in answer.sources if not source.cited]
    if cited:
        st.markdown("**Sources citées**")
        for index, source in enumerate(cited):
            render_source_card(source, f"{key}-c{index}", renderer)
    if consulted:
        with st.expander(f"Sources consultées ({len(consulted)})", expanded=False):
            for index, source in enumerate(consulted):
                render_source_card(source, f"{key}-s{index}", renderer)


def render_source_card(source: Source, key: str, renderer: PageRenderer) -> None:
    """Carte d'une source : titre, page, extrait, et bouton « Voir la page »."""
    excerpt = source.excerpt
    if len(excerpt) > EXCERPT_PREVIEW_CHARS:
        excerpt = excerpt[:EXCERPT_PREVIEW_CHARS].rsplit(" ", 1)[0] + "…"
    st.markdown(
        '<div class="zc-card">'
        f'<div class="zc-card-title">{escape(source.title)}</div>'
        f'<div class="zc-card-page">Page {source.page_number} sur {source.page_count}</div>'
        f'<div class="zc-card-excerpt">« {escape(excerpt)} »</div>'
        "</div>",
        unsafe_allow_html=True,
    )
    open_pages: set[str] = st.session_state.setdefault(OPEN_PAGES_KEY, set())
    is_open = key in open_pages
    if st.button("Masquer la page" if is_open else "Voir la page", key=f"page-{key}"):
        open_pages.symmetric_difference_update({key})
        st.rerun()
    if is_open:
        png, caption = renderer(source)
        if png is None:
            st.error(caption)
        else:
            st.image(png, caption=caption, width="stretch")
