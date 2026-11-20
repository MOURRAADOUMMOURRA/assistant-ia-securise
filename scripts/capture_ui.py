"""Captures d'écran de l'interface et vérification « aucune requête vers Internet ».

Usage, depuis la racine du projet (outil de développement) :

    .venv\\Scripts\\python -m scripts.capture_ui

Le script lance l'application sur un port de test, avec un mot de passe temporaire
tiré au hasard (le .env n'est pas utilisé pour cela), puis pilote Microsoft Edge en
mode invisible via le protocole de débogage (CDP) :

1. il parcourt l'application comme un utilisateur et enregistre des captures ;
2. il note toutes les requêtes réseau émises par la page ;
3. il surveille les connexions réseau du serveur Streamlit pendant toute la session.

Le rapport liste toute requête ou connexion vers une adresse qui n'est pas locale.
"""

import base64
import itertools
import json
import os
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

import psutil
from websockets.sync.client import connect

from config import PROJECT_ROOT

EDGE = Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")) / (
    "Microsoft/Edge/Application/msedge.exe"
)
APP_PORT = 8599
CDP_PORT = 9333
OUT_DIR = PROJECT_ROOT / "docs" / "captures"
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", "[::1]"}
LOCAL_SCHEMES = {"data", "blob", "about", "chrome", "edge", "devtools"}
VIEWPORT = (1440, 1000)
TALL_VIEWPORT = 1700


class Browser:
    """Pilotage minimal d'un onglet Edge par le protocole CDP."""

    def __init__(self, ws_url: str) -> None:
        self._ws = connect(ws_url, max_size=50_000_000)
        self._ids = itertools.count(1)
        self.requests: list[str] = []

    def send(self, method: str, **params: object) -> dict:
        """Envoie une commande et attend sa réponse, en notant les événements réseau."""
        message_id = next(self._ids)
        self._ws.send(json.dumps({"id": message_id, "method": method, "params": params}))
        while True:
            message = json.loads(self._ws.recv())
            if message.get("method") == "Network.requestWillBeSent":
                self.requests.append(message["params"]["request"]["url"])
            if message.get("id") == message_id:
                return message.get("result", {})

    def js(self, expression: str) -> object:
        """Évalue du JavaScript dans la page et renvoie le résultat."""
        result = self.send("Runtime.evaluate", expression=expression, returnByValue=True)
        return result.get("result", {}).get("value")

    def wait_for(self, expression: str, timeout: float = 90.0) -> None:
        """Attend qu'une condition JavaScript devienne vraie."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.js(expression):
                return
            time.sleep(0.5)
        raise TimeoutError(f"Condition non remplie : {expression}")

    def click_text(self, selector: str, text: str) -> None:
        """Clique sur le premier élément `selector` dont le texte contient `text`."""
        found = self.js(
            f"(() => {{ const el = [...document.querySelectorAll({json.dumps(selector)})]"
            f".find(e => e.innerText.includes({json.dumps(text)}));"
            " if (!el) return false; el.scrollIntoView({block: 'center'}); el.click();"
            " return true; })()"
        )
        if not found:
            raise RuntimeError(f"Élément introuvable : {selector} « {text} »")

    def type_password(self, value: str) -> None:
        """Saisit une valeur dans le champ mot de passe (compatible React)."""
        self.js(
            "(() => { const i = document.querySelector('input[type=password]');"
            " const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,"
            " 'value').set;"
            f" set.call(i, {json.dumps(value)});"
            " i.dispatchEvent(new Event('input', {bubbles: true})); })()"
        )

    def screenshot(self, name: str) -> Path:
        """Enregistre une capture PNG de la fenêtre."""
        time.sleep(1.2)
        data = self.send("Page.captureScreenshot", format="png")["data"]
        path = OUT_DIR / name
        path.write_bytes(base64.b64decode(data))
        print(f"  capture : {path.relative_to(PROJECT_ROOT)}")
        return path


def is_local(url: str) -> bool:
    """Indique si une URL reste sur la machine locale."""
    parsed = urlparse(url)
    return parsed.scheme in LOCAL_SCHEMES or (parsed.hostname or "") in LOCAL_HOSTS


def external_connections(pid: int) -> set[str]:
    """Connexions réseau du processus et de ses enfants vers une adresse non locale."""
    found: set[str] = set()
    try:
        process = psutil.Process(pid)
        for proc in [process, *process.children(recursive=True)]:
            for conn in proc.net_connections(kind="inet"):
                if conn.raddr and conn.raddr.ip not in {"127.0.0.1", "::1"}:
                    found.add(f"{conn.raddr.ip}:{conn.raddr.port}")
    except psutil.Error:
        pass
    return found


def wait_http(url: str, timeout: float = 90.0) -> object:
    """Attend qu'une URL locale réponde, puis renvoie le JSON ou le texte reçu."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                body = response.read().decode("utf-8")
            return json.loads(body) if body.startswith(("{", "[")) else body
        except OSError:
            time.sleep(0.5)
    raise TimeoutError(url)


def start_app(password: str) -> subprocess.Popen:
    """Lance Streamlit sur le port de test, sans le mode doublure imposé."""
    env = {**os.environ, "ASSISTANT_DEMO_PASSWORD": password, "ASSISTANT_TEST_DOUBLE": "false"}
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(PROJECT_ROOT / "app" / "main.py"),
        "--server.port",
        str(APP_PORT),
        "--server.headless",
        "true",
    ]
    return subprocess.Popen(
        command,
        cwd=PROJECT_ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def start_edge(profile: Path) -> subprocess.Popen:
    """Lance Edge en mode invisible avec le port de débogage."""
    command = [
        str(EDGE),
        "--headless=new",
        "--disable-gpu",
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={profile}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-networking",
        "--disable-component-update",
        "--disable-sync",
        "--disable-extensions",
        f"--window-size={VIEWPORT[0]},{VIEWPORT[1]}",
        "--lang=fr-FR",
        "about:blank",
    ]
    return subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def scenario(browser: Browser, password: str, app_pid: int) -> set[str]:
    """Parcours utilisateur complet ; renvoie les connexions externes du serveur."""
    seen: set[str] = set()
    url = f"http://localhost:{APP_PORT}"
    browser.send("Page.navigate", url=url)
    browser.wait_for("!!document.querySelector('input[type=password]')")
    browser.screenshot("01_connexion.png")

    browser.type_password("mauvais-mot-de-passe")
    browser.click_text("button", "Se connecter")
    browser.wait_for("document.body.innerText.includes('Mot de passe incorrect')")
    browser.screenshot("02_mot_de_passe_faux.png")
    seen |= external_connections(app_pid)

    browser.type_password(password)
    browser.click_text("button", "Se connecter")
    browser.wait_for('document.body.innerText.includes("Questions d\'exemple")')
    browser.screenshot("03_accueil_sans_ollama.png")

    browser.click_text("button", "Question directe")
    browser.wait_for("document.body.innerText.includes('ne répond pas')")
    browser.screenshot("04_message_ollama_arrete.png")
    seen |= external_connections(app_pid)

    browser.js(
        "[...document.querySelectorAll('label')].find(l => l.innerText.includes("
        "'Mode doublure')).querySelector('input').click()"
    )
    browser.wait_for("document.body.innerText.includes('Mode doublure : les réponses')")
    browser.click_text("button", "Question directe")
    browser.wait_for("document.body.innerText.split('Réponse en').length > 1", timeout=180)
    browser.js("document.querySelector('[data-testid=\"stChatInput\"]')?.scrollIntoView()")
    browser.screenshot("05_reponse_et_sources.png")

    browser.click_text("button", "Voir la page")
    browser.wait_for(
        "[...document.querySelectorAll('img')].some(i => i.naturalWidth > 600)", timeout=60
    )
    browser.send(
        "Emulation.setDeviceMetricsOverride",
        width=VIEWPORT[0],
        height=TALL_VIEWPORT,
        deviceScaleFactor=1,
        mobile=False,
    )
    time.sleep(1.5)
    browser.js(
        "[...document.querySelectorAll('img')].filter(i => i.naturalWidth > 600)[0]"
        ".scrollIntoView({block: 'start'})"
    )
    browser.screenshot("06_page_surlignee.png")
    browser.send(
        "Emulation.setDeviceMetricsOverride",
        width=VIEWPORT[0],
        height=VIEWPORT[1],
        deviceScaleFactor=1,
        mobile=False,
    )

    browser.click_text("button", "Piège 2025 / 2026")
    browser.wait_for("document.body.innerText.split('Réponse en').length > 2", timeout=120)
    browser.click_text("summary", "Sources consultées")
    browser.js("document.querySelector('[data-testid=\"stChatInput\"]')?.scrollIntoView()")
    browser.screenshot("07_sources_consultees.png")
    return seen | external_connections(app_pid)


def main() -> int:
    """Lance l'application et Edge, déroule le scénario et affiche le rapport."""
    sys.stdout.reconfigure(errors="replace")
    if not EDGE.exists():
        print(f"Microsoft Edge introuvable : {EDGE}")
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    password = secrets.token_urlsafe(18)
    profile = Path(tempfile.mkdtemp(prefix="edge_capture_"))
    app = start_app(password)
    edge = start_edge(profile)
    try:
        wait_http(f"http://localhost:{APP_PORT}/_stcore/health")
        targets = wait_http(f"http://127.0.0.1:{CDP_PORT}/json")
        page = next(t for t in targets if t.get("type") == "page")
        browser = Browser(page["webSocketDebuggerUrl"])
        browser.send("Network.enable")
        browser.send("Page.enable")
        browser.send(
            "Emulation.setDeviceMetricsOverride",
            width=VIEWPORT[0],
            height=VIEWPORT[1],
            deviceScaleFactor=1,
            mobile=False,
        )
        print("Parcours de l'interface :")
        server_external = scenario(browser, password, app.pid)
    finally:
        for process in (edge, app):
            for child in psutil.Process(process.pid).children(recursive=True):
                child.kill()
            process.kill()
        shutil.rmtree(profile, ignore_errors=True)
    external = sorted({url for url in browser.requests if not is_local(url)})
    print(f"\nRequêtes émises par la page : {len(browser.requests)}")
    print(f"Requêtes vers une adresse non locale : {len(external)}")
    for url in external:
        print(f"  - {url}")
    print(f"Connexions du serveur vers une adresse non locale : {len(server_external)}")
    for address in sorted(server_external):
        print(f"  - {address}")
    return 0 if not external and not server_external else 1


if __name__ == "__main__":
    sys.exit(main())
