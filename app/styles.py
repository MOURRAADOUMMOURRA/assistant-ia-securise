"""Charte ZakiCortex : violet sur fond sombre.

Aucune police ni feuille de style n'est chargée depuis Internet : la pile de polices
ne contient que des polices déjà présentes sur le poste.
"""

import streamlit as st

VIOLET = "#8B5CF6"
VIOLET_DARK = "#6D28D9"
VIOLET_LIGHT = "#C4B5FD"
BACKGROUND = "#0F0B1A"
SURFACE = "#1A1430"
BORDER = "#2E2550"
TEXT = "#EDE9FE"
MUTED = "#A79FC7"
SUCCESS = "#34D399"
DANGER = "#F87171"

FONT_STACK = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"

CSS = f"""
<style>
html, body, [class*="css"] {{ font-family: {FONT_STACK}; }}
.zc-logo {{ font-size: 1.7rem; font-weight: 800; letter-spacing: 0.02em; color: {TEXT}; }}
.zc-logo span {{ color: {VIOLET}; }}
.zc-tagline {{ color: {MUTED}; font-size: 0.85rem; margin-top: -0.3rem; }}
.zc-badge {{
    display: inline-block; padding: 0.45rem 0.75rem; margin: 0.6rem 0 0.4rem 0;
    border-radius: 999px; border: 1px solid {VIOLET};
    background: rgba(139, 92, 246, 0.12); color: {VIOLET_LIGHT};
    font-size: 0.82rem; font-weight: 600;
}}
.zc-status {{ font-size: 0.85rem; padding: 0.35rem 0; }}
.zc-status-on {{ color: {SUCCESS}; }}
.zc-status-off {{ color: {DANGER}; }}
.zc-card {{
    background: {SURFACE}; border: 1px solid {BORDER}; border-left: 4px solid {VIOLET};
    border-radius: 10px; padding: 0.75rem 0.9rem; margin: 0.35rem 0;
}}
.zc-card-title {{ font-weight: 700; color: {TEXT}; }}
.zc-card-page {{ color: {VIOLET_LIGHT}; font-size: 0.85rem; font-weight: 600; }}
.zc-card-excerpt {{ color: {MUTED}; font-size: 0.88rem; margin-top: 0.35rem; }}
.zc-time {{ color: {MUTED}; font-size: 0.8rem; }}
.zc-doc {{ font-size: 0.8rem; color: {MUTED}; padding: 0.15rem 0; }}
.zc-doc b {{ color: {TEXT}; font-weight: 600; }}
.zc-double {{
    border: 1px dashed {VIOLET}; border-radius: 8px; padding: 0.5rem 0.7rem;
    color: {VIOLET_LIGHT}; font-size: 0.85rem; margin-bottom: 0.6rem;
}}
.zc-hero h1 {{ font-size: 1.6rem; margin-bottom: 0.1rem; }}
.zc-hero p {{ color: {MUTED}; margin-top: 0; }}
</style>
"""


def apply_styles() -> None:
    """Injecte la feuille de style de la charte (locale, sans ressource externe)."""
    st.markdown(CSS, unsafe_allow_html=True)


def logo_html() -> str:
    """Logo texte ZakiCortex."""
    return (
        '<div class="zc-logo">Zaki<span>Cortex</span></div>'
        '<div class="zc-tagline">Assistant IA interne sécurisé</div>'
    )


LOCAL_BADGE = "🔒 100 % local – aucune donnée ne quitte ce PC"


def badge_html() -> str:
    """Badge « 100 % local »."""
    return f'<div class="zc-badge">{LOCAL_BADGE}</div>'
