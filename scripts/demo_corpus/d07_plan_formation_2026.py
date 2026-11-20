"""Document n° 7 — Plan de formation 2026 (RH-PLF-2026, 5 pages).

Réponses attendues : heures de formation par salarié (page 2) et date de la
formation anti-blanchiment obligatoire (page 4).
"""

from scripts.demo_corpus.facts import DOCUMENTS, fcfa
from scripts.demo_corpus.render import (
    Page,
    bullets,
    calculation,
    callout,
    faq,
    h1,
    h2,
    p,
    table,
    title_block,
)

SPEC = DOCUMENTS[7]
BUDGET = 18_000_000
AXES = (
    ("Conformité et formations obligatoires", 30),
    ("Métiers du crédit et du recouvrement", 35),
    ("Service à la clientèle et caisse", 15),
    ("Management et encadrement", 12),
    ("Informatique et outils", 8),
)


def build_pages() -> list[Page]:
    """Construit les 5 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Introduction"),
        p(
            "Le plan de formation 2026 traduit en actions concrètes les priorités de "
            "l'institution pour l'année : un portefeuille de crédit plus sain, un service à "
            "la clientèle plus rapide, et une conformité irréprochable face aux exigences "
            "croissantes de la réglementation. Il a été établi à partir des entretiens "
            "annuels d'évaluation et des constats de l'audit interne."
        ),
        h2("Méthode d'élaboration"),
        p(
            "Chaque responsable a recensé les besoins de son équipe lors des entretiens "
            "annuels. La Direction des ressources humaines les a regroupés, chiffrés et "
            "classés par priorité, puis la Direction générale a arbitré en fonction du budget "
            "et des obligations réglementaires."
        ),
        h1("2. Enseignements de l'année écoulée"),
        *bullets(
            [
                "Les agents de crédit recrutés en cours d'année ont demandé davantage de "
                "pratique sur l'analyse de la capacité de remboursement.",
                "Les erreurs de caisse ont diminué dans les agences où le tutorat a été "
                "organisé ; le dispositif est étendu à toutes les agences.",
                "Les sessions organisées le vendredi après-midi ont été peu suivies ; elles "
                "sont supprimées en 2026.",
            ]
        ),
        h1("3. Objectifs 2026"),
        table(
            [
                ["Objectif", "Indicateur de réussite"],
                [
                    "Former tout le personnel aux obligations de conformité",
                    "100 % de présence aux formations obligatoires",
                ],
                ["Renforcer l'analyse du crédit", "Baisse des dossiers renvoyés pour incomplétude"],
                ["Améliorer l'accueil et la caisse", "Baisse des réclamations liées à l'accueil"],
                ["Préparer les futurs chefs d'agence", "Quatre salariés formés au management"],
            ],
            (0.5, 0.5),
        ),
    ]


def _p2() -> Page:
    lines = [
        (f"{label} : {share} % du budget", fcfa(BUDGET * share // 100)) for label, share in AXES
    ]
    lines.append(("Total = somme des lignes 1 à 5", fcfa(BUDGET)))
    return [
        h1("4. Droits et principes"),
        p(
            "Chaque salarié bénéficie d'au moins 30 heures de formation au cours de l'année. "
            "Ce volume comprend les formations obligatoires de la section 6 et les "
            "formations choisies avec le responsable lors de l'entretien annuel. Les heures "
            "de formation sont du temps de travail et sont rémunérées comme tel."
        ),
        *bullets(
            [
                "Les formations ont lieu pendant les heures de travail, en dehors des fins de "
                "mois et des périodes de forte affluence.",
                "Les sessions sont organisées au siège ou, pour les agences de Moundou et "
                "d'Abéché, sur place ou à distance.",
                "Les supports de formation sont disponibles hors connexion, pour les "
                "agences où le réseau est instable.",
            ]
        ),
        h2("Formateurs internes"),
        p(
            "Une partie des sessions est animée par des salariés expérimentés, formés à la "
            "pédagogie au début de l'année. Leur temps d'animation est du temps de travail, "
            "et leur contribution est reconnue lors de leur entretien annuel. Ce choix "
            "réduit les coûts et ancre les formations dans les pratiques réelles des agences."
        ),
        h2("Agences éloignées"),
        p(
            "Pour les agences de Moundou et d'Abéché, les sessions du siège sont reprises sur "
            "place par un formateur interne qui se déplace, ou suivies à distance lorsque la "
            "connexion le permet. Les frais de déplacement correspondants sont imputés sur "
            "le budget de formation."
        ),
        h1("5. Budget"),
        p(
            f"Le budget de formation 2026 est fixé à {fcfa(BUDGET)}. Sa répartition par axe "
            "est la suivante :"
        ),
        *calculation(lines, "Axe de formation et part du budget"),
        callout(
            "Suivi du budget",
            [
                "La Direction des ressources humaines présente l'état d'exécution du budget "
                "chaque trimestre à la Direction générale. Un axe peut céder une partie de "
                "son budget à un autre sur décision écrite.",
            ],
        ),
    ]


def _p3() -> Page:
    return [
        h1("6. Catalogue des formations"),
        table(
            [
                ["Formation", "Public", "Durée", "Période"],
                [
                    "Analyse de la capacité de remboursement",
                    "Agents de crédit",
                    "12 h",
                    "1er trimestre",
                ],
                [
                    "Recouvrement amiable et négociation",
                    "Agents de crédit, chefs d'agence",
                    "8 h",
                    "2e trimestre",
                ],
                [
                    "Accueil et gestion des clients mécontents",
                    "Caissiers, accueil",
                    "6 h",
                    "2e trimestre",
                ],
                [
                    "Détection des faux billets et sécurité de la caisse",
                    "Caissiers",
                    "4 h",
                    "3e trimestre",
                ],
                ["Management d'équipe", "Chefs d'agence et futurs chefs", "16 h", "3e trimestre"],
                [
                    "Tableur et rapports de gestion",
                    "Personnel administratif",
                    "8 h",
                    "4e trimestre",
                ],
                [
                    "Crédit agricole : saisons et risques",
                    "Agents des agences de Moundou et d'Abéché",
                    "6 h",
                    "2e trimestre",
                ],
                [
                    "Crédit solidaire : animer un groupement",
                    "Agents de crédit",
                    "6 h",
                    "3e trimestre",
                ],
                [
                    "Contrôle interne des agences",
                    "Chefs d'agence, contrôleurs",
                    "8 h",
                    "4e trimestre",
                ],
            ],
            (0.4, 0.3, 0.1, 0.2),
        ),
        h2("Formats proposés"),
        table(
            [
                ["Format", "Description"],
                ["Présentiel", "Session en groupe au siège, avec cas pratiques"],
                ["Tutorat", "Accompagnement sur le poste par un collègue expérimenté"],
                ["Module hors ligne", "Support installé sur les postes, avec questionnaire final"],
            ],
            (0.25, 0.75),
        ),
        p(
            "Chaque formation se conclut par une évaluation des acquis. Les heures ne sont "
            "comptées dans le droit annuel qu'après la remise de l'évaluation signée par le "
            "formateur."
        ),
        h2("Organismes extérieurs"),
        p(
            "Lorsqu'une compétence n'existe pas en interne, la formation est confiée à un "
            "organisme extérieur choisi après comparaison d'au moins deux offres. Le contrat "
            "précise le programme, le nombre d'heures, les supports remis et les modalités "
            "d'évaluation. Les données des clients ne sont jamais utilisées comme exemples "
            "par un formateur extérieur."
        ),
        h2("Formations diplômantes"),
        p(
            "Un salarié confirmé peut demander le financement partiel d'une formation "
            "diplômante en lien avec son poste. La demande est examinée une fois par an ; "
            "le salarié s'engage alors à rester dans l'institution pendant une durée fixée "
            "dans une convention, à défaut de quoi il rembourse une partie des frais."
        ),
    ]


def _p4() -> Page:
    return [
        h1("7. Formations obligatoires"),
        p(
            "Certaines formations sont imposées par la réglementation ou par les politiques "
            "internes. La présence est obligatoire ; une absence doit être justifiée et la "
            "session rattrapée dans le trimestre suivant."
        ),
        table(
            [
                ["Formation", "Public", "Date"],
                [
                    "Lutte anti-blanchiment et connaissance du client (voir CONF-POL-01)",
                    "Tout le personnel",
                    "1er trimestre (ci-dessous)",
                ],
                [
                    "Consignes incendie et évacuation (voir SEC-CON-01)",
                    "Tout le personnel",
                    "Juin, avec exercice d'évacuation",
                ],
                [
                    "Protection des données personnelles (voir CONF-POL-02)",
                    "Tout le personnel",
                    "Septembre",
                ],
                [
                    "Sécurité informatique et fraudes par message (voir SI-CHA-01)",
                    "Tout le personnel",
                    "Octobre",
                ],
            ],
            (0.5, 0.22, 0.28),
        ),
        h2("Formation anti-blanchiment"),
        p(
            "La formation anti-blanchiment est obligatoire pour tout le personnel. La session "
            "a lieu en mars 2026, au siège et dans chaque agence, par demi-journées, afin "
            "que les guichets restent ouverts. Elle dure quatre heures et se conclut par un "
            "questionnaire individuel."
        ),
        p(
            "Pourquoi cette formation vient en premier : les institutions de microfinance "
            "manipulent beaucoup d'espèces : elles sont "
            "exposées au risque que des fonds d'origine illicite transitent par leurs "
            "comptes. Chaque salarié doit savoir reconnaître une opération inhabituelle et "
            "connaître la procédure de déclaration interne. La session rappelle aussi les "
            "sanctions encourues par l'institution et par ses salariés."
        ),
        h2("Contenu de la session anti-blanchiment"),
        *bullets(
            [
                "Les obligations de connaissance du client et de vigilance.",
                "Les signaux d'alerte : opérations fractionnées, origine des fonds floue.",
                "La procédure de déclaration interne et la confidentialité qui l'entoure.",
                "Des cas pratiques tirés de situations rencontrées en agence.",
            ]
        ),
        h2("Attestation"),
        p(
            "Chaque participant reçoit une attestation, classée dans son dossier individuel. "
            "La liste des salariés formés est tenue à la disposition des autorités de "
            "contrôle, qui peuvent la demander lors d'une inspection."
        ),
        h2("Nouveaux arrivants"),
        p(
            "Un salarié recruté après une session obligatoire suit le module hors ligne "
            "correspondant dans son premier mois, avant toute opération seule avec la "
            "clientèle, puis participe à la session suivante."
        ),
    ]


def _p5() -> Page:
    return [
        h1("8. Inscription et obligations"),
        *bullets(
            [
                "Le responsable inscrit le salarié auprès de la Direction des ressources "
                "humaines au moins deux semaines avant la session.",
                "Le salarié signe la feuille de présence à chaque demi-journée.",
                "Il remplit le questionnaire de satisfaction à la fin de la session.",
                "Il partage ce qu'il a appris avec son équipe lors de la réunion suivante.",
            ]
        ),
        h1("9. Évaluation du plan"),
        p(
            "Le plan est évalué à la fin de l'année : taux de réalisation, heures par "
            "salarié, satisfaction des participants et effets observés sur le travail, "
            "mesurés trois mois après chaque formation par le responsable."
        ),
        p(
            "L'évaluation à froid, trois mois après la session, demande au responsable si le "
            "salarié applique ce qu'il a appris. Une formation dont les effets ne sont pas "
            "visibles est revue ou remplacée l'année suivante."
        ),
        table(
            [
                ["Indicateur de fin d'année", "Cible"],
                ["Réalisation du plan (sessions tenues / prévues)", "90 % au moins"],
                ["Participation aux formations obligatoires", "100 %"],
                ["Satisfaction moyenne des participants", "4 sur 5 au moins"],
            ],
            (0.7, 0.3),
        ),
        h1("10. Questions fréquentes"),
        *faq(
            [
                (
                    "Une formation suivie à l'extérieur compte-t-elle dans mes heures ?",
                    "Oui, si elle a été autorisée par écrit et qu'une attestation est remise.",
                ),
                (
                    "Que se passe-t-il si je n'atteins pas mon volume d'heures ?",
                    "Le responsable propose des modules hors ligne au dernier trimestre pour "
                    "compléter.",
                ),
                (
                    "Les frais de déplacement pour une formation sont-ils pris en charge ?",
                    "Oui, selon la procédure des frais de mission (voir FIN-PRO-05).",
                ),
                (
                    "Puis-je proposer une formation qui n'est pas au catalogue ?",
                    "Oui, lors de l'entretien annuel ou par écrit à la DRH ; elle est examinée "
                    "pour le plan de l'année suivante, ou en cours d'année si le budget le "
                    "permet.",
                ),
            ]
        ),
        h1("11. Historique"),
        table(
            [
                ["Version", "Date", "Modification"],
                [
                    SPEC.version,
                    SPEC.approval_date,
                    "Plan de formation de l'année, approuvé par la Direction générale",
                ],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
