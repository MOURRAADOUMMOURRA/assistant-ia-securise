"""Tests des réglages (config.py)."""

import pytest
from pydantic import ValidationError

from config import PROJECT_ROOT, Settings, get_settings


def test_valeurs_par_defaut(make_settings):
    settings = make_settings()
    assert settings.llm_model == "qwen3:4b-instruct-2507-q4_K_M"
    assert settings.embed_model == "bge-m3"
    assert settings.top_k == 5
    assert settings.llm_temperature == pytest.approx(0.1)
    assert settings.chunk_overlap < settings.chunk_size
    assert settings.demo_password is None


def test_lecture_depuis_variables_environnement(monkeypatch, make_settings):
    monkeypatch.setenv("ASSISTANT_TOP_K", "8")
    monkeypatch.setenv("ASSISTANT_SIMILARITY_THRESHOLD", "0.62")
    settings = make_settings()
    assert settings.top_k == 8
    assert settings.similarity_threshold == pytest.approx(0.62)


def test_lecture_depuis_fichier_env(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("ASSISTANT_CHUNK_SIZE=1000\nASSISTANT_LOG_LEVEL=DEBUG\n", encoding="utf-8")
    settings = Settings(_env_file=env_file)
    assert settings.chunk_size == 1000
    assert settings.log_level == "DEBUG"


def test_chemins_relatifs_resolus_depuis_la_racine(make_settings):
    settings = make_settings(index_dir="data/index")
    assert settings.index_dir.is_absolute()
    assert settings.index_dir == (PROJECT_ROOT / "data" / "index").resolve()


def test_chemin_absolu_conserve(tmp_path, make_settings):
    settings = make_settings(docs_dir=tmp_path)
    assert settings.docs_dir == tmp_path


def test_chevauchement_superieur_a_la_taille_refuse(make_settings):
    with pytest.raises(ValidationError, match="CHUNK_OVERLAP"):
        make_settings(chunk_size=500, chunk_overlap=500)


@pytest.mark.parametrize("valeur", [-0.1, 1.5])
def test_seuil_hors_bornes_refuse(make_settings, valeur):
    with pytest.raises(ValidationError):
        make_settings(similarity_threshold=valeur)


def test_top_k_nul_refuse(make_settings):
    with pytest.raises(ValidationError):
        make_settings(top_k=0)


@pytest.mark.parametrize(
    "hote", ["http://127.0.0.1:11434", "http://localhost:11434/", "http://[::1]:11434"]
)
def test_ollama_local_accepte(make_settings, hote):
    settings = make_settings(ollama_host=hote)
    assert not settings.ollama_host.endswith("/")


@pytest.mark.parametrize("hote", ["http://192.168.1.20:11434", "https://api.exemple.com"])
def test_ollama_distant_refuse(make_settings, hote):
    with pytest.raises(ValidationError, match="machine locale"):
        make_settings(ollama_host=hote)


def test_mot_de_passe_jamais_affiche(make_settings):
    settings = make_settings(demo_password="secret-de-test-123")
    assert "secret-de-test-123" not in repr(settings)
    assert "secret-de-test-123" not in str(settings.model_dump())
    assert settings.demo_password.get_secret_value() == "secret-de-test-123"


def test_get_settings_renvoie_toujours_le_meme_objet():
    get_settings.cache_clear()
    try:
        assert get_settings() is get_settings()
    finally:
        get_settings.cache_clear()
