"""Réglages typés de l'application, lus depuis le fichier `.env`.

C'est le seul endroit du projet où figurent des valeurs par défaut. Le reste du
code reçoit un objet `Settings` et n'écrit aucune valeur en dur.

Chaque réglage peut être surchargé par une variable d'environnement préfixée
par `ASSISTANT_` (par exemple `ASSISTANT_TOP_K=8`).
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT: Path = Path(__file__).resolve().parent
"""Racine du projet : tous les chemins relatifs sont résolus à partir d'elle."""

LOCAL_HOSTS: frozenset[str] = frozenset({"localhost", "127.0.0.1", "::1"})
"""Noms d'hôtes acceptés pour Ollama : la machine locale uniquement."""

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class Settings(BaseSettings):
    """Ensemble des réglages de l'assistant, validés au chargement."""

    model_config = SettingsConfigDict(
        env_prefix="ASSISTANT_",
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    demo_password: SecretStr | None = Field(
        default=None,
        description="Mot de passe de démonstration (obligatoire pour ouvrir l'interface).",
    )

    ollama_host: str = "http://127.0.0.1:11434"
    llm_model: str = "qwen3:4b-instruct-2507-q4_K_M"
    embed_model: str = "bge-m3"
    ollama_keep_alive: str = "30m"
    ollama_timeout_s: float = Field(default=180.0, gt=0)

    llm_temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    llm_num_ctx: int = Field(default=4096, ge=512)
    llm_num_predict: int = Field(default=300, ge=16)

    chunk_size: int = Field(default=900, ge=100)
    chunk_overlap: int = Field(default=150, ge=0)

    top_k: int = Field(default=5, ge=1, le=50)
    similarity_threshold: float = Field(default=0.5, ge=0.0, le=1.0)

    docs_dir: Path = Path("demo_docs")
    index_dir: Path = Path("data/index")
    logs_dir: Path = Path("logs")

    log_level: LogLevel = "INFO"

    test_double: bool = Field(
        default=False,
        description="Mode doublure : faux modèles locaux, pour tester l'interface sans Ollama.",
    )

    @field_validator("docs_dir", "index_dir", "logs_dir")
    @classmethod
    def _resolve_from_root(cls, value: Path) -> Path:
        """Rend un chemin relatif absolu, à partir de la racine du projet."""
        return value if value.is_absolute() else (PROJECT_ROOT / value).resolve()

    @field_validator("ollama_host")
    @classmethod
    def _require_local_host(cls, value: str) -> str:
        """Refuse toute adresse d'Ollama qui ne pointe pas vers la machine locale."""
        hostname = urlparse(value).hostname
        if hostname not in LOCAL_HOSTS:
            raise ValueError(
                f"ASSISTANT_OLLAMA_HOST doit pointer vers la machine locale "
                f"({', '.join(sorted(LOCAL_HOSTS))}), reçu : {value!r}"
            )
        return value.rstrip("/")

    @model_validator(mode="after")
    def _check_overlap(self) -> "Settings":
        """Vérifie que le chevauchement est plus petit que la taille d'un morceau."""
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                f"ASSISTANT_CHUNK_OVERLAP ({self.chunk_overlap}) doit être inférieur "
                f"à ASSISTANT_CHUNK_SIZE ({self.chunk_size})."
            )
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Charge les réglages une seule fois et renvoie toujours le même objet."""
    return Settings()
