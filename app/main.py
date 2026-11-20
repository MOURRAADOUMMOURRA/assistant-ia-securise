"""Point d'entrée de l'interface : streamlit run app/main.py

Ce script ne fait qu'afficher : toute la logique (recherche, génération, rendu des
pages, état d'Ollama) est dans le paquet rag/.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st  # noqa: E402
from pydantic import ValidationError  # noqa: E402

from app import auth, components, styles  # noqa: E402
from config import Settings, get_settings  # noqa: E402
from rag.catalog import corpus_overview  # noqa: E402
from rag.errors import AssistantError  # noqa: E402
from rag.llm import OllamaStatus, check_ollama  # noqa: E402
from rag.logging_setup import get_logger, setup_logging_from_settings  # noqa: E402
from rag.models import Answer, DocumentSummary, Source  # noqa: E402
from rag.page_render import render_highlighted_page  # noqa: E402
from rag.pipeline import AssistantRuntime, create_runtime  # noqa: E402

HISTORY_KEY = "messages"
PENDING_KEY = "pending_question"
SEARCH_LABEL = "Recherche dans les documents…"
UNEXPECTED_ERROR = (
    "Une erreur inattendue est survenue. Réessayez ; si le problème persiste, "
    "consultez le journal (dossier logs)."
)

logger = get_logger("app.main")


@st.cache_resource(show_spinner=False)
def init_logging(_settings: Settings) -> bool:
    """Configure le journal une seule fois par processus."""
    setup_logging_from_settings(_settings)
    return True


@st.cache_resource(show_spinner="Préparation de l'assistant…")
def get_runtime(_settings: Settings, test_double: bool) -> AssistantRuntime:
    """Construit l'assistant (réel ou doublure) une seule fois par mode."""
    return create_runtime(_settings, test_double=test_double)


@st.cache_data(ttl=30, show_spinner=False)
def get_ollama_status(_settings: Settings) -> OllamaStatus:
    """État d'Ollama, revérifié au plus toutes les 30 secondes."""
    return check_ollama(_settings)


@st.cache_data(ttl=60, show_spinner=False)
def get_overview(_runtime: AssistantRuntime, docs_dir: str, test_double: bool) -> list:
    """Liste des documents avec pages et morceaux, rafraîchie chaque minute."""
    return corpus_overview(Path(docs_dir), _runtime.store)


@st.cache_data(max_entries=64, show_spinner=False)
def render_page(path: str, page_number: int, passage: str, docs_dir: str) -> bytes:
    """Image PNG d'une page avec le passage surligné (mise en cache)."""
    return render_highlighted_page(Path(path), page_number, passage, Path(docs_dir)).png


def load_settings() -> Settings:
    """Lit les réglages ; arrête l'application avec un message clair s'ils sont invalides."""
    try:
        return get_settings()
    except ValidationError as error:
        st.error(f"Configuration invalide dans le fichier .env : {error.errors()[0]['msg']}")
        st.stop()
        raise


def make_renderer(settings: Settings) -> components.PageRenderer:
    """Fonction d'affichage d'une page source, avec message clair en cas d'échec."""

    def renderer(source: Source) -> tuple[bytes | None, str]:
        try:
            png = render_page(
                str(source.source_path),
                source.page_number,
                source.excerpt,
                str(settings.docs_dir),
            )
        except AssistantError as error:
            return None, error.user_message
        return png, f"{source.title} — page {source.page_number} (passage utilisé en jaune)"

    return renderer


def ask(runtime: AssistantRuntime, question: str) -> tuple[Answer | None, str | None]:
    """Pose la question au moteur ; renvoie (réponse, None) ou (None, message d'erreur)."""
    try:
        return runtime.pipeline.ask(question), None
    except AssistantError as error:
        logger.warning("Question non traitée : %s", error.user_message)
        return None, error.user_message
    except Exception:
        logger.exception("Erreur inattendue pendant le traitement d'une question.")
        return None, UNEXPECTED_ERROR


def render_history(renderer: components.PageRenderer) -> None:
    """Réaffiche la conversation de la session."""
    for index, message in enumerate(st.session_state.setdefault(HISTORY_KEY, [])):
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(message["text"])
            elif message.get("error"):
                st.error(message["error"])
            else:
                components.render_answer(message["answer"], f"m{index}", renderer)


def answer_question(
    question: str, runtime: AssistantRuntime, renderer: components.PageRenderer
) -> None:
    """Affiche la question, l'indicateur de recherche, puis la réponse."""
    history = st.session_state.setdefault(HISTORY_KEY, [])
    history.append({"role": "user", "text": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.status(SEARCH_LABEL, expanded=False) as status:
            answer, error = ask(runtime, question)
            status.update(
                label="Recherche terminée" if error is None else "Recherche interrompue",
                state="complete" if error is None else "error",
            )
        if error is not None:
            st.error(error)
            history.append({"role": "assistant", "error": error})
        else:
            components.render_answer(answer, f"m{len(history)}", renderer)
            history.append({"role": "assistant", "answer": answer})


def main() -> None:
    """Construit la page."""
    st.set_page_config(
        page_title="Assistant IA interne sécurisé — ZakiCortex", page_icon="🔒", layout="wide"
    )
    styles.apply_styles()
    settings = load_settings()
    init_logging(settings)
    if not auth.is_authenticated():
        auth.render_login(settings)
        return

    status = get_ollama_status(settings)
    test_double = settings.test_double or bool(st.session_state.get("doublure"))
    try:
        runtime = get_runtime(settings, test_double)
    except AssistantError as error:
        st.error(error.user_message)
        return
    overview: list[DocumentSummary] = get_overview(runtime, str(settings.docs_dir), test_double)
    components.render_sidebar(overview, status, settings.test_double, auth.logout)

    st.markdown(
        '<div class="zc-hero"><h1>Assistant IA interne sécurisé</h1>'
        "<p>Posez une question sur les procédures internes : la réponse cite le document "
        "et la page.</p></div>",
        unsafe_allow_html=True,
    )
    if test_double:
        st.markdown(
            '<div class="zc-double">Mode doublure : les réponses recopient le passage le '
            "plus proche, sans IA. Il sert à tester le parcours sans Ollama.</div>",
            unsafe_allow_html=True,
        )
    elif not status.ready:
        st.info(
            f"Ollama : {status.message} Les questions afficheront un message d'erreur "
            "tant qu'Ollama n'est pas prêt. Pour tester le parcours, activez le mode "
            "doublure dans la barre latérale."
        )

    renderer = make_renderer(settings)
    example = components.render_examples()
    render_history(renderer)
    question = st.chat_input("Posez votre question…") or example
    if question:
        answer_question(question.strip(), runtime, renderer)


main()
