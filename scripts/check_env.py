"""Contrôle santé de la machine avant de lancer l'assistant.

Usage, depuis la racine du projet :

    .venv\\Scripts\\python -m scripts.check_env

Vérifie Python, l'environnement virtuel, les bibliothèques, la RAM, le disque,
le fichier .env, Ollama et la présence des deux modèles. Code de sortie 0 si
aucun contrôle n'est en échec, 1 sinon.
"""

import importlib.util
import json
import shutil
import sys
import urllib.error
import urllib.request
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import Enum

from pydantic import ValidationError

from config import PROJECT_ROOT, Settings

SUPPORTED_PYTHON: tuple[tuple[int, int], ...] = ((3, 11), (3, 12))
REQUIRED_MODULES: dict[str, str] = {
    "chromadb": "chromadb",
    "streamlit": "streamlit",
    "fitz": "pymupdf",
    "ollama": "ollama",
    "pydantic_settings": "pydantic-settings",
    "psutil": "psutil",
    "tqdm": "tqdm",
}
MIN_RAM_GB = 8.0
MIN_FREE_DISK_GB = 10.0
OLLAMA_TIMEOUT_S = 5.0
GB = 1024**3
ENV_EXAMPLE_PATH = PROJECT_ROOT / ".env.example"
ENV_PATH = PROJECT_ROOT / ".env"
PASSWORD_KEY = "ASSISTANT_DEMO_PASSWORD"


class Status(Enum):
    """Résultat d'un contrôle."""

    OK = "OK"
    WARNING = "ATTENTION"
    FAILED = "ECHEC"


@dataclass(frozen=True)
class CheckResult:
    """Résultat d'un contrôle : nom, statut, constat et conseil éventuel."""

    name: str
    status: Status
    message: str
    advice: str = ""


def check_python_version(version: tuple[int, int] | None = None) -> CheckResult:
    """Vérifie que la version de Python est 3.11 ou 3.12."""
    current = version or (sys.version_info.major, sys.version_info.minor)
    label = f"{current[0]}.{current[1]}"
    if current in SUPPORTED_PYTHON:
        return CheckResult("Python", Status.OK, f"Python {label}")
    return CheckResult(
        "Python", Status.FAILED, f"Python {label} non pris en charge", "Installez Python 3.12."
    )


def check_virtualenv(prefix: str | None = None, base_prefix: str | None = None) -> CheckResult:
    """Vérifie que le script tourne dans un environnement virtuel."""
    if (prefix or sys.prefix) != (base_prefix or sys.base_prefix):
        return CheckResult("Environnement virtuel", Status.OK, "actif")
    return CheckResult(
        "Environnement virtuel",
        Status.WARNING,
        "non actif",
        "Lancez le script avec .venv\\Scripts\\python.",
    )


def check_modules(is_available: Callable[[str], bool] | None = None) -> CheckResult:
    """Vérifie que les bibliothèques nécessaires sont installées."""
    available = is_available or _module_is_installed
    missing = [package for module, package in REQUIRED_MODULES.items() if not available(module)]
    if not missing:
        return CheckResult("Bibliothèques", Status.OK, f"{len(REQUIRED_MODULES)} présentes")
    return CheckResult(
        "Bibliothèques",
        Status.FAILED,
        f"manquantes : {', '.join(missing)}",
        "Lancez : .venv\\Scripts\\python -m pip install -r requirements.txt",
    )


def check_ram(total_bytes: int | None = None) -> CheckResult:
    """Vérifie que la machine a au moins 8 Go de RAM."""
    if total_bytes is None:
        try:
            import psutil
        except ImportError:
            return CheckResult("RAM", Status.WARNING, "impossible à mesurer (psutil absent)")
        total_bytes = psutil.virtual_memory().total
    total_gb = total_bytes / GB
    if total_gb >= MIN_RAM_GB:
        return CheckResult("RAM", Status.OK, f"{total_gb:.1f} Go")
    return CheckResult(
        "RAM",
        Status.WARNING,
        f"{total_gb:.1f} Go (moins de {MIN_RAM_GB:.0f} Go)",
        "Le modèle risque d'être lent ou de manquer de mémoire.",
    )


def check_disk(free_bytes: int | None = None) -> CheckResult:
    """Vérifie qu'il reste au moins 10 Go libres sur le disque du projet."""
    free = free_bytes if free_bytes is not None else shutil.disk_usage(PROJECT_ROOT).free
    free_gb = free / GB
    if free_gb >= MIN_FREE_DISK_GB:
        return CheckResult("Disque", Status.OK, f"{free_gb:.0f} Go libres")
    return CheckResult(
        "Disque",
        Status.WARNING,
        f"{free_gb:.1f} Go libres",
        f"Prévoyez au moins {MIN_FREE_DISK_GB:.0f} Go pour les modèles et l'index.",
    )


def check_env_file(settings: Settings, example_password: str | None) -> CheckResult:
    """Vérifie que le .env existe et que le mot de passe n'est pas la valeur d'exemple."""
    if not ENV_PATH.exists():
        return CheckResult(
            "Fichier .env", Status.WARNING, "absent", "Lancez : Copy-Item .env.example .env"
        )
    if settings.demo_password is None:
        return CheckResult(
            "Fichier .env", Status.FAILED, f"{PASSWORD_KEY} manquant", "Ajoutez-le dans .env."
        )
    if settings.demo_password.get_secret_value() == example_password:
        return CheckResult(
            "Fichier .env",
            Status.WARNING,
            "mot de passe d'exemple encore utilisé",
            "Changez ASSISTANT_DEMO_PASSWORD dans .env avant la démo.",
        )
    return CheckResult("Fichier .env", Status.OK, "présent, mot de passe personnalisé")


def check_ollama_and_models(
    settings: Settings, fetch: Callable[[str], list[str]] | None = None
) -> list[CheckResult]:
    """Vérifie qu'Ollama répond puis, si oui, que les deux modèles sont installés."""
    try:
        installed = (fetch or fetch_ollama_models)(settings.ollama_host)
    except (urllib.error.URLError, OSError, ValueError):
        return [
            CheckResult(
                "Ollama",
                Status.FAILED,
                f"injoignable sur {settings.ollama_host}",
                "Installez Ollama puis lancez-le (icône près de l'horloge).",
            )
        ]
    ollama_ok = CheckResult("Ollama", Status.OK, f"actif, {len(installed)} modèle(s) installé(s)")
    return [ollama_ok, check_models([settings.llm_model, settings.embed_model], installed)]


def check_models(wanted: Iterable[str], installed: Iterable[str]) -> CheckResult:
    """Vérifie que les modèles attendus sont installés dans Ollama."""
    installed_set = set(installed)
    missing = [name for name in wanted if not model_is_installed(name, installed_set)]
    if not missing:
        return CheckResult("Modèles", Status.OK, "tous présents")
    return CheckResult(
        "Modèles",
        Status.FAILED,
        f"manquants : {', '.join(missing)}",
        "Lancez : ollama pull <modèle>, ou copiez le dossier .ollama\\models.",
    )


def model_is_installed(wanted: str, installed: set[str]) -> bool:
    """Indique si un modèle est installé (« bge-m3 » correspond à « bge-m3:latest »)."""
    candidates = {wanted} if ":" in wanted else {wanted, f"{wanted}:latest"}
    return not candidates.isdisjoint(installed)


def fetch_ollama_models(host: str) -> list[str]:
    """Interroge le serveur Ollama local et renvoie les noms des modèles installés."""
    with urllib.request.urlopen(f"{host}/api/tags", timeout=OLLAMA_TIMEOUT_S) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return [model["name"] for model in payload.get("models", [])]


def read_example_password() -> str | None:
    """Lit la valeur d'exemple du mot de passe dans .env.example."""
    if not ENV_EXAMPLE_PATH.exists():
        return None
    for line in ENV_EXAMPLE_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith(f"{PASSWORD_KEY}="):
            return line.split("=", 1)[1].strip()
    return None


def run_checks() -> list[CheckResult]:
    """Exécute tous les contrôles, dans l'ordre, et renvoie leurs résultats."""
    results = [check_python_version(), check_virtualenv(), check_modules(), check_ram()]
    results.append(check_disk())
    try:
        settings = Settings()
    except ValidationError as error:
        results.append(CheckResult("Configuration", Status.FAILED, _first_error(error)))
        return results
    results.append(check_env_file(settings, read_example_password()))
    results.extend(check_ollama_and_models(settings))
    return results


def format_result(result: CheckResult) -> str:
    """Met en forme un résultat sur une ou deux lignes."""
    line = f"[{result.status.value:<9}] {result.name:<22} {result.message}"
    return f"{line}\n{'':12}-> {result.advice}" if result.advice else line


def main() -> int:
    """Affiche le résultat de chaque contrôle et renvoie le code de sortie."""
    sys.stdout.reconfigure(errors="replace")
    print("Contrôle de l'environnement — Assistant IA interne sécurisé\n")
    results = run_checks()
    for result in results:
        print(format_result(result))
    failed = sum(result.status is Status.FAILED for result in results)
    print(f"\n{len(results)} contrôles, {failed} en échec.")
    return 1 if failed else 0


def _module_is_installed(module: str) -> bool:
    """Indique si un module Python est installé, sans l'importer."""
    return importlib.util.find_spec(module) is not None


def _first_error(error: ValidationError) -> str:
    """Renvoie le premier message d'erreur de validation, lisible."""
    first = error.errors()[0]
    return str(first.get("msg", error))


if __name__ == "__main__":
    sys.exit(main())
