"""Erreurs métier de l'assistant, chacune avec un message clair pour l'utilisateur.

L'interface affiche `user_message` ; elle ne montre jamais une trace Python brute.
"""


class AssistantError(Exception):
    """Erreur de base de l'assistant, porteuse d'un message lisible en français."""

    default_message = "Une erreur inattendue est survenue."

    def __init__(self, user_message: str | None = None) -> None:
        """Enregistre le message destiné à l'utilisateur."""
        self.user_message = user_message or self.default_message
        super().__init__(self.user_message)


class UnsupportedFormatError(AssistantError):
    """Le fichier fourni n'est pas un PDF."""

    default_message = "Exportez votre document en PDF (Fichier › Enregistrer sous › PDF)."


class UnreadablePdfError(AssistantError):
    """Le PDF est endommagé, protégé ou ne contient pas de texte."""

    default_message = "Ce PDF est illisible (fichier endommagé, protégé ou sans texte)."


class OllamaUnavailableError(AssistantError):
    """Le serveur Ollama local ne répond pas."""

    default_message = (
        "Le moteur d'IA local (Ollama) ne répond pas. "
        "Lancez Ollama (icône près de l'horloge), puis réessayez."
    )


class OllamaTimeoutError(AssistantError):
    """Ollama a mis trop de temps à répondre."""

    default_message = (
        "Le moteur d'IA local a mis trop de temps à répondre. "
        "Réessayez : la première question est plus lente, le temps de charger le modèle."
    )


class ModelNotFoundError(AssistantError):
    """Le modèle demandé n'est pas installé dans Ollama."""

    def __init__(self, model: str) -> None:
        """Construit le message à partir du nom du modèle manquant."""
        self.model = model
        super().__init__(
            f"Le modèle « {model} » n'est pas installé. "
            f"Lancez : ollama pull {model} (ou copiez le dossier .ollama\\models)."
        )


class EmptyIndexError(AssistantError):
    """L'index des documents est vide : rien à rechercher."""

    default_message = "Aucun document n'est indexé. Lancez : .venv\\Scripts\\python -m rag.indexer"
