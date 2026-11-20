"""Fixtures partagées par les tests."""

import os

import pytest

from config import Settings


@pytest.fixture(autouse=True)
def clean_assistant_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Retire les variables ASSISTANT_* de l'environnement pour isoler chaque test."""
    for name in list(os.environ):
        if name.startswith("ASSISTANT_"):
            monkeypatch.delenv(name)


@pytest.fixture
def make_settings():
    """Fabrique des réglages qui ignorent le vrai fichier .env de la machine."""

    def _make(**overrides: object) -> Settings:
        return Settings(_env_file=None, **overrides)

    return _make
