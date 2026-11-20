"""Point d'entrée unique du moteur RAG : `ask(question) -> Answer`.

Étapes : recherche des extraits → seuil (refus immédiat, sans LLM, si rien de
pertinent) → génération → sources construites depuis les métadonnées des
extraits retrouvés. Le texte du LLM sert seulement à marquer les sources
citées : une citation inventée n'apparaît donc jamais dans les sources.
"""

import re
import time
from collections.abc import Callable, Sequence
from functools import lru_cache

from config import Settings, get_settings
from rag.llm import Generator, OllamaClient
from rag.logging_setup import get_logger
from rag.models import Answer, ScoredChunk, Source
from rag.prompts import REFUSAL_MESSAGE, SYSTEM_PROMPT, build_user_prompt, is_refusal
from rag.retrieval import Retriever
from rag.vectorstore import VectorStore

EMPTY_QUESTION_MESSAGE = "Posez une question sur les documents internes."

_APOSTROPHES = str.maketrans({"’": "'", "‘": "'", "`": "'"})
_SPACES = re.compile(r"\s+")

logger = get_logger(__name__)


class RagPipeline:
    """Chaîne complète question → réponse citée."""

    def __init__(
        self,
        retriever: Retriever,
        generator: Generator,
        clock: Callable[[], float] = time.perf_counter,
    ) -> None:
        """Assemble la recherche et la génération."""
        self._retriever = retriever
        self._generator = generator
        self._clock = clock

    def ask(self, question: str) -> Answer:
        """Répond à une question à partir des documents indexés."""
        started = self._clock()
        question = question.strip()
        if not question:
            return Answer(EMPTY_QUESTION_MESSAGE, refused=True)

        retrieval = self._retriever.retrieve(question)
        if not retrieval.is_relevant:
            answer = Answer(
                REFUSAL_MESSAGE,
                refused=True,
                duration_s=self._clock() - started,
                best_score=retrieval.best_score,
            )
            _log_answer(answer, llm_called=False)
            return answer

        text = self._generator.generate(SYSTEM_PROMPT, build_user_prompt(question, retrieval.hits))
        refused = is_refusal(text)
        answer = Answer(
            text=REFUSAL_MESSAGE if refused else text,
            sources=() if refused else build_sources(text, retrieval.hits),
            refused=refused,
            duration_s=self._clock() - started,
            best_score=retrieval.best_score,
        )
        _log_answer(answer, llm_called=True)
        return answer


def build_sources(answer_text: str, hits: Sequence[ScoredChunk]) -> tuple[Source, ...]:
    """Construit les sources depuis les métadonnées : une par page, la plus pertinente d'abord."""
    sources: dict[tuple[str, int], Source] = {}
    for hit in sorted(hits, key=lambda h: h.score, reverse=True):
        chunk = hit.chunk
        key = (chunk.doc_id, chunk.page_number)
        if key in sources:
            continue
        sources[key] = Source(
            doc_id=chunk.doc_id,
            title=chunk.title,
            source_path=chunk.source_path,
            page_number=chunk.page_number,
            page_count=chunk.page_count,
            excerpt=chunk.text,
            score=hit.score,
            cited=is_cited(answer_text, chunk.title, chunk.page_number),
        )
    return tuple(sources.values())


def is_cited(answer_text: str, title: str, page_number: int) -> bool:
    """Indique si la réponse cite « Titre, page N » (casse, espaces et apostrophes ignorés)."""
    pattern = re.escape(_normalize(title)) + rf"\W{{0,5}}(?:page|p\.)\s*{page_number}\b"
    return re.search(pattern, _normalize(answer_text)) is not None


def build_pipeline(settings: Settings) -> RagPipeline:
    """Construit le pipeline réel : Ollama local et index ChromaDB sur disque."""
    client = OllamaClient(settings)
    store = VectorStore(settings.index_dir, settings.embed_model)
    retriever = Retriever(client, store, settings.top_k, settings.similarity_threshold)
    return RagPipeline(retriever, client)


@lru_cache(maxsize=1)
def default_pipeline() -> RagPipeline:
    """Pipeline construit une seule fois à partir des réglages du fichier .env."""
    return build_pipeline(get_settings())


def ask(question: str) -> Answer:
    """Point d'entrée unique : répond à une question avec le pipeline par défaut."""
    return default_pipeline().ask(question)


def _normalize(text: str) -> str:
    """Minuscules, apostrophes droites et espaces simples, pour comparer des citations."""
    return _SPACES.sub(" ", text.translate(_APOSTROPHES)).casefold()


def _log_answer(answer: Answer, llm_called: bool) -> None:
    """Journalise la durée, les sources et les documents cités, jamais la question."""
    cited = sorted({source.doc_id for source in answer.cited_sources})
    best = f"{answer.best_score:.3f}" if answer.best_score is not None else "-"
    logger.info(
        "Réponse en %.2f s | LLM appelé : %s | refus : %s | sources : %d | citées : %s | "
        "meilleure similarité : %s",
        answer.duration_s,
        "oui" if llm_called else "non",
        "oui" if answer.refused else "non",
        len(answer.sources),
        ", ".join(cited) or "aucune",
        best,
    )
