"""Tests du journal (rag/logging_setup.py)."""

import logging

import pytest

from rag.logging_setup import (
    LOG_FILE_NAME,
    LOGGER_NAME,
    REDACTED,
    get_logger,
    setup_logging,
    setup_logging_from_settings,
)


@pytest.fixture(autouse=True)
def fermer_le_journal():
    """Ferme les fichiers du journal après chaque test (indispensable sous Windows)."""
    yield
    logger = logging.getLogger(LOGGER_NAME)
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)


def _flush(logger: logging.Logger) -> None:
    for handler in logger.handlers:
        handler.flush()


def test_ecrit_dans_le_fichier_avec_horodatage(tmp_path):
    logger = setup_logging(tmp_path, "INFO")
    get_logger("test").info("question traitée en 1.2 s")
    _flush(logger)
    contenu = (tmp_path / LOG_FILE_NAME).read_text(encoding="utf-8")
    assert "question traitée en 1.2 s" in contenu
    assert "assistant.test" in contenu
    assert contenu[:4].isdigit()


def test_cree_le_dossier_des_journaux(tmp_path):
    dossier = tmp_path / "sous" / "dossier"
    setup_logging(dossier)
    assert dossier.is_dir()


def test_appels_repetes_sans_doublon(tmp_path):
    setup_logging(tmp_path)
    logger = setup_logging(tmp_path)
    assert len(logger.handlers) == 2


def test_respecte_le_niveau(tmp_path):
    logger = setup_logging(tmp_path, "WARNING")
    get_logger("test").info("message ignoré")
    _flush(logger)
    assert "message ignoré" not in (tmp_path / LOG_FILE_NAME).read_text(encoding="utf-8")


def test_le_secret_est_masque(tmp_path):
    logger = setup_logging(tmp_path, "INFO", secrets=["MotDePasse!42"])
    get_logger("auth").warning("tentative avec %s", "MotDePasse!42")
    _flush(logger)
    contenu = (tmp_path / LOG_FILE_NAME).read_text(encoding="utf-8")
    assert "MotDePasse!42" not in contenu
    assert REDACTED in contenu


def test_mot_de_passe_des_reglages_masque(tmp_path, make_settings):
    settings = make_settings(logs_dir=tmp_path, demo_password="Kouri-2026")
    logger = setup_logging_from_settings(settings)
    get_logger("auth").info("valeur reçue : Kouri-2026")
    _flush(logger)
    assert "Kouri-2026" not in (tmp_path / LOG_FILE_NAME).read_text(encoding="utf-8")
