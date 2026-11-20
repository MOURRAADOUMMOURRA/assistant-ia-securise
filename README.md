# Assistant IA interne sécurisé — ZakiCortex

> Démonstration : un assistant qui répond aux questions des employés à partir des
> documents internes d'une institution, en citant le document et la page.
> **Tout fonctionne sur le PC, sans Internet.** README complet en préparation.

## Mot de passe de démo

L'interface refuse toute connexion tant que le mot de passe de démonstration n'est
pas configuré correctement. Message affiché : « Mot de passe de démo non configuré –
voir le README ».

Le mot de passe se règle dans le fichier `.env`, à la racine du projet, sur la ligne
`ASSISTANT_DEMO_PASSWORD=`. Il doit :

- faire **au moins 12 caractères** ;
- être **différent de la valeur d'exemple** de `.env.example`.

Pour le définir sans l'afficher à l'écran, dans PowerShell, à la racine du projet :

```powershell
$mdp = Read-Host "Nouveau mot de passe (12 caractères minimum)"
$lignes = (Get-Content .env -Encoding UTF8) -replace '^ASSISTANT_DEMO_PASSWORD=.*', "ASSISTANT_DEMO_PASSWORD=$mdp"
[IO.File]::WriteAllLines("$PWD\.env", $lignes, (New-Object Text.UTF8Encoding $false))
.\.venv\Scripts\python -m scripts.check_env
```

`check_env` doit afficher `[OK] Fichier .env`. Relancez ensuite l'application. Le
fichier `.env` n'est jamais publié (voir `.gitignore`).

## Mode doublure (tests)

Pour tester le parcours de l'interface sans Ollama, mettez `ASSISTANT_ALLOW_MOCK=true`
dans `.env` : une bascule « Mode doublure » apparaît alors dans la barre latérale.
Laissez `false` pour une démonstration client.
