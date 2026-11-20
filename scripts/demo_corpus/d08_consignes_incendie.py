"""Document n° 8 — Consignes incendie et évacuation (SEC-CON-01, 4 pages).

Réponses attendues : point de rassemblement du siège (page 2) et responsable de
l'évacuation en agence (page 3).
"""

from scripts.demo_corpus.facts import DOCUMENTS
from scripts.demo_corpus.render import Page, bullets, callout, h1, h2, p, table, title_block

SPEC = DOCUMENTS[8]


def build_pages() -> list[Page]:
    """Construit les 4 pages du document."""
    return [_p1(), _p2(), _p3(), _p4()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Ces consignes indiquent comment prévenir un incendie, donner l'alerte et "
            "évacuer les locaux en sécurité, au siège comme en agence. Elles sont affichées "
            "près de chaque sortie et rappelées lors de chaque exercice d'évacuation. La vie "
            "des personnes passe avant les fonds et les documents."
        ),
        h1("2. Prévention au quotidien"),
        *bullets(
            [
                "Ne jamais surcharger une prise ni utiliser de multiprise en cascade.",
                "Éteindre les climatiseurs, les ordinateurs et les éclairages en fin de "
                "journée, sauf le matériel qui doit rester en marche.",
                "Ne stocker aucun carburant, gaz ou produit inflammable dans les locaux.",
                "Laisser libres les issues de secours, les couloirs et l'accès aux extincteurs.",
                "Signaler tout câble abîmé, toute odeur de brûlé ou tout appareil qui chauffe.",
            ]
        ),
        h1("3. Numéros utiles"),
        table(
            [
                ["Service", "Numéro", "Quand appeler"],
                [
                    "Sapeurs-pompiers",
                    "18",
                    "Dès qu'un feu ne peut pas être maîtrisé avec un extincteur",
                ],
                ["Police", "17", "En cas de blessé grave ou de danger pour l'ordre public"],
                [
                    "Responsable sécurité de l'institution",
                    "Affiché à l'accueil",
                    "Pour tout incident, même maîtrisé",
                ],
                [
                    "Groupe électrogène et maintenance",
                    "Affiché au local technique",
                    "Panne ou odeur suspecte au local technique",
                ],
            ],
            (0.35, 0.2, 0.45),
        ),
        callout(
            "À retenir",
            [
                "Donner l'alerte, évacuer, ne jamais revenir en arrière : ces trois gestes "
                "sauvent des vies.",
            ],
        ),
    ]


def _p2() -> Page:
    return [
        h1("4. Conduite à tenir au siège"),
        table(
            [
                ["Étape", "Qui", "Action"],
                [
                    "1. Alerter",
                    "La personne qui découvre le feu",
                    "Crier « Au feu », déclencher l'alarme, prévenir l'accueil",
                ],
                [
                    "2. Attaquer le feu",
                    "Personne formée, si le feu est petit",
                    "Utiliser l'extincteur adapté, sans se mettre en danger",
                ],
                [
                    "3. Appeler les secours",
                    "Accueil",
                    "Composer le 18, donner l'adresse et la nature du feu",
                ],
                [
                    "4. Évacuer",
                    "Tout le personnel et les visiteurs",
                    "Sortir calmement par l'issue la plus proche, sans prendre l'ascenseur",
                ],
                ["5. Se rassembler", "Tout le monde", "Rejoindre le point de rassemblement"],
                [
                    "6. Compter",
                    "Serre-files",
                    "Vérifier la présence de chacun et le signaler au chargé d'évacuation",
                ],
            ],
            (0.2, 0.3, 0.5),
        ),
        h2("Point de rassemblement"),
        p(
            "Le point de rassemblement du siège est le parking devant le siège, côté rue, à "
            "distance du bâtiment. Il est signalé par un panneau vert. Personne ne quitte le "
            "point de rassemblement avant l'autorisation du chargé d'évacuation."
        ),
        h2("Rôles désignés au siège"),
        table(
            [
                ["Rôle", "Mission"],
                ["Chargé d'évacuation", "Coordonne l'évacuation et accueille les secours"],
                ["Guide-files (un par étage)", "Ouvrent la marche et dirigent vers les sorties"],
                [
                    "Serre-files (un par étage)",
                    "Ferment la marche, vérifient bureaux et toilettes, ferment les portes",
                ],
            ],
            (0.3, 0.7),
        ),
        p(
            "Les noms des personnes désignées sont affichés à chaque étage et mis à jour à "
            "chaque mouvement de personnel."
        ),
        h2("Si la fumée bloque la sortie"),
        p(
            "Si la fumée envahit l'escalier, ne pas le traverser : rester dans un bureau, "
            "fermer la porte, calfeutrer le bas avec un vêtement mouillé, se signaler à la "
            "fenêtre et attendre les secours. Dans la fumée, se déplacer baissé, près du sol."
        ),
        h2("Visiteurs et personnes vulnérables"),
        p(
            "L'accueil tient la liste des visiteurs présents et la remet au chargé "
            "d'évacuation. Une personne à mobilité réduite est accompagnée par deux "
            "collègues désignés à l'avance ; les femmes enceintes et les personnes âgées sont "
            "guidées en priorité, sans précipitation dans les escaliers."
        ),
    ]


def _p3() -> Page:
    return [
        h1("5. Conduite à tenir en agence"),
        p(
            "En agence, le chef d'agence dirige l'évacuation. En son absence, ce rôle revient "
            "à son adjoint désigné, puis au caissier principal. La personne responsable "
            "s'assure que tous les clients et le personnel sont sortis, puis rend compte aux "
            "secours à leur arrivée."
        ),
        h2("Ordre des actions en agence"),
        *bullets(
            [
                "Faire sortir d'abord les clients, en les guidant vers la sortie la plus proche.",
                "Les caissiers ferment leur tiroir-caisse à clé s'ils peuvent le faire en "
                "quelques secondes, sinon ils sortent sans délai.",
                "Le coffre n'est jamais ouvert pendant une alerte.",
                "Couper l'électricité au tableau général si c'est possible sans risque.",
                "Rejoindre le point de rassemblement indiqué sur le plan affiché à l'entrée "
                "de l'agence.",
            ]
        ),
        h2("Fonds et documents"),
        p(
            "Les fonds laissés dans les tiroirs et le coffre ne justifient jamais de prendre "
            "un risque : ils sont assurés. Après l'incident, le chef d'agence fait recompter "
            "les caisses en présence d'un témoin dès que l'accès est autorisé, et consigne le "
            "résultat dans un procès-verbal transmis à la Direction des opérations."
        ),
        h2("Information des clients"),
        p(
            "Une fois les secours sur place, le chef d'agence informe les clients présents "
            "que l'agence est fermée et leur indique l'agence la plus proche. Une affiche est "
            "posée sur la porte dès que possible."
        ),
        h2("Agences situées dans un marché"),
        p(
            "Dans une agence entourée d'étals et de marchandises, le feu peut se propager "
            "très vite. Le personnel s'éloigne davantage du bâtiment et guide les clients "
            "vers une voie dégagée, à l'écart des stocks inflammables. Les voisins "
            "commerçants sont prévenus pendant l'évacuation."
        ),
        h2("Après l'évacuation"),
        p(
            "L'accès aux locaux reste fermé jusqu'à l'autorisation des sapeurs-pompiers. "
            "Le chef d'agence informe la Direction des opérations et le responsable "
            "sécurité, puis organise la surveillance des locaux. La reprise de l'activité "
            "suit le plan de continuité d'activité (voir PCA-01)."
        ),
        callout(
            "Interdit pendant une évacuation",
            [
                "Revenir chercher un objet personnel, des fonds ou des documents.",
                "Utiliser l'eau sur un feu d'origine électrique.",
                "Ouvrir une porte chaude : vérifier d'abord avec le dos de la main.",
            ],
        ),
    ]


def _p4() -> Page:
    return [
        h1("6. Choisir le bon extincteur"),
        table(
            [
                ["Type d'extincteur", "Feux concernés", "À ne pas utiliser sur"],
                ["Eau pulvérisée", "Papier, bois, tissus", "Appareils électriques"],
                ["Poudre", "Feux de liquides, de gaz, d'appareils électriques", "—"],
                [
                    "Dioxyde de carbone (CO2)",
                    "Ordinateurs, tableaux électriques",
                    "Feux de papier en profondeur",
                ],
            ],
            (0.3, 0.42, 0.28),
        ),
        p(
            "Utilisation : tirer la goupille, viser la base des flammes, presser la poignée "
            "et balayer. Se placer dos à la sortie, à deux ou trois mètres du feu. Un "
            "extincteur utilisé, même partiellement, est signalé pour être rechargé."
        ),
        h1("7. Exercices et vérifications"),
        table(
            [
                ["Action", "Fréquence", "Responsable"],
                [
                    "Exercice d'évacuation",
                    "Deux fois par an dans chaque site",
                    "Responsable sécurité",
                ],
                ["Vérification des extincteurs", "Une fois par an", "Prestataire agréé"],
                [
                    "Contrôle visuel des issues et des extincteurs",
                    "Chaque mois",
                    "Chef d'agence ou chargé d'évacuation",
                ],
                ["Formation du personnel", "Chaque année (voir RH-PLF-2026)", "DRH"],
            ],
            (0.4, 0.3, 0.3),
        ),
        h2("Registre de sécurité"),
        p(
            "Chaque site tient un registre de sécurité où sont notés les exercices, les "
            "vérifications d'extincteurs, les incidents et les travaux électriques. Le "
            "registre est présenté à tout contrôle et revu par le responsable sécurité lors "
            "de ses visites."
        ),
        h2("Leçons d'un exercice"),
        p(
            "Après chaque exercice, le chargé d'évacuation note la durée d'évacuation et les "
            "difficultés rencontrées (porte bloquée, alarme peu audible, personne restée à "
            "l'intérieur). Les corrections sont faites avant l'exercice suivant."
        ),
        h2("Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Mars 2022", "Création des consignes"],
                [
                    "1.1",
                    SPEC.approval_date,
                    "Rôles désignés au siège et ordre des actions en agence",
                ],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
