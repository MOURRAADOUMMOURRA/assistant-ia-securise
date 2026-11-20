"""Doublures locales du modèle d'embedding et du LLM, pour tester le parcours sans Ollama.

- `HashEmbedder` : embedding « sac de mots » déterministe. Deux textes qui partagent
  des mots sont proches. Aucune compréhension du sens : c'est un outil de test.
- `ExtractiveGenerator` : faux LLM qui recopie le passage le plus pertinent reçu et
  cite sa source. Il ne génère rien : il prouve que le circuit fonctionne.

Les réponses produites en mode doublure sont clairement signalées comme telles.
"""

import hashlib
import math
import re
from collections.abc import Sequence

from rag.prompts import REFUSAL_MESSAGE
from rag.textutils import normalize_for_matching

DOUBLE_EMBED_MODEL = "doublure-hachage"
"""Nom du « modèle » de la doublure : il donne sa propre collection dans l'index."""

DOUBLE_THRESHOLD = 0.25
"""Seuil de similarité adapté à l'embedding par hachage (différent de celui de bge-m3)."""

DOUBLE_ANSWER_PREFIX = "Mode doublure (sans IA)"
DIMENSIONS = 256
EXCERPT_CHARS = 260

_WORD = re.compile(r"\w+", re.UNICODE)
_FIRST_EXCERPT = re.compile(
    r"\[(?P<title>.+?), page (?P<page>\d+)\]\n(?P<text>.+?)(?:\n\n---|\n\nQuestion :)", re.DOTALL
)
_STOPWORDS = frozenset(
    {
        "le", "la", "les", "l", "un", "une", "des", "de", "du", "d", "et", "ou", "à", "au",
        "aux", "en", "est", "il", "elle", "on", "ce", "ces", "se", "sa", "son", "ses", "qui",
        "que", "quoi", "quel", "quelle", "quels", "quelles", "pour", "par", "sur", "dans",
        "avec", "pas", "ne", "plus", "je", "tu", "nous", "vous", "ils", "elles", "y", "a",
        "combien", "comment", "faut", "être", "avoir",
    }
)  # fmt: skip


class HashEmbedder:
    """Embedding déterministe par hachage des mots (sans les mots vides)."""

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Renvoie un vecteur normalisé de 256 dimensions par texte."""
        return [_vectorize(text) for text in texts]


class ExtractiveGenerator:
    """Faux LLM : recopie le début du premier extrait reçu et cite sa source."""

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Construit une réponse extractive à partir du prompt utilisateur."""
        match = _FIRST_EXCERPT.search(user_prompt)
        if match is None:
            return REFUSAL_MESSAGE
        text = " ".join(match["text"].split())
        excerpt = (
            text if len(text) <= EXCERPT_CHARS else text[:EXCERPT_CHARS].rsplit(" ", 1)[0] + "…"
        )
        return (
            f"{DOUBLE_ANSWER_PREFIX} : passage le plus proche de votre question. "
            f"« {excerpt} » (Source : {match['title']}, page {match['page']})"
        )


def _vectorize(text: str) -> list[float]:
    """Projette chaque mot utile sur une dimension stable, puis normalise le vecteur."""
    vector = [0.0] * DIMENSIONS
    for word in _WORD.findall(normalize_for_matching(text)):
        if word in _STOPWORDS:
            continue
        digest = hashlib.md5(word.encode("utf-8"), usedforsecurity=False).digest()
        vector[int.from_bytes(digest[:2], "big") % DIMENSIONS] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]
