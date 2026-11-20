"""Tests du client Ollama (rag/llm.py) avec une doublure : Ollama n'est jamais appelé."""

from types import SimpleNamespace

import httpx
import ollama
import pytest

from rag.errors import (
    AssistantError,
    ModelNotFoundError,
    OllamaTimeoutError,
    OllamaUnavailableError,
)
from rag.llm import OllamaClient


class FakeOllama:
    """Doublure du client ollama : enregistre les appels, renvoie des réponses fixes."""

    def __init__(self, chat_errors: list[Exception] | None = None, embed_error=None):
        self.chat_calls: list[dict] = []
        self.embed_calls: list[dict] = []
        self._chat_errors = list(chat_errors or [])
        self._embed_error = embed_error

    def chat(self, **kwargs):
        self.chat_calls.append(kwargs)
        if self._chat_errors:
            raise self._chat_errors.pop(0)
        return SimpleNamespace(message=SimpleNamespace(content="  Réponse (Source : A, page 1)  "))

    def embed(self, **kwargs):
        self.embed_calls.append(kwargs)
        if self._embed_error:
            raise self._embed_error
        return SimpleNamespace(embeddings=[[0.1, 0.2] for _ in kwargs["input"]])


@pytest.fixture
def settings(make_settings):
    return make_settings()


def test_generation_avec_les_bons_parametres(settings):
    fake = FakeOllama()
    texte = OllamaClient(settings, fake).generate("système", "question")
    assert texte == "Réponse (Source : A, page 1)"
    call = fake.chat_calls[0]
    assert call["model"] == "qwen3:4b-instruct-2507-q4_K_M"
    assert call["think"] is False
    assert call["keep_alive"] == "30m"
    assert call["options"] == {"temperature": 0.1, "num_ctx": 4096, "num_predict": 300}
    assert [m["role"] for m in call["messages"]] == ["system", "user"]


def test_think_refuse_nouvel_essai_sans_le_parametre(settings, caplog):
    refus = ollama.ResponseError('"model" does not support thinking', 400)
    fake = FakeOllama(chat_errors=[refus])
    client = OllamaClient(settings, fake)
    with caplog.at_level("WARNING", logger="assistant"):
        assert client.generate("s", "q").startswith("Réponse")
    assert [c["think"] for c in fake.chat_calls] == [False, None]
    assert "think" in caplog.text
    client.generate("s", "q")
    assert fake.chat_calls[-1]["think"] is None


def test_embeddings(settings):
    fake = FakeOllama()
    vecteurs = OllamaClient(settings, fake).embed(["a", "b", "c"])
    assert len(vecteurs) == 3
    assert fake.embed_calls[0]["model"] == "bge-m3"
    assert fake.embed_calls[0]["keep_alive"] == "30m"


def test_embeddings_liste_vide_sans_appel(settings):
    fake = FakeOllama()
    assert OllamaClient(settings, fake).embed([]) == []
    assert fake.embed_calls == []


def test_ollama_arrete(settings):
    fake = FakeOllama(embed_error=ConnectionError("Failed to connect to Ollama"))
    with pytest.raises(OllamaUnavailableError) as info:
        OllamaClient(settings, fake).embed(["a"])
    assert "Lancez Ollama" in info.value.user_message


def test_delai_depasse(settings):
    fake = FakeOllama(chat_errors=[httpx.ReadTimeout("trop long")])
    with pytest.raises(OllamaTimeoutError):
        OllamaClient(settings, fake).generate("s", "q")


def test_modele_absent(settings):
    erreur = ollama.ResponseError('model "qwen3:4b-instruct-2507-q4_K_M" not found', 404)
    with pytest.raises(ModelNotFoundError) as info:
        OllamaClient(settings, FakeOllama(chat_errors=[erreur])).generate("s", "q")
    assert "ollama pull qwen3:4b-instruct-2507-q4_K_M" in info.value.user_message


def test_modele_d_embedding_absent(settings):
    erreur = ollama.ResponseError('model "bge-m3" not found', 404)
    with pytest.raises(ModelNotFoundError) as info:
        OllamaClient(settings, FakeOllama(embed_error=erreur)).embed(["a"])
    assert info.value.model == "bge-m3"


def test_autre_erreur_message_generique(settings):
    erreur = ollama.ResponseError("erreur interne", 500)
    with pytest.raises(AssistantError, match="code 500"):
        OllamaClient(settings, FakeOllama(chat_errors=[erreur])).generate("s", "q")


def test_client_reel_configure_en_local_strict(settings):
    client = OllamaClient(settings)._client._client
    assert str(client.base_url).startswith("http://127.0.0.1:11434")
    assert client.follow_redirects is False
    assert client.trust_env is False
