"""Essai réel des 5 questions de démonstration, avec mesure des temps de réponse.

Usage, depuis la racine du projet (Ollama lancé, corpus indexé) :

    .venv\\Scripts\\python -m scripts.demo_check

Les modèles sont d'abord déchargés de la mémoire (`ollama stop`) pour mesurer une
vraie première question, chargement compris. Les questions suivantes profitent du
keep_alive : les modèles restent chargés.
"""

import shutil
import subprocess
import sys
from dataclasses import dataclass

from config import get_settings
from rag.logging_setup import setup_logging_from_settings
from rag.models import Answer
from rag.pipeline import create_runtime
from rag.textutils import normalize_for_matching


@dataclass(frozen=True)
class DemoQuestion:
    """Question de démonstration et ce que la réponse doit contenir."""

    label: str
    question: str
    expected: tuple[str, ...]
    cited_page: tuple[str, int] | None
    must_refuse: bool = False


DEMO_QUESTIONS: tuple[DemoQuestion, ...] = (
    DemoQuestion(
        "Directe",
        "Quel est le montant maximal d'un premier crédit ?",
        ("500 000",),
        ("Politique et procédure d'octroi de crédit", 4),
    ),
    DemoQuestion(
        "Reformulée",
        "Je me marie le mois prochain, j'ai droit à combien de jours ?",
        ("4 jours",),
        ("Procédure de demande de congés", 2),
    ),
    DemoQuestion(
        "Piège 2025/2026",
        "Quel est le taux du crédit pour activité génératrice de revenus ?",
        ("21 %",),
        ("Grille des taux et frais 2026", 2),
    ),
    DemoQuestion(
        "Réserve (Q2)",
        "Qu'arrive-t-il si un membre d'un groupement ne rembourse pas ?",
        ("place",),
        ("Crédit solidaire aux groupements", 3),
    ),
    DemoQuestion(
        "Sans réponse",
        "L'institution autorise-t-elle le télétravail ?",
        (),
        None,
        must_refuse=True,
    ),
)


def unload_models(models: tuple[str, ...]) -> None:
    """Décharge les modèles de la mémoire d'Ollama, pour mesurer un démarrage à froid."""
    ollama = shutil.which("ollama")
    if ollama is None:
        return
    for model in models:
        subprocess.run([ollama, "stop", model], capture_output=True, check=False)


def check(demo: DemoQuestion, answer: Answer) -> tuple[bool, str]:
    """Vérifie une réponse : refus attendu, ou contenu et page citée attendus."""
    if demo.must_refuse:
        return answer.refused, "refus correct" if answer.refused else "devait refuser"
    if answer.refused:
        return False, "refus à tort"
    text = normalize_for_matching(answer.text)
    missing = [item for item in demo.expected if normalize_for_matching(item) not in text]
    cited = {(s.title, s.page_number) for s in answer.cited_sources}
    page_ok = demo.cited_page in cited
    problems = [f"manque « {m} »" for m in missing]
    if not page_ok:
        problems.append(f"page attendue non citée : {demo.cited_page}")
    return not problems, "correcte et citée" if not problems else " ; ".join(problems)


def main() -> int:
    """Pose les questions, affiche réponses, sources, temps et bilan."""
    sys.stdout.reconfigure(errors="replace")
    settings = get_settings()
    setup_logging_from_settings(settings)
    runtime = create_runtime(settings, test_double=False)
    unload_models((settings.llm_model, settings.embed_model))
    results: list[tuple[DemoQuestion, Answer, bool, str]] = []
    for index, demo in enumerate(DEMO_QUESTIONS, start=1):
        answer = runtime.pipeline.ask(demo.question)
        ok, verdict = check(demo, answer)
        results.append((demo, answer, ok, verdict))
        cited = ", ".join(s.label for s in answer.cited_sources) or "aucune"
        print(f"\n[{index}] {demo.label} — {demo.question}")
        print(f"    Réponse ({answer.duration_s:.1f} s) : {answer.text}")
        print(f"    Sources citées : {cited}")
        print(f"    Meilleure similarité : {answer.best_score:.3f}" if answer.best_score else "")
        print(f"    Verdict : {'OK' if ok else 'ÉCHEC'} — {verdict}")
    durations = [answer.duration_s for _, answer, _, _ in results]
    following = durations[1:]
    print("\nTemps de réponse")
    print(f"    Première question (modèles chargés à froid) : {durations[0]:.1f} s")
    print(
        f"    Questions suivantes : moyenne {sum(following) / len(following):.1f} s, "
        f"maximum {max(following):.1f} s"
    )
    passed = sum(ok for _, _, ok, _ in results)
    print(f"\n{passed}/{len(results)} questions conformes.")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
