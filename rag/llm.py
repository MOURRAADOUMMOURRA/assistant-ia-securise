"""Client Ollama local : calcul des embeddings et génération des réponses.

Les erreurs techniques d'Ollama sont traduites en erreurs métier (`rag.errors`)
porteuses d'un message clair. Le client HTTP ne suit aucune redirection et
ignore les proxys du système : les requêtes ne peuvent aller que vers l'Ollama
local configuré.
"""

from collections.abc import Callable, Sequence
from typing import Protocol, TypeVar

import httpx
import ollama

from config import Settings
from rag.errors import (
    AssistantError,
    ModelNotFoundError,
    OllamaTimeoutError,
    OllamaUnavailableError,
)
from rag.logging_setup import get_logger

HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400

T = TypeVar("T")
logger = get_logger(__name__)


class Embedder(Protocol):
    """Tout objet capable de transformer des textes en vecteurs."""

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Renvoie un vecteur par texte, dans le même ordre."""
        ...


class Generator(Protocol):
    """Tout objet capable de générer une réponse à partir de deux consignes."""

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Renvoie le texte généré."""
        ...


class OllamaClient:
    """Accès à Ollama pour les embeddings (bge-m3) et la génération (qwen3)."""

    def __init__(self, settings: Settings, client: ollama.Client | None = None) -> None:
        """Prépare le client ; aucune requête n'est envoyée à la construction."""
        self._settings = settings
        self._client = client or ollama.Client(
            host=settings.ollama_host,
            timeout=settings.ollama_timeout_s,
            follow_redirects=False,
            trust_env=False,
        )
        self._think_supported = True

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Calcule les embeddings d'une liste de textes avec le modèle d'embedding."""
        if not texts:
            return []
        model = self._settings.embed_model
        response = self._call(
            model,
            lambda: self._client.embed(
                model=model, input=list(texts), keep_alive=self._settings.ollama_keep_alive
            ),
        )
        return [list(vector) for vector in response.embeddings]

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Génère une réponse courte, à température basse et sans mode « réflexion »."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        if self._think_supported:
            try:
                return self._chat(messages, think=False)
            except ollama.ResponseError:
                self._think_supported = False
                logger.warning("Le modèle refuse le paramètre think : nouvel essai sans lui.")
        return self._chat(messages, think=None)

    def _chat(self, messages: list[dict[str, str]], think: bool | None) -> str:
        """Appelle le modèle de génération et renvoie le texte de sa réponse."""
        model = self._settings.llm_model
        options = {
            "temperature": self._settings.llm_temperature,
            "num_ctx": self._settings.llm_num_ctx,
            "num_predict": self._settings.llm_num_predict,
        }
        response = self._call(
            model,
            lambda: self._client.chat(
                model=model,
                messages=messages,
                options=options,
                think=think,
                keep_alive=self._settings.ollama_keep_alive,
            ),
            passthrough_think_errors=think is not None,
        )
        return (response.message.content or "").strip()

    def _call(
        self, model: str, request: Callable[[], T], passthrough_think_errors: bool = False
    ) -> T:
        """Exécute une requête Ollama et traduit les erreurs techniques en erreurs métier."""
        try:
            return request()
        except ConnectionError as error:
            raise OllamaUnavailableError from error
        except httpx.TimeoutException as error:
            raise OllamaTimeoutError from error
        except httpx.TransportError as error:
            raise OllamaUnavailableError from error
        except ollama.ResponseError as error:
            if passthrough_think_errors and _is_think_rejection(error):
                raise
            raise _translate_response_error(error, model) from error


def _is_think_rejection(error: ollama.ResponseError) -> bool:
    """Indique si Ollama refuse la requête à cause du paramètre think."""
    return error.status_code == HTTP_BAD_REQUEST and "think" in str(error.error).lower()


def _translate_response_error(error: ollama.ResponseError, model: str) -> AssistantError:
    """Convertit une erreur HTTP d'Ollama en erreur métier lisible."""
    if error.status_code == HTTP_NOT_FOUND:
        return ModelNotFoundError(model)
    logger.error("Erreur Ollama %s : %s", error.status_code, error.error)
    return AssistantError(
        f"Le moteur d'IA local a renvoyé une erreur (code {error.status_code}). "
        "Consultez le journal pour le détail."
    )
