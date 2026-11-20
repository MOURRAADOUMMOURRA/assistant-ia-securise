"""Tests de l'interface Streamlit avec AppTest (sans navigateur, sans Ollama)."""

from html import escape

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

from app.auth import NOT_CONFIGURED, WRONG_PASSWORD, verify_password
from config import PROJECT_ROOT, get_settings, read_example_password
from rag.doubles import DOUBLE_ANSWER_PREFIX
from tests.pdf_factory import write_pdf

APP = str(PROJECT_ROOT / "app" / "main.py")
PASSWORD = "Mot-de-passe-de-test-2026"
TIMEOUT = 120


@pytest.fixture
def app_env(tmp_path, monkeypatch):
    """Environnement isolé : petits PDF, index temporaire, Ollama injoignable."""
    docs = tmp_path / "docs"
    docs.mkdir()
    write_pdf(
        docs / "d10_octroi_credit.pdf",
        [
            ["Objet de la politique de crédit."],
            ["Pour un premier crédit, le montant maximal accordé est de 500 000 FCFA."],
        ],
        title="Politique et procédure d'octroi de crédit",
    )
    monkeypatch.setenv("ASSISTANT_DEMO_PASSWORD", PASSWORD)
    monkeypatch.setenv("ASSISTANT_DOCS_DIR", str(docs))
    monkeypatch.setenv("ASSISTANT_INDEX_DIR", str(tmp_path / "index"))
    monkeypatch.setenv("ASSISTANT_LOGS_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("ASSISTANT_OLLAMA_HOST", "http://127.0.0.1:9")
    monkeypatch.setenv("ASSISTANT_ALLOW_MOCK", "false")
    monkeypatch.setenv("ASSISTANT_TEST_DOUBLE", "false")
    _reset_caches()
    yield
    _reset_caches()


def _reset_caches():
    get_settings.cache_clear()
    st.cache_data.clear()
    st.cache_resource.clear()


def _login(at: AppTest, password: str = PASSWORD) -> AppTest:
    at.text_input(key="password_input").input(password)
    next(b for b in at.button if b.label == "Se connecter").click()
    return at.run()


def _all_text(at: AppTest) -> str:
    parts = [m.value for m in at.markdown] + [m.value for m in at.sidebar.markdown]
    parts += [e.value for e in at.error] + [w.value for w in at.warning]
    parts += [i.value for i in at.info] + [c.value for c in at.caption]
    return "\n".join(str(p) for p in parts)


def test_verification_du_mot_de_passe(make_settings):
    settings = make_settings(demo_password="Correct-Horse-42")
    assert verify_password("Correct-Horse-42", settings)
    assert not verify_password("correct-horse-42", settings)
    assert not verify_password("", settings)
    assert not verify_password("x", make_settings())
    assert not verify_password("", make_settings(demo_password=""))


def test_mot_de_passe_court_ou_d_exemple_toujours_refuse(make_settings):
    exemple = read_example_password()
    assert not verify_password(exemple, make_settings(demo_password=exemple))
    assert not verify_password("Court-11car", make_settings(demo_password="Court-11car"))


@pytest.mark.usefixtures("app_env")
@pytest.mark.parametrize("mot_de_passe", ["exemple", "Court-11car"])
def test_connexion_bloquee_si_mot_de_passe_exemple_ou_court(monkeypatch, mot_de_passe):
    valeur = read_example_password() if mot_de_passe == "exemple" else mot_de_passe
    monkeypatch.setenv("ASSISTANT_DEMO_PASSWORD", valeur)
    get_settings.cache_clear()
    at = AppTest.from_file(APP, default_timeout=TIMEOUT).run()
    assert not at.exception
    assert [e.value for e in at.error] == ["Mot de passe de démo non configuré – voir le README"]
    assert not at.text_input
    assert not any(b.label == "Se connecter" for b in at.button)


@pytest.mark.usefixtures("app_env")
def test_mode_doublure_masque_par_defaut():
    at = _login(AppTest.from_file(APP, default_timeout=TIMEOUT).run())
    assert not at.exception
    assert not at.toggle
    assert "doublure" not in _all_text(at).lower()


@pytest.mark.usefixtures("app_env")
def test_mode_doublure_impose_sans_autorisation_ignore(monkeypatch):
    monkeypatch.setenv("ASSISTANT_TEST_DOUBLE", "true")
    get_settings.cache_clear()
    at = _login(AppTest.from_file(APP, default_timeout=TIMEOUT).run())
    assert not at.toggle
    assert "doublure" not in _all_text(at).lower()


@pytest.mark.usefixtures("app_env")
def test_ecran_de_connexion_puis_mot_de_passe_faux():
    at = AppTest.from_file(APP, default_timeout=TIMEOUT).run()
    assert not at.exception
    assert "100 % local" in _all_text(at)
    _login(at, "mauvais-mot-de-passe")
    assert WRONG_PASSWORD in [e.value for e in at.error]
    assert not at.chat_input


@pytest.mark.usefixtures("app_env")
def test_mot_de_passe_non_configure(monkeypatch):
    monkeypatch.setenv("ASSISTANT_DEMO_PASSWORD", "")
    get_settings.cache_clear()
    at = AppTest.from_file(APP, default_timeout=TIMEOUT).run()
    assert NOT_CONFIGURED in [e.value for e in at.error]


@pytest.mark.usefixtures("app_env")
def test_sans_ollama_message_clair_et_erreur_lisible():
    at = _login(AppTest.from_file(APP, default_timeout=TIMEOUT).run())
    assert not at.exception
    assert "Non connecté" in _all_text(at)
    at.chat_input[0].set_value("Quel est le plafond d'un premier crédit ?").run()
    assert not at.exception
    assert any("Ollama" in e.value for e in at.error)


@pytest.mark.usefixtures("app_env")
def test_parcours_complet_en_mode_doublure(monkeypatch):
    monkeypatch.setenv("ASSISTANT_ALLOW_MOCK", "true")
    get_settings.cache_clear()
    at = _login(AppTest.from_file(APP, default_timeout=TIMEOUT).run())
    assert "mode doublure" in _all_text(at).lower()
    at.toggle(key="doublure").set_value(True).run()
    assert not at.exception
    at.button(key="exemple_0").click().run()
    assert not at.exception
    texte = _all_text(at)
    assert DOUBLE_ANSWER_PREFIX in texte
    assert "Réponse en" in texte
    assert "Politique et procédure d'octroi de crédit" in texte
    assert "Page 2 sur 2" in texte
    voir = [b for b in at.button if b.label == "Voir la page"]
    assert voir
    voir[0].click().run()
    assert not at.exception
    assert at.session_state["open_pages"]
    assert any(b.label == "Masquer la page" for b in at.button)


@pytest.mark.usefixtures("app_env")
def test_liste_des_documents_dans_la_barre_laterale():
    at = _login(AppTest.from_file(APP, default_timeout=TIMEOUT).run())
    sidebar = "\n".join(m.value for m in at.sidebar.markdown)
    assert escape("Politique et procédure d'octroi de crédit") in sidebar
    assert "2 pages · non indexé" in sidebar
    assert "Zaki<span>Cortex</span>" in sidebar
