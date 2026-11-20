"""Écran de connexion par mot de passe de démonstration (lu dans .env, jamais affiché)."""

import hmac
import time

import streamlit as st

from app.styles import badge_html, logo_html
from config import Settings
from rag.logging_setup import get_logger

MAX_ATTEMPTS = 5
LOCK_SECONDS = 30
AUTH_KEY = "authenticated"
FAILS_KEY = "login_failures"
LOCK_KEY = "login_locked_until"

WRONG_PASSWORD = "Mot de passe incorrect. Vérifiez la saisie (majuscules, chiffres, symboles)."
NOT_CONFIGURED = "Mot de passe de démo non configuré – voir le README"

logger = get_logger("app.auth")


def verify_password(candidate: str, settings: Settings) -> bool:
    """Compare le mot de passe saisi à celui du .env, en temps constant.

    Refuse toujours si le mot de passe du .env est absent, trop court ou égal à la
    valeur d'exemple.
    """
    if not settings.demo_password_usable or not candidate:
        return False
    expected = settings.demo_password.get_secret_value().encode("utf-8")
    return hmac.compare_digest(candidate.encode("utf-8"), expected)


def is_authenticated() -> bool:
    """Indique si la session est connectée."""
    return bool(st.session_state.get(AUTH_KEY))


def logout() -> None:
    """Déconnecte la session et efface l'historique de conversation."""
    st.session_state.clear()


def render_login(settings: Settings) -> None:
    """Affiche l'écran de connexion et traite la saisie."""
    st.markdown(logo_html() + badge_html(), unsafe_allow_html=True)
    st.markdown("### Connexion")
    st.caption("Accès réservé au personnel. Saisissez le mot de passe de démonstration.")
    if not settings.demo_password_usable:
        logger.warning("Connexion refusée : mot de passe de démo absent, trop court ou d'exemple.")
        st.error(NOT_CONFIGURED)
        return
    with st.form("login", clear_on_submit=True):
        candidate = st.text_input("Mot de passe", type="password", key="password_input")
        submitted = st.form_submit_button("Se connecter", type="primary")
    if submitted:
        _handle_attempt(candidate, settings)


def _handle_attempt(candidate: str, settings: Settings) -> None:
    """Vérifie une tentative, avec blocage temporaire après plusieurs échecs."""
    remaining = st.session_state.get(LOCK_KEY, 0.0) - time.monotonic()
    if remaining > 0:
        st.warning(f"Trop de tentatives. Réessayez dans {int(remaining) + 1} secondes.")
        return
    if verify_password(candidate, settings):
        st.session_state[AUTH_KEY] = True
        st.session_state[FAILS_KEY] = 0
        logger.info("Connexion réussie.")
        st.rerun()
    failures = st.session_state.get(FAILS_KEY, 0) + 1
    st.session_state[FAILS_KEY] = failures
    logger.warning("Échec de connexion (tentative %d).", failures)
    if failures >= MAX_ATTEMPTS:
        st.session_state[LOCK_KEY] = time.monotonic() + LOCK_SECONDS
        st.session_state[FAILS_KEY] = 0
        st.error(f"{WRONG_PASSWORD} Accès bloqué pendant {LOCK_SECONDS} secondes.")
    else:
        st.error(WRONG_PASSWORD)
