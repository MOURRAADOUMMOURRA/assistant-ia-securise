"""Configuration du journal (logging) local de l'application.

Le journal est écrit dans un fichier qui tourne (`logs/assistant.log`, 5 copies
de 1 Mo au plus) et affiché dans la console. Un filtre remplace toute valeur
secrète (le mot de passe de démo) par des étoiles, au cas où elle apparaîtrait
par erreur dans un message.
"""

import logging
from collections.abc import Iterable
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import Settings

LOGGER_NAME = "assistant"
LOG_FILE_NAME = "assistant.log"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_LOG_BYTES = 1_000_000
BACKUP_COUNT = 5
REDACTED = "********"
NOISY_LIBRARIES: tuple[str, ...] = ("httpx", "httpcore", "urllib3", "chromadb")


class SecretRedactionFilter(logging.Filter):
    """Masque les valeurs secrètes dans les messages du journal."""

    def __init__(self, secrets: Iterable[str]) -> None:
        """Mémorise les secrets à masquer (les chaînes vides sont ignorées)."""
        super().__init__()
        self._secrets: tuple[str, ...] = tuple(secret for secret in secrets if secret)

    def filter(self, record: logging.LogRecord) -> bool:
        """Remplace chaque secret par des étoiles ; ne bloque jamais le message."""
        if not self._secrets:
            return True
        message = record.getMessage()
        redacted = message
        for secret in self._secrets:
            redacted = redacted.replace(secret, REDACTED)
        if redacted != message:
            record.msg = redacted
            record.args = None
        return True


def setup_logging(
    logs_dir: Path,
    level: str = "INFO",
    secrets: Iterable[str] = (),
) -> logging.Logger:
    """Configure le journal de l'application et renvoie son logger racine.

    Peut être appelée plusieurs fois (Streamlit relance le script à chaque
    interaction) sans dupliquer les lignes du journal.
    """
    logs_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.propagate = False
    _remove_handlers(logger)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    redaction = SecretRedactionFilter(secrets)
    for handler in (_build_file_handler(logs_dir), logging.StreamHandler()):
        handler.setFormatter(formatter)
        handler.addFilter(redaction)
        logger.addHandler(handler)

    for name in NOISY_LIBRARIES:
        logging.getLogger(name).setLevel(logging.WARNING)
    return logger


def setup_logging_from_settings(settings: Settings) -> logging.Logger:
    """Configure le journal à partir des réglages, en masquant le mot de passe de démo."""
    secrets = [settings.demo_password.get_secret_value()] if settings.demo_password else []
    return setup_logging(settings.logs_dir, settings.log_level, secrets)


def get_logger(module_name: str) -> logging.Logger:
    """Renvoie le logger d'un module, rattaché au journal de l'application."""
    return logging.getLogger(f"{LOGGER_NAME}.{module_name}")


def _build_file_handler(logs_dir: Path) -> RotatingFileHandler:
    """Crée le fichier de journal tournant, encodé en UTF-8."""
    return RotatingFileHandler(
        logs_dir / LOG_FILE_NAME,
        maxBytes=MAX_LOG_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )


def _remove_handlers(logger: logging.Logger) -> None:
    """Ferme et retire les gestionnaires existants (libère le fichier sous Windows)."""
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)
