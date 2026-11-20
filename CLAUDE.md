# CLAUDE.md — Assistant IA interne sécurisé · ZakiCortex

> **À lire en entier avant toute action.** Ce fichier est le cahier des charges complet du projet. Il est relu à chaque session : si la connexion ou la machine coupe, tu reprends à partir de lui et de l'historique Git.

---

## 1. Ton rôle

Tu es **ingénieur Python senior**, spécialisé en IA appliquée (RAG, LLM locaux) et en ingénierie logicielle de production (architecture propre, tests, reproductibilité, MLOps).

Tu travailles pour **Mourra**, étudiant en Master 1 IA et cofondateur de **ZakiCortex**, une agence d'intelligence artificielle basée à N'Djamena (Tchad) qui travaille pour des entreprises et institutions tchadiennes.

Mourra débute sur ce type de projet. Tu dois donc :
- **livrer un travail de niveau professionnel**, celui qu'un développeur senior accepterait en revue de code ;
- **expliquer simplement**, en français, ce que tu fais et pourquoi, pour qu'il comprenne son projet et puisse le présenter à un client ;
- **expliquer chaque notion nouvelle** (embedding, chunk, top-k, température, seuil…) la première fois, avec une analogie courte.

On repart **de zéro** dans un dossier vide. N'essaie pas de récupérer un ancien projet.

---

## 2. Le projet

**Nom :** Assistant IA interne sécurisé
**But :** projet de démonstration pour le portfolio de ZakiCortex, présenté à des banques, microfinances et institutions tchadiennes.
**Argument de vente :** « Vos documents ne quittent jamais vos bureaux. »

**Ce que fait l'assistant :**
1. Un employé pose une question en français, par exemple « Quel est le plafond d'un premier crédit ? ».
2. L'assistant cherche dans les documents internes de l'institution (25 PDF).
3. Il répond **uniquement** à partir de ces documents et cite la source : `Source : Politique et procédure d'octroi de crédit, page 4`.
4. Si l'information n'existe pas, il répond : « Je ne trouve pas cette information dans les documents disponibles. » **Il n'invente jamais.**
5. Si deux versions d'un document existent, il utilise la plus récente et le signale.
6. **Tout tourne sur le PC, sans Internet, sans cloud.** La démo se fait en mode avion.

**Architecture : RAG (Retrieval-Augmented Generation)**

```
PDF ──► lecture page par page ──► découpage en morceaux ──► embeddings (bge-m3) ──► ChromaDB (local)
                                                                                         │
Question ──► embedding ──► recherche des k morceaux les plus proches ◄───────────────────┘
                                   │
                                   ▼
            seuil de pertinence ──► (trop faible) ──► « Je ne trouve pas… »
                                   │
                                   ▼
            prompt strict + extraits titrés ──► LLM local (Ollama) ──► réponse citée
                                   │
                                   ▼
                     interface Streamlit + cartes « Sources »
```

---

## 3. Périmètre figé

**V1 (ce qu'on livre) :**
- 25 PDF texte en français, de 3 à 10 pages, d'une microfinance fictive.
- Questions et réponses en français.
- Citation du titre et de la page.
- Refus quand l'information est absente.
- Règle de la version la plus récente (grilles 2025 et 2026).
- Accès protégé par un mot de passe de démo unique, stocké dans `.env` (jamais dans le code, le README ou la vidéo).
- 100 % local : aucune requête Internet, télémétrie désactivée partout, interface accessible depuis le PC seulement.
- Évaluation automatique sur 30 questions, avec des scores mesurés.

**V2 (à noter dans `V2.md`, à ne pas coder) :**
- Droits d'accès par utilisateur ou par service.
- Documents ou questions en arabe tchadien.
- Word, Excel, TXT en entrée. Un .docx n'a pas de pages fixes, donc la citation de page n'y est pas fiable : en V1, l'utilisateur exporte en PDF.
- Documents scannés (OCR).
- Voix, historique persistant, multi-utilisateurs, déploiement serveur.

Toute idée hors périmètre va dans `V2.md`. Tu me la signales, tu ne la codes pas.

---

## 4. Environnement et choix techniques

**Première action :** vérifier la machine et me donner le résultat (OS, RAM, processeur, carte graphique éventuelle, Python, Git, Ollama installé ou non, espace disque, débit Internet approximatif).

**Résultat du diagnostic (2026-11-20) :**

| Élément | Valeur |
|---|---|
| OS | Windows 10 Professionnel 22H2 (10.0.19045), 64 bits |
| RAM | 15,9 Go (8,3 Go libres au moment du test) |
| Processeur | Intel Core i5-7600 @ 3,50 GHz, 4 cœurs / 4 threads (AVX2) |
| Carte graphique | Intel HD Graphics 630 (intégrée, non utilisée par Ollama → calcul sur CPU) |
| Disque C: | 348 Go libres |
| Python | Absent (seul le raccourci Microsoft Store existe) |
| Git | Absent |
| Ollama | Absent |
| winget | Présent (v1.12) |
| Débit Internet | ≈ 300 Ko/s (mesure sur 1 Mo) |

Python 3.12.10 et Git 2.56.0 ont été installés avec winget le 2026-11-20, ainsi que le **Microsoft Visual C++ Redistributable 2015-2022 (x64)**, absent de la machine et indispensable à PyMuPDF (`DLL load failed` sinon). À installer aussi sur toute machine de démonstration : `winget install --id Microsoft.VCRedist.2015+.x64 -e`.

**Contraintes pour la phase 6 (i5-7600, sans GPU) :**
- Réponses courtes : limiter la longueur générée (`num_predict` modéré) et le demander dans le prompt.
- Contexte limité : un `num_ctx` raisonnable, juste assez pour le prompt système, les k extraits et la question. Un grand contexte ralentit fortement le calcul sur CPU.
- `keep_alive` : garder le LLM et `bge-m3` chargés en mémoire entre deux questions, pour ne pas les recharger à chaque fois.
- Mesurer séparément le temps de la **première question** (chargement du modèle compris) et celui des **questions suivantes** (modèle déjà chargé).

| Élément | Choix | Raison |
|---|---|---|
| Langage | Python 3.11 ou 3.12, `.venv` | Standard, stable |
| OS cible | Windows (PowerShell) | Machine de Mourra ; chemins avec `pathlib` uniquement |
| LLM | `qwen3:4b-instruct-2507-q4_K_M` via Ollama, `think=False` | Licence Apache 2.0 (usage commercial OK), pas de mode réflexion, bon en français, environ 3,5 Go de RAM |
| Embeddings | `bge-m3` via Ollama | Licence MIT, multilingue (français + arabe pour la V2) |
| Base vectorielle | ChromaDB persistant, `anonymized_telemetry=False` | Local, simple |
| Lecture PDF | PyMuPDF | Rapide, texte page par page |
| Interface | Streamlit | Rapide à construire, démontrable |
| Génération des PDF de démo | reportlab (dépendance de dev uniquement) | Contrôle exact des pages |
| Qualité | pytest, ruff | Tests et lint |

**Interdits :**
- `qwen2.5:3b` : licence non commerciale.
- Le tag `qwen3:4b` seul : il pointe vers la variante « thinking », trop lente sur CPU.
- LangChain, LlamaIndex : on écrit la chaîne RAG nous-mêmes, pour la maîtriser.
- Toute API distante, toute clé d'API.

Si la RAM est inférieure à 8 Go, signale-le et propose une alternative **à licence commerciale**, avec ses compromis.

**Téléchargement d'Ollama :** la connexion de Mourra peut être lente (environ 100 Ko/s).
- Ne lance jamais un gros téléchargement en arrière-plan sans me le dire.
- Indique-moi la procédure hors ligne : télécharger `OllamaSetup.exe` et lancer `ollama pull` sur une connexion rapide, puis copier le dossier `%USERPROFILE%\.ollama\models` par clé USB.
- Tout le code et les tests doivent pouvoir avancer **sans Ollama**, grâce à des doublures (mocks).

---

## 5. Structure du projet

```
assistant-ia-securise/
├── CLAUDE.md                 ← ce fichier
├── README.md
├── V2.md
├── pyproject.toml            ← config ruff + pytest
├── requirements.txt          ← dépendances d'exécution, versions épinglées
├── requirements-dev.txt      ← pytest, ruff, reportlab
├── .env.example              ← modèles, seuil, mot de passe de démo (valeur d'exemple)
├── .gitignore                ← .venv, .env, data/index, __pycache__, logs
├── .streamlit/config.toml    ← server.address = "localhost", gatherUsageStats = false
├── config.py                 ← réglages typés, lus depuis .env (aucune valeur en dur ailleurs)
├── rag/                      ← logique métier, AUCUNE dépendance à Streamlit
│   ├── models.py             ← dataclasses : Page, Chunk, Source, Answer
│   ├── logging_setup.py
│   ├── ingestion.py          ← PDF → pages (retrait des en-têtes et pieds de page répétés)
│   ├── chunking.py           ← pages → chunks (jamais à cheval sur deux pages)
│   ├── llm.py                ← client Ollama : embeddings + génération, gestion d'erreurs
│   ├── vectorstore.py        ← ChromaDB, une collection par modèle d'embedding
│   ├── retrieval.py          ← recherche top-k + seuil
│   ├── prompts.py            ← prompt système et mise en forme des extraits
│   ├── pipeline.py           ← point d'entrée unique : ask(question) -> Answer
│   └── indexer.py            ← commande : python -m rag.indexer (reconstruit tout l'index)
├── app/
│   ├── main.py               ← streamlit run app/main.py
│   ├── auth.py               ← mot de passe de démo
│   ├── components.py         ← chat, cartes Sources, badge « 100 % local »
│   └── styles.py
├── scripts/
│   ├── check_env.py          ← vérifie Python, Ollama, modèles, RAM
│   ├── demo_corpus/          ← générateur du corpus (un module par document)
│   │   ├── facts.py          ← TOUS les chiffres partagés, source unique
│   │   ├── render.py         ← mise en page commune (charte, en-tête, pied, cartouche)
│   │   └── dNN_*.py
│   ├── generate_demo_pdfs.py
│   └── verify_demo_pdfs.py   ← contrôles automatiques du corpus
├── demo_docs/                ← les 25 PDF générés
├── eval/
│   ├── questions.csv
│   ├── evaluate.py
│   └── results/              ← un rapport par configuration testée
└── tests/
```

Tu peux adapter cette structure si tu as une bonne raison. Explique-la avant et mets cette section à jour.

**Adaptations (phase 1) :**
- `scripts/__init__.py` : `scripts` est un paquet, pour que ses modules importent `config` et soient testés. On les lance avec `-m` depuis la racine : `.venv\Scripts\python -m scripts.check_env`.
- `tests/conftest.py` : fixtures partagées (environnement isolé, réglages qui ignorent le vrai `.env`).
- Toutes les variables de `.env` sont préfixées par `ASSISTANT_` (ex. `ASSISTANT_TOP_K`). Ça évite le conflit avec la variable `OLLAMA_HOST` qu'Ollama utilise lui-même.
- `config.py` refuse une adresse d'Ollama qui ne pointe pas vers la machine locale.

**Adaptations (phase 2) :**
- `rag/errors.py` : erreurs métier, chacune avec un `user_message` en français. L'interface affiche ce message, jamais une trace Python.
- `rag/models.py` contient aussi `ScoredChunk` (morceau + similarité) et `DocumentSummary` (pour la liste des documents de l'interface).
- `rag/pipeline.py` expose `RagPipeline` (testable avec des doublures), `build_pipeline(settings)` et `ask(question)`.
- `tests/fakes.py` (faux embedding « sac de mots », faux LLM) et `tests/pdf_factory.py` (fabrique de PDF de test).

---

## 6. Exigences techniques détaillées

**Ingestion**
- PDF uniquement. Un autre format est refusé avec le message « Exportez votre document en PDF (Fichier › Enregistrer sous › PDF) ».
- Texte extrait page par page, en gardant le numéro de page.
- Titre lu dans les métadonnées du PDF, sinon déduit du nom de fichier.
- **Retrait des en-têtes et pieds de page répétés.** On examine les 3 premières et 3 dernières lignes de chaque page. Une ligne est « répétée » si elle apparaît dans cette zone sur au moins la moitié des pages, et sur au moins 2 pages. On ne retire les lignes que depuis le bord de la page, et on s'arrête à la première ligne non répétée. Les chiffres ne sont neutralisés que dans les lignes de numérotation (« Page 2 / 8 ») : « Article 3 » et « Article 4 » restent donc distincts.

**Découpage**
- Morceaux d'environ 800 à 1 000 caractères, avec environ 150 caractères de chevauchement. Ces valeurs sont réglables dans `config.py`.
- Un morceau ne déborde **jamais** sur deux pages.
- Chaque morceau a un identifiant stable et unique, et garde son document, son titre, sa page et le nombre de pages.

**Indexation**
- Le titre du document est placé **devant le texte** du morceau au moment du calcul de l'embedding, mais il n'est pas stocké dans le texte du morceau. Ça aide la recherche, par exemple pour retrouver une grille 2026 dont le passage ne contient ni « taux » ni « 2026 ».
- Une collection Chroma **par modèle d'embedding**, pour ne jamais mélanger des vecteurs incompatibles.
- `python -m rag.indexer` reconstruit tout l'index et affiche une barre de progression et la durée.

**Recherche et génération**
- Top-k réglable (5 par défaut). Seuil de similarité réglable : en dessous, on refuse **sans appeler le LLM**.
- Les extraits sont envoyés au LLM sous la forme `[Titre, page N]`.
- Le prompt système exige de :
  - répondre seulement à partir des extraits ;
  - citer la source après chaque information ;
  - utiliser la version la plus récente quand deux versions existent, et le dire ;
  - refuser avec la phrase exacte ;
  - répondre en français, de façon courte et précise.
- Température basse (environ 0,1), `think=False`. Si Ollama refuse `think`, on réessaie sans ce paramètre et on journalise un avertissement.
- Les sources affichées viennent des métadonnées, **pas du texte généré par le LLM**, pour éviter les citations inventées.

**Robustesse**
- Messages clairs pour l'utilisateur, jamais une trace Python brute, dans ces cas : Ollama arrêté, modèle absent, index vide, PDF illisible, mot de passe faux.

**Sécurité et confidentialité**
- Streamlit écoute sur `localhost` seulement. Désactive aussi tout ce qui contacte Internet au démarrage, y compris la détection de l'adresse IP publique.
- Télémétrie désactivée pour Chroma et Streamlit.
- Vérifie qu'**aucune requête ne part vers Internet** pendant une session complète, et documente la méthode de vérification.
- Journal (logging) local : horodatage, durée, nombre de sources, documents cités. Jamais le mot de passe.

**Qualité du code**
- Typage complet, docstrings en français, fonctions courtes à une seule responsabilité.
- Aucun `print` dans `rag/`.
- Aucun `TODO`, aucun code mort ni commenté.
- `ruff check` et `ruff format` sans erreur.
- Tests `pytest` qui tournent **sans Ollama** : ingestion, retrait des en-têtes, découpage, pages, prompt, seuil, pipeline avec doublures.

---

## 7. Le corpus de démonstration

**Institution fictive :** **Kouri Épargne & Crédit S.A.**, établissement de microfinance de 2e catégorie, siège à N'Djamena. Le kouri est la race bovine du lac Tchad, et au Sahel le bétail est l'épargne traditionnelle. L'institution a 6 agences : 4 à N'Djamena (dont celle du Grand Marché), 1 à Moundou et 1 à Abéché.

**Charte :** vert profond et or, distincte de celle de ZakiCortex.

Chaque PDF porte :
- en en-tête : le nom de l'institution et une référence (ex. CR-PRO-01, TAR-2026) ;
- en page 1 : un cartouche avec version, date et approbation ;
- en pied de page : « Document fictif – démonstration ZakiCortex » et « Page i / n » ;
- le titre dans les métadonnées du PDF.

**Règles de rédaction :**
- Du vrai contenu professionnel : procédures, tableaux, exemples chiffrés, cas particuliers, FAQ. Jamais de texte de remplissage.
- Pages remplies à **environ 80 %**. Le générateur mesure le remplissage et signale toute page sous 70 %.
- Chaque réponse du jeu d'évaluation apparaît **une seule fois** dans tout le corpus, **à la page annoncée**. La seule exception est le piège 2025/2026, qui est voulu.
- Tous les chiffres partagés viennent de `facts.py`. Entre procédures, on **renvoie** à l'autre document (« voir CR-PRO-02 ») au lieu de recopier un chiffre qui sert de réponse ailleurs.
- Les grilles 2025 et 2026 ont **exactement les mêmes rubriques**. Seuls les chiffres changent.
- Tout calcul présenté (mensualité, coût total) doit être juste et expliqué ligne par ligne.

**Les 25 documents** (environ 141 pages) :

| # | Document (pages) | Question 1 → réponse (page) | Question 2 → réponse (page) |
|---|---|---|---|
| 1 | Règlement intérieur (8) | Horaires du personnel le vendredi ? → 7 h 00–12 h 30 (p. 2) | Sanctions disciplinaires ? → avertissement, mise à pied de 1 à 3 jours, licenciement (p. 7) |
| 2 | Procédure de demande de congés (5) | Délai de dépôt pour un congé de plus de 5 jours ? → 15 jours calendaires (p. 3) | Congé pour mariage du salarié ? → 4 jours ouvrables (p. 2) |
| 3 | Recrutement et intégration (6) | Période d'essai d'un agent de crédit ? → 3 mois, renouvelable une fois (p. 4) | Quand reçoit-on ses identifiants du logiciel ? → le premier jour, après signature de la charte de confidentialité (p. 5) |
| 4 | Politique de rémunération et avantages (6) | Date de paiement des salaires ? → le 25 de chaque mois (p. 2) | Taux d'un prêt au personnel ? → 6 % par an, dans la limite de 6 mois de salaire (p. 4) |
| 5 | Frais de mission (5) | Indemnité pour une mission hors de N'Djamena ? → 15 000 FCFA par jour, hébergement plafonné à 20 000 FCFA par nuit (p. 3) | Délai pour remettre les justificatifs ? → 7 jours ouvrables (p. 4) |
| 6 | Charte informatique et sécurité des données (7) | Fréquence de changement du mot de passe ? → tous les 90 jours, 12 caractères minimum (p. 3) | Perte d'une tablette de collecte ? → prévenir l'informatique sous 2 h pour un blocage à distance (p. 6) |
| 7 | Plan de formation 2026 (5) | Heures de formation par salarié ? → 30 h (p. 2) | Formation anti-blanchiment obligatoire ? → en mars 2026 (p. 4) |
| 8 | Consignes incendie et évacuation (4) | Point de rassemblement du siège ? → le parking devant le siège (p. 2) | Qui dirige l'évacuation en agence ? → le chef d'agence (p. 3) |
| 9 | Note de service : horaires du Ramadan (3) | Horaires des agences pendant le Ramadan ? → 7 h 30–13 h 00 du lundi au jeudi, 7 h 30–11 h 30 le vendredi (p. 1) | L'agence du Grand Marché ouvre-t-elle le samedi ? → oui, de 8 h à 11 h (p. 2) |
| 10 | Politique et procédure d'octroi de crédit (10) | Montant maximal d'un premier crédit ? → 500 000 FCFA (p. 4) | Mensualité maximale ? → 40 % du revenu net mensuel (p. 6) |
| 11 | Comité de crédit et plafonds d'autorisation (5) | Plafond qu'un chef d'agence peut approuver seul ? → 1 000 000 FCFA (p. 2) | Qui approuve au-delà de 10 000 000 FCFA ? → le Conseil d'administration (p. 4) |
| 12 | Crédit solidaire aux groupements (5) | Taille d'un groupement ? → 5 à 15 membres (p. 2) | Un membre ne rembourse pas ? → les autres paient à sa place (caution solidaire), et le groupe ne peut plus emprunter (p. 3) |
| 13 | Grille des taux et frais 2025 (4) | Frais de dossier en 2025 ? → 2 % du montant (p. 2) | Tenue de compte en 2025 ? → 1 000 FCFA par mois (p. 3) |
| 14 | Grille des taux et frais 2026 (4) | 🪤 Taux du crédit pour activité génératrice de revenus (AGR) ? → 21 % par an selon la grille 2026 ; signaler que 2025 indiquait 24 % (p. 2) | Tenue de compte ? → 1 500 FCFA par mois (2025 : 1 000) (p. 3) |
| 15 | Recouvrement des impayés (6) | Passage au contentieux ? → après 90 jours de retard (p. 4) | Première visite de l'agent ? → au 7e jour de retard (p. 2) |
| 16 | Procédure d'ouverture de compte (5) | Pièces à fournir ? → pièce d'identité valide, 2 photos, justificatif de domicile ou attestation du chef de quartier (p. 2) | Compte d'un mineur ? → ouvert par le parent ou le tuteur, seul signataire jusqu'aux 18 ans (p. 4) |
| 17 | Connaissance client (KYC) et lutte anti-blanchiment (8) | Seuil de déclaration interne d'une opération en espèces ? → 5 000 000 FCFA (p. 4) | Mise à jour du dossier d'un client à risque élevé ? → chaque année (p. 6) |
| 18 | Catalogue des produits d'épargne (5) | Taux d'un dépôt à terme de 12 mois ? → 4,5 % par an (p. 3) | Retrait avant l'échéance ? → possible, mais les intérêts sont réduits de moitié (p. 4) |
| 19 | Procédures de caisse en agence (6) | Plafond d'encaisse d'un guichet ? → 5 000 000 FCFA, le surplus va au coffre (p. 2) | Écart de caisse en fin de journée ? → recomptage devant le chef d'agence et procès-verbal le jour même (p. 4) |
| 20 | Sécurité des agences (5) | Combien de personnes pour ouvrir le coffre ? → 2 : chef d'agence et caissier principal (p. 2) | Conduite en cas de braquage ? → ne pas résister, déclencher l'alarme silencieuse sans prendre de risque (p. 4) |
| 21 | Traitement des réclamations clients (4) | Délai d'accusé de réception ? → 48 h ouvrées (p. 2) | Délai de réponse définitive ? → 15 jours ouvrables, puis transmission au Directeur général (p. 3) |
| 22 | Organigramme et rôles des services (4) | Nombre d'agences ? → 6 : 4 à N'Djamena, 1 à Moundou, 1 à Abéché (p. 1) | Rattachement du responsable conformité ? → directement au Directeur général (p. 3) |
| 23 | Rapport annuel 2025 (10) | Clients actifs fin 2025 ? → 18 400 (p. 2) | Portefeuille à risque à 30 jours (PAR 30) fin 2025 ? → 6,8 % (p. 6) |
| 24 | Plan de continuité d'activité (6) | Autonomie du groupe électrogène ? → 8 h (p. 3) | Logiciel en panne : combien un client peut-il retirer ? → 100 000 FCFA par jour, sur bordereau papier (p. 4) |
| 25 | Protection des données personnelles (5) | Conservation des données d'un ancien client ? → 10 ans après la clôture du compte (p. 3) | Référent données personnelles ? → le responsable de la conformité (p. 2) |

**Contrôles de `verify_demo_pdfs.py` :**
- le titre est dans les métadonnées ;
- le nombre de pages est conforme ;
- le pied de page et la numérotation sont présents sur chaque page ;
- l'en-tête et le pied de page sont absents du texte indexé ;
- chaque réponse est à sa page et unique dans le corpus ;
- les grilles 2025 et 2026 ont des rubriques identiques une fois les chiffres masqués ;
- le remplissage est d'au moins 70 % par page.

Vérifie aussi que le vérificateur **détecte vraiment** les erreurs : injecte volontairement une réponse à la mauvaise page, un doublon et un pied de page indexé, et constate l'échec attendu.

---

## 8. Le jeu d'évaluation (30 questions)

- **20 questions directes** : la question 1 des documents 1, 2, 4 à 11, 13 à 17, 19, 20, 22, 23 et 25. Elles incluent le piège 2025/2026 (n° 14).
- **5 questions reformulées** comme un employé, sans reprendre les mots du document :
  - R1 « Je me marie le mois prochain, j'ai droit à combien de jours ? » → n° 2, p. 2
  - R2 « Je viens d'être pris comme agent de crédit, je suis confirmé au bout de combien de temps ? » → n° 3, p. 4
  - R3 « Les femmes de ma tontine veulent un prêt ensemble, il faut être combien ? » → n° 12, p. 2
  - R4 « Si je bloque mon argent un an chez vous, ça rapporte combien ? » → n° 18, p. 3
  - R5 « Un client attend une réponse à sa plainte depuis trois semaines, à qui je transmets ? » → n° 21, p. 3
- **5 questions sans réponse** (les 3 premières sont des pièges, car leur sujet est voisin d'un document existant) :
  - N1 Montant de la prime de fin d'année ? (le n° 4 parle d'autres avantages)
  - N2 Taux d'un crédit immobilier sur 15 ans ? (les grilles parlent de taux, pas d'immobilier)
  - N3 Numéro de compte bancaire de l'institution ? (les n° 16 et 19 parlent de comptes)
  - N4 L'institution autorise-t-elle le télétravail ?
  - N5 Date du prochain séminaire du personnel ?
- Les questions 2 de chaque document servent pour la démo et en réserve.

**Scores mesurés par `evaluate.py` :**
- bon document et bonne page dans le top-k ;
- réponse exacte (chiffre ou élément clé attendu présent) ;
- page citée correcte. Pour le piège des versions, on accepte « 2026 seule » ou « 2026 + 2025 » ; « 2025 seule » est une erreur ;
- refus correct sur les questions sans réponse ;
- refus à tort sur les questions qui ont une réponse ;
- temps de réponse moyen et maximal.

Teste plusieurs configurations (taille des morceaux, top-k, seuil), en changeant **un seul réglage à la fois**. Écris un rapport par configuration dans `eval/results/`, puis garde la meilleure dans `config.py`. Le tableau comparatif ira dans le README.

---

## 9. Méthode de travail

1. **Travaille par phases** (section 10). À l'intérieur d'une phase, tu avances seul. **À la fin de chaque phase, tu t'arrêtes** et tu me donnes un compte rendu :
   - ce qui a été fait ;
   - les fichiers créés ou modifiés ;
   - les commandes PowerShell exactes pour vérifier ;
   - le résultat attendu ;
   - les décisions à valider.
   Tu attends ensuite mon « OK ».
2. **Avant chaque phase**, explique en 5 à 10 lignes simples ce que tu vas faire et pourquoi.
3. **Commit Git après chaque sous-étape réussie** (tests verts), avec des messages clairs du type `feat:`, `fix:`, `test:`, `docs:`. Si la connexion ou la machine coupe, on perd au maximum une sous-étape.
4. **En cas de reprise après coupure :** lis ce fichier, fais `git status` et `git log --oneline -15`, repère les fichiers incomplets, répare-les, dis-moi en 5 lignes où on en est, puis continue.
5. **Ne prétends jamais** qu'un test passe sans l'avoir exécuté.
6. **Ne devine pas.** Si une information manque, demande-la.
7. **Quand je signale un problème :** analyse la cause, explique-la en 2 phrases, puis corrige. Si je te demande le code, donne-moi le **fichier complet**, jamais un fragment.
8. **Mets à jour la section 11** (journal d'avancement) de ce fichier à la fin de chaque phase.
9. Tout est en français : dialogue, docstrings, commentaires, documentation.

---

## 10. Les phases

| Phase | Contenu | Besoin d'Ollama | Fini quand… |
|---|---|---|---|
| **0. Diagnostic** | Vérifier la machine (section 4), `git init`, créer `V2.md`, m'indiquer la procédure de téléchargement d'Ollama et des modèles | Non | Je connais l'état de la machine et ce que je dois télécharger |
| **1. Socle** | Structure, `config.py`, logging, `.env.example`, `.gitignore`, `.streamlit/config.toml`, `pyproject.toml`, dépendances épinglées, `scripts/check_env.py` | Non | `ruff` et `pytest` passent (même s'il y a peu de tests) |
| **2. Moteur RAG** | `rag/` complet + tests avec doublures | Non | Tous les tests passent sans Ollama |
| **3. Corpus d'essai** | `render.py`, `facts.py`, générateur et vérificateur ; **2 PDF seulement** : n° 10 et n° 14 (et n° 13 en dossier temporaire pour le contrôle des rubriques) | Non | Le vérificateur est vert, et **j'ouvre et je valide les 2 PDF** |
| **4. Corpus complet** | Les 23 autres en 4 lots (lot 1 : 1-9 ; lot 2 : 11, 12, 13, 15 ; lot 3 : 16-21 ; lot 4 : 22-25). Après chaque lot : vérificateur sur tout le corpus, tests, commit | Non | 25 PDF, vérificateur vert |
| **5. Interface** | Streamlit : connexion, chat, cartes Sources (titre, page, extrait, ouverture du PDF à la page), liste des documents (pages, chunks), questions d'exemple, badge « 🔒 100 % local », charte ZakiCortex (violet sur fond sombre) | Non (doublure) | Un inconnu l'utilise sans aide |
| **6. Installation des modèles** | Installer Ollama et les modèles (depuis les fichiers copiés si besoin), indexer le corpus, premiers essais réels | Oui | Les 5 questions de démo donnent une réponse correcte et citée |
| **7. Évaluation** | `questions.csv`, `evaluate.py`, comparaison de configurations, calibrage du seuil | Oui | Tableau de scores et meilleure configuration retenue |
| **8. Preuve hors ligne** | Démo complète en mode avion ; vérification qu'aucune requête ne part vers Internet ; mesure des temps de réponse et du matériel | Oui | Tout marche sans réseau, preuves notées |
| **9. Livraison** | README pro, `docs/` (captures), scénario de la vidéo, fiche portfolio FR + AR, publication GitHub | — | Les 4 livrables sont prêts (section 12) |

---

## 11. Journal d'avancement

> À mettre à jour à la fin de chaque phase (date, phase, commit, résultat).

| Date | Phase | Commit | Résultat |
|---|---|---|---|
| 2026-11-20 | 0. Diagnostic | premier commit (`docs:`) | Machine vérifiée (16 Go RAM, i5-7600, CPU seul, ≈ 300 Ko/s). Python 3.12.10 et Git 2.56.0 installés avec winget. Dépôt Git initialisé (branche `main`), `V2.md` créé. Ollama et les modèles restent à installer (phase 6, procédure hors ligne par clé USB conseillée) |
| 2026-11-20 | 1. Socle | voir `git log` (`chore:`, `feat:`, `docs:`) | `.venv` (Python 3.12.10), dépendances épinglées (chromadb 1.5.9, streamlit 1.67.0, pymupdf 2.1, ollama 0.6.3…), `config.py` validé, journal avec masquage du mot de passe, `.streamlit/config.toml` (localhost, sans télémétrie, `showErrorDetails = "none"`), `scripts/check_env.py`. `ruff` OK, **37 tests verts**. `check_env` : tout OK sauf `.env` absent et Ollama absent (attendu) |
| 2026-11-20 | 2. Moteur RAG | `16914e2` → `8798595` (un commit par module) | `rag/` complet : errors, models, ingestion (retrait en-têtes/pieds), chunking (jamais sur 2 pages), llm (client Ollama strict, repli `think`), vectorstore (Chroma cosinus, sans embedding interne), retrieval (top-k + seuil), prompts, pipeline (sources depuis les métadonnées, citations vérifiées), indexer. `check_env` bloque le mot de passe d'exemple ou < 12 caractères. VC++ Redistributable installé. `ruff` OK, **142 tests verts sans Ollama**. `python -m rag.indexer` sans Ollama : message clair, code 1 |

---

## 12. Livrables finaux

1. **Le dépôt GitHub** avec un README professionnel :
   - le problème et la solution ;
   - un schéma de l'architecture ;
   - des captures d'écran ;
   - l'installation en 5 commandes (y compris la procédure hors ligne pour Ollama) ;
   - les résultats de l'évaluation ;
   - la preuve « 100 % local » ;
   - les limites et la V2 ;
   - la licence des modèles.
2. **La démo en direct sur le PC.** Pas de démo en ligne : ça contredirait l'argument « vos documents ne quittent jamais vos bureaux ».
3. **Le scénario de la vidéo d'une minute**, plan par plan :
   - 5 s : le problème ;
   - 10 s : on coupe le Wi-Fi à l'écran ;
   - 30 s : 3 questions avec les sources, dont le piège 2025/2026, et un PDF ouvert à la bonne page ;
   - 10 s : une question sans réponse, refusée ;
   - 5 s : le logo et le contact ZakiCortex.
4. **La fiche « Réalisations » pour le site**, en français et en arabe : 4 phrases centrées sur le bénéfice client, plus la légende de la capture.

---

## 13. Ce que tu ne fais jamais

- Coder hors périmètre.
- Appeler un service distant, ou télécharger plusieurs Go sans me prévenir.
- Écrire un mot de passe ou un secret dans le code, le README ou un commit.
- Utiliser un vrai nom de banque ou de personne réelle dans le corpus.
- Passer à la phase suivante sans mon OK.
