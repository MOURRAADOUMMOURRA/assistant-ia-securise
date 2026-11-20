"""Document n° 21 — Traitement des réclamations clients (QUA-PRO-01, 4 pages).

Réponses attendues : délai d'accusé de réception (page 2) et délai de réponse
définitive, puis transmission au Directeur général (page 3).
"""

from scripts.demo_corpus.facts import DOCUMENTS
from scripts.demo_corpus.render import Page, bullets, callout, faq, h1, h2, p, table, title_block

SPEC = DOCUMENTS[21]


def build_pages() -> list[Page]:
    """Construit les 4 pages du document."""
    return [_p1(), _p2(), _p3(), _p4()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Cette procédure garantit que chaque réclamation d'un client est enregistrée, "
            "examinée avec sérieux et suivie d'une réponse écrite dans un délai connu. Une "
            "réclamation bien traitée transforme souvent un client mécontent en client "
            "fidèle, et révèle des défauts à corriger dans nos pratiques."
        ),
        h1("2. Définition"),
        p(
            "Une réclamation est l'expression d'un mécontentement d'un client envers "
            "l'institution : erreur sur un compte, frais contestés, délai jugé trop long, "
            "comportement d'un salarié, refus d'un service. Une simple demande "
            "d'information ou de document n'est pas une réclamation, mais elle est traitée "
            "avec la même courtoisie."
        ),
        h1("3. Comment un client peut réclamer"),
        table(
            [
                ["Canal", "Précisions"],
                [
                    "Au guichet ou à l'accueil",
                    "Le salarié remplit la fiche de réclamation avec le client, qui la signe",
                ],
                ["Par écrit", "Lettre déposée en agence ou au siège"],
                ["Par téléphone", "Le salarié remplit la fiche et la lit au client"],
                ["Boîte à suggestions", "Présente dans chaque agence ; relevée chaque semaine"],
            ],
            (0.3, 0.7),
        ),
        h2("Principes"),
        *bullets(
            [
                "Toute réclamation est acceptée, même si elle paraît infondée.",
                "Le traitement est gratuit pour le client.",
                "Le salarié mis en cause ne traite pas la réclamation qui le concerne.",
                "Aucune mesure de représailles n'est prise contre un client qui réclame.",
            ]
        ),
        h2("Accueil du client mécontent"),
        p(
            "Le salarié écoute le client sans l'interrompre, reformule sa demande et "
            "reste courtois, même face à un ton vif. Il évite de se justifier ou de "
            "mettre en cause un collègue devant le client."
        ),
    ]


def _p2() -> Page:
    return [
        h1("4. Enregistrement et accusé de réception"),
        p(
            "Chaque réclamation est inscrite le jour même dans le registre des réclamations "
            "de l'agence, avec un numéro. Le client reçoit un accusé de réception sous 48 h "
            "ouvrées, qui indique le numéro de sa réclamation, le nom de la personne chargée "
            "de la traiter et le délai de réponse. L'accusé est remis en main propre, par "
            "message ou par courrier."
        ),
        h2("Classement des réclamations"),
        table(
            [
                ["Catégorie", "Exemples", "Traitée par"],
                ["Opérations de caisse", "Erreur de montant, dépôt non crédité", "Chef d'agence"],
                [
                    "Frais et intérêts",
                    "Frais contestés, calcul d'intérêts",
                    "Chef d'agence, avec la Direction financière",
                ],
                [
                    "Crédit",
                    "Refus, délai, conditions, recouvrement",
                    "Chef d'agence, avec la Direction du crédit",
                ],
                [
                    "Comportement d'un salarié",
                    "Impolitesse, demande d'argent",
                    "Direction des ressources humaines",
                ],
                [
                    "Données personnelles",
                    "Accès, rectification, divulgation",
                    "Conformité (voir CONF-POL-02)",
                ],
            ],
            (0.28, 0.4, 0.32),
        ),
        h2("Réclamations graves"),
        p(
            "Une réclamation qui évoque une fraude, un détournement, une demande d'argent "
            "par un salarié ou une divulgation d'informations est transmise immédiatement "
            "à la Direction générale et au contrôle interne, sans attendre le délai de "
            "traitement habituel."
        ),
        h2("Contenu de la fiche de réclamation"),
        *bullets(
            [
                "Identité et coordonnées du client, numéro de compte.",
                "Description des faits, dates, montants en cause.",
                "Ce que le client demande : correction, remboursement, explication.",
                "Pièces remises par le client.",
            ]
        ),
        h2("Suivi du registre"),
        p(
            "Le chef d'agence consulte le registre chaque semaine et vérifie que chaque "
            "réclamation avance dans les délais. Le registre ne contient que les "
            "informations nécessaires au traitement."
        ),
        h2("Information du client en cours de traitement"),
        p(
            "Si l'examen nécessite des vérifications au siège, le client en est informé "
            "et reçoit un nouveau point d'avancement dès que possible."
        ),
        h2("Réclamation reçue au siège"),
        p(
            "Une réclamation adressée au siège est enregistrée par le service qualité, "
            "puis transmise à l'agence concernée avec copie de l'accusé de réception."
        ),
    ]


def _p3() -> Page:
    return [
        h1("5. Examen et réponse"),
        p(
            "La personne chargée du dossier rassemble les pièces, interroge les salariés "
            "concernés et vérifie les opérations dans le logiciel. Le client reçoit une "
            "réponse définitive écrite dans un délai de 15 jours ouvrables à compter de la "
            "réception de sa réclamation. Si ce délai ne peut être tenu, ou si le client "
            "conteste la réponse, la réclamation est transmise au Directeur général, qui y "
            "répond personnellement."
        ),
        h2("Contenu de la réponse"),
        *bullets(
            [
                "Rappel de la réclamation et des vérifications effectuées.",
                "Décision : réclamation fondée, partiellement fondée ou non fondée.",
                "Mesure prise : correction, remboursement, excuses, explication.",
                "Possibilité de recours auprès du Directeur général.",
            ]
        ),
        h2("Réparation"),
        p(
            "Lorsque la réclamation est fondée, l'erreur est corrigée sans délai : "
            "recrédit du compte, remboursement des frais prélevés à tort, rectification "
            "d'une information. La correction est visible sur le relevé du client, à qui "
            "l'on présente des excuses."
        ),
        h2("Recours"),
        p(
            "Après la réponse du Directeur général, le client qui reste insatisfait peut "
            "saisir l'autorité de supervision des établissements de microfinance ou les "
            "voies de droit ordinaires. Ces possibilités sont indiquées dans la réponse."
        ),
        callout(
            "Bon réflexe",
            [
                "Une réclamation simple (erreur évidente au guichet) peut être réglée sur le "
                "champ ; elle est tout de même enregistrée, pour mesurer et prévenir les "
                "erreurs.",
            ],
        ),
        h2("Réclamation non fondée"),
        p(
            "Lorsque la réclamation n'est pas fondée, la réponse l'explique avec des "
            "éléments précis : copie du reçu, extrait du contrat, calcul détaillé. Le ton"
            " reste respectueux ; on remercie le client de sa démarche."
        ),
        h2("Geste commercial"),
        p(
            "Le chef d'agence peut accorder un geste commercial limité (remise de frais) "
            "pour tenir compte d'un désagrément, même quand l'institution n'a pas commis "
            "d'erreur. Il le motive par écrit."
        ),
        h2("Clôture du dossier"),
        p(
            "La réclamation est close lorsque la réponse définitive a été remise et, le "
            "cas échéant, la correction effectuée. La date de clôture est inscrite au "
            "registre."
        ),
    ]


def _p4() -> Page:
    return [
        h1("6. Suivi et amélioration"),
        p(
            "Le service qualité reçoit chaque mois la copie des registres de réclamations. "
            "Il analyse les causes les plus fréquentes et propose des actions : formation, "
            "modification d'un document, amélioration d'un affichage."
        ),
        table(
            [
                ["Indicateur", "Objectif"],
                ["Accusés de réception remis dans le délai", "100 %"],
                ["Réponses définitives dans le délai", "95 % au moins"],
                ["Réclamations transmises au Directeur général", "Suivies une à une"],
                ["Réclamations répétées sur un même sujet", "En baisse d'un trimestre à l'autre"],
            ],
            (0.6, 0.4),
        ),
        h2("Rapport annuel"),
        p(
            "Le service qualité présente chaque année à la Direction générale un rapport "
            "sur les réclamations : nombre, catégories, délais, actions menées. Le "
            "rapport est présenté au Conseil d'administration."
        ),
        h2("Conservation des dossiers"),
        p(
            "Les dossiers de réclamation sont conservés au moins cinq ans. Ils peuvent "
            "être consultés par l'audit interne et par les autorités de contrôle."
        ),
        h2("Formation"),
        p(
            "Les salariés au contact des clients sont formés à l'accueil des réclamations"
            " lors de leur intégration, et lors des formations prévues au plan de "
            "formation annuel."
        ),
        h2("Suggestions des clients"),
        p(
            "Les suggestions déposées dans la boîte de l'agence sont lues par le chef "
            "d'agence et transmises au service qualité. Les meilleures idées sont mises "
            "en œuvre et présentées aux équipes."
        ),
        h1("7. Questions fréquentes"),
        *faq(
            [
                (
                    "Un client se plaint oralement mais refuse de signer une fiche.",
                    "Remplissez la fiche avec la mention « refus de signer » ; la réclamation "
                    "est traitée normalement.",
                ),
                (
                    "La réclamation concerne un autre établissement.",
                    "Expliquez poliment au client à qui s'adresser ; aucune fiche n'est ouverte.",
                ),
            ]
        ),
        h1("8. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Octobre 2022", "Création de la procédure"],
                ["1.1", SPEC.approval_date, "Classement des réclamations et indicateurs"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
