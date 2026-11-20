"""Tests du contrôle de l'environnement (scripts/check_env.py), sans Ollama."""

import urllib.error

import pytest

from scripts import check_env
from scripts.check_env import (
    GB,
    Status,
    check_disk,
    check_env_file,
    check_models,
    check_modules,
    check_ollama_and_models,
    check_python_version,
    check_ram,
    format_result,
    model_is_installed,
)


def test_python_supporte():
    assert check_python_version((3, 12)).status is Status.OK
    assert check_python_version((3, 11)).status is Status.OK


def test_python_trop_recent_ou_ancien():
    assert check_python_version((3, 13)).status is Status.FAILED
    assert check_python_version((3, 10)).status is Status.FAILED


def test_modules_manquants_listes():
    result = check_modules(lambda module: module != "fitz")
    assert result.status is Status.FAILED
    assert "pymupdf" in result.message


def test_modules_tous_presents():
    assert check_modules(lambda _module: True).status is Status.OK


def test_ram_suffisante_et_insuffisante():
    assert check_ram(16 * GB).status is Status.OK
    assert check_ram(4 * GB).status is Status.WARNING


def test_disque():
    assert check_disk(100 * GB).status is Status.OK
    assert check_disk(2 * GB).status is Status.WARNING


def test_correspondance_des_noms_de_modeles():
    installes = {"bge-m3:latest", "qwen3:4b-instruct-2507-q4_K_M"}
    assert model_is_installed("bge-m3", installes)
    assert model_is_installed("qwen3:4b-instruct-2507-q4_K_M", installes)
    assert not model_is_installed("qwen3:4b", installes)


def test_modele_manquant_signale():
    result = check_models(["bge-m3", "qwen3:4b-instruct-2507-q4_K_M"], ["bge-m3:latest"])
    assert result.status is Status.FAILED
    assert "qwen3:4b-instruct-2507-q4_K_M" in result.message


def test_ollama_arrete(make_settings):
    def refuse(_host: str) -> list[str]:
        raise urllib.error.URLError("connexion refusée")

    results = check_ollama_and_models(make_settings(), refuse)
    assert [r.status for r in results] == [Status.FAILED]


def test_ollama_actif_avec_modeles(make_settings):
    results = check_ollama_and_models(
        make_settings(), lambda _host: ["bge-m3:latest", "qwen3:4b-instruct-2507-q4_K_M"]
    )
    assert [r.status for r in results] == [Status.OK, Status.OK]


def test_fichier_env_absent(tmp_path, monkeypatch, make_settings):
    monkeypatch.setattr(check_env, "ENV_PATH", tmp_path / ".env")
    assert check_env_file(make_settings(), "exemple").status is Status.WARNING


@pytest.fixture
def env_present(tmp_path, monkeypatch):
    """Simule la présence d'un fichier .env."""
    env_path = tmp_path / ".env"
    env_path.write_text("", encoding="utf-8")
    monkeypatch.setattr(check_env, "ENV_PATH", env_path)


@pytest.mark.usefixtures("env_present")
def test_mot_de_passe_exemple_en_echec(make_settings):
    exemple = check_env.read_example_password()
    result = check_env_file(make_settings(demo_password=exemple), exemple)
    assert result.status is Status.FAILED
    assert exemple not in result.message


@pytest.mark.usefixtures("env_present")
@pytest.mark.parametrize("mot_de_passe", ["Zq7", "Kouri-2026", "Onze-carac!"])
def test_mot_de_passe_trop_court_en_echec(make_settings, mot_de_passe):
    result = check_env_file(make_settings(demo_password=mot_de_passe), "exemple")
    assert result.status is Status.FAILED
    assert "trop court" in result.message
    assert mot_de_passe not in result.message


@pytest.mark.usefixtures("env_present")
def test_mot_de_passe_de_12_caracteres_accepte(make_settings):
    result = check_env_file(make_settings(demo_password="Douze-carac!"), "exemple")
    assert result.status is Status.OK


def test_valeur_exemple_lue_dans_env_example():
    assert check_env.read_example_password() == "changez-moi-avant-la-demo"


def test_mise_en_forme_avec_conseil():
    result = check_env.CheckResult("Ollama", Status.FAILED, "injoignable", "Lancez Ollama.")
    texte = format_result(result)
    assert "[ÉCHEC" in texte
    assert "-> Lancez Ollama." in texte
