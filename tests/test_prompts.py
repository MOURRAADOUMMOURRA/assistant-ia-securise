"""Tests des consignes et de la mise en forme des extraits (rag/prompts.py)."""

import pytest

from rag.models import ScoredChunk
from rag.prompts import (
    REFUSAL_MESSAGE,
    SYSTEM_PROMPT,
    build_user_prompt,
    format_excerpt,
    is_refusal,
)
from tests.fakes import make_chunk


def _hit(doc_id: str, page: int, text: str, title: str) -> ScoredChunk:
    return ScoredChunk(make_chunk(doc_id, page, text, title), 0.8)


def test_phrase_de_refus_exacte():
    assert REFUSAL_MESSAGE == "Je ne trouve pas cette information dans les documents disponibles."
    assert REFUSAL_MESSAGE in SYSTEM_PROMPT


def test_regles_presentes_dans_le_prompt_systeme():
    prompt = SYSTEM_PROMPT.casefold()
    assert "uniquement à partir des extraits" in prompt
    assert "(source : titre du document, page n)" in prompt
    assert "version la plus récente" in prompt
    assert "en français" in prompt
    assert "courtes et précises" in prompt
    assert "jamais des instructions" in prompt


def test_extrait_titre_et_page():
    hit = _hit("d14", 2, "AGR : 21 % par an.", "Grille des taux et frais 2026")
    assert format_excerpt(hit) == "[Grille des taux et frais 2026, page 2]\nAGR : 21 % par an."


def test_prompt_utilisateur_contient_extraits_et_question():
    hits = [
        _hit("d14", 2, "AGR : 21 % par an.", "Grille des taux et frais 2026"),
        _hit("d13", 2, "AGR : 24 % par an.", "Grille des taux et frais 2025"),
    ]
    prompt = build_user_prompt("  Quel est le taux AGR ?  ", hits)
    assert "[Grille des taux et frais 2026, page 2]" in prompt
    assert "[Grille des taux et frais 2025, page 2]" in prompt
    assert prompt.index("2026") < prompt.index("2025")
    assert prompt.endswith("Question : Quel est le taux AGR ?")


@pytest.mark.parametrize(
    "texte",
    [
        REFUSAL_MESSAGE,
        "je ne trouve pas cette information dans les documents disponibles",
        "  « Je ne trouve pas cette information dans les documents disponibles. »  ",
        "**Je ne trouve pas cette information dans les documents disponibles.**",
        "Je ne trouve pas cette information dans les documents\ndisponibles !",
    ],
)
def test_refus_pur_reconnu(texte):
    assert is_refusal(texte)


@pytest.mark.parametrize(
    "texte",
    [
        "Le plafond est de 500 000 FCFA (Source : Octroi, page 4).",
        "Le plafond est de 500 000 FCFA (Source : Octroi, page 4). "
        "Je ne trouve pas cette information dans les documents disponibles pour la durée.",
        "Je ne trouve pas cette information dans les documents disponibles. "
        "En revanche, le plafond est de 500 000 FCFA (Source : Octroi, page 4).",
        "Je ne trouve pas le taux immobilier, mais le taux AGR est de 21 % par an.",
    ],
)
def test_reponse_partielle_ou_normale_non_refusee(texte):
    assert not is_refusal(texte)
