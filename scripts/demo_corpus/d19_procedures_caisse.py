"""Document n° 19 — Procédures de caisse en agence (OP-PRO-02, 6 pages).

Réponses attendues : plafond d'encaisse d'un guichet (page 2) et écart de caisse en
fin de journée (page 4).
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

SPEC = DOCUMENTS[19]
TELLER_CASH_CAP = 5_000_000
WITHDRAWAL_VISA = 2_000_000

# Exemple d'arrêté de caisse (page 4).
OPENING = 1_500_000
DEPOSITS = 3_240_000
WITHDRAWALS = 2_115_000
TRANSFER_TO_SAFE = 1_000_000


def build_pages() -> list[Page]:
    """Construit les 6 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Ces procédures encadrent toutes les opérations en espèces des agences : "
            "ouverture des caisses, dépôts, retraits, mouvements avec le coffre et arrêté de "
            "fin de journée. Elles protègent les fonds des clients, l'institution et les "
            "caissiers eux-mêmes : une procédure respectée est la meilleure défense d'un "
            "caissier en cas d'écart."
        ),
        h1("2. Principes"),
        *bullets(
            [
                "**Double contrôle** : tout mouvement entre le coffre et un guichet est "
                "compté par deux personnes et signé par les deux.",
                "**Traçabilité** : chaque opération est saisie dans le logiciel au moment où "
                "elle est faite, avec un reçu remis au client.",
                "**Encaisse limitée** : un guichet ne garde que les espèces nécessaires à "
                "l'activité de la journée.",
                "**Responsabilité individuelle** : chaque caissier est seul responsable de "
                "sa caisse ; personne d'autre n'y touche pendant la journée.",
            ]
        ),
        h1("3. Acteurs"),
        table(
            [
                ["Acteur", "Rôle"],
                ["Caissier", "Opérations au guichet, tenue de sa caisse, arrêté de fin de journée"],
                [
                    "Caissier principal",
                    "Gestion de la réserve de l'agence, mouvements avec le "
                    "coffre, contrôle des caissiers",
                ],
                [
                    "Chef d'agence",
                    "Visa des opérations importantes, contrôle de l'arrêté, traitement des écarts",
                ],
                ["Contrôle interne", "Inventaires surprises, contrôle des procès-verbaux"],
            ],
            (0.25, 0.75),
        ),
        callout(
            "Règle absolue",
            [
                "Aucune opération en espèces sans saisie dans le logiciel et sans reçu. Une "
                "somme reçue « en attendant » est une faute grave.",
            ],
        ),
    ]


def _p2() -> Page:
    return [
        h1("4. Ouverture de la journée"),
        table(
            [
                ["Étape", "Action"],
                [
                    "1",
                    "Le caissier principal sort du coffre la dotation de chaque guichet, "
                    "en présence d'un témoin habilité",
                ],
                [
                    "2",
                    "Chaque caissier recompte sa dotation devant le caissier principal, "
                    "billet par billet, et signe le bon de dotation",
                ],
                [
                    "3",
                    "Le caissier ouvre sa session dans le logiciel et saisit le montant de "
                    "sa dotation",
                ],
                [
                    "4",
                    "Le caissier vérifie son matériel : détecteur de faux billets, "
                    "tampon, carnets de reçus",
                ],
            ],
            (0.1, 0.9),
        ),
        h2("Plafond d'encaisse"),
        p(
            f"L'encaisse d'un guichet est plafonnée à {fcfa(TELLER_CASH_CAP)} : dès que ce "
            "montant est atteint, le surplus est versé au coffre par l'intermédiaire du "
            "caissier principal, contre un bon signé des deux. Le logiciel alerte le caissier "
            "lorsque son encaisse approche du plafond."
        ),
        h2("Pourquoi un plafond"),
        p(
            "Le plafond limite la perte en cas de vol ou de braquage, et facilite le "
            "comptage en fin de journée. Les espèces les plus utiles (petites coupures) "
            "restent au guichet ; les grosses coupures sont rangées au coffre en priorité."
        ),
        h2("Billetage"),
        p(
            "Le billetage est le détail des espèces par coupure : nombre de billets de "
            "10 000, 5 000, 2 000, 1 000 et 500 francs, et de pièces. Il est noté sur chaque "
            "bon de mouvement et sur l'arrêté de fin de journée. Les billets sont rangés par "
            "coupure, face dans le même sens, en liasses de cent."
        ),
        h2("Ordre de travail au guichet"),
        *bullets(
            [
                "Un seul client à la fois au guichet ; les autres attendent derrière la "
                "ligne de confidentialité.",
                "Les espèces du client sont comptées devant lui, puis rangées seulement après "
                "la saisie et l'impression du reçu.",
            ]
        ),
        h2("Dotation adaptée à la journée"),
        p(
            "Le caissier principal adapte la dotation au jour : plus importante les jours"
            " de paie des salariés et les jours de marché, plus faible en début de mois. "
            "Il s'appuie sur les retraits observés les semaines précédentes."
        ),
        h2("Pause du caissier"),
        p(
            "Pendant sa pause, le caissier ferme son tiroir à clé, verrouille sa session "
            "et place le panneau « guichet fermé ». Il ne confie jamais sa caisse à un "
            "collègue."
        ),
        h2("Guichet de remplacement"),
        p(
            "Si un guichet doit fermer en cours de journée, sa caisse est arrêtée avant "
            "la fermeture et les clients en attente sont orientés vers un autre guichet."
        ),
    ]


def _p3() -> Page:
    return [
        h1("5. Dépôts et retraits"),
        h2("Dépôt"),
        *bullets(
            [
                "Le client remplit le bordereau de dépôt ; le caissier l'aide si besoin.",
                "Le caissier compte les espèces devant le client et vérifie les billets au "
                "détecteur.",
                "Il saisit l'opération, imprime le reçu, le fait signer et en remet une copie.",
            ]
        ),
        h2("Retrait"),
        *bullets(
            [
                "Le caissier vérifie l'identité du client sur sa carte de membre et sa pièce "
                "d'identité, et compare la signature au spécimen affiché à l'écran.",
                "Il vérifie le solde disponible avant de compter les espèces.",
                "Il compte deux fois les billets devant le client, qui les recompte avant de "
                "quitter le guichet.",
            ]
        ),
        h2("Opérations soumises à visa"),
        table(
            [
                ["Opération", "Visa requis"],
                [f"Retrait de plus de {fcfa(WITHDRAWAL_VISA)}", "Chef d'agence, avant paiement"],
                ["Retrait par un mandataire", "Chef d'agence, vérification de la procuration"],
                ["Opération en espèces importante", "Déclaration interne selon CONF-POL-01"],
                ["Annulation d'une opération", "Chef d'agence, avec motif écrit"],
            ],
            (0.5, 0.5),
        ),
        h2("Faux billets"),
        p(
            "Un billet douteux est retenu contre un reçu indiquant sa coupure et son numéro. "
            "Le client en est informé calmement. Le billet est remis au chef d'agence, qui "
            "le transmet aux autorités selon la procédure prévue. Il n'est jamais rendu au "
            "client ni remis en circulation."
        ),
        h2("Retrait par un tiers"),
        p(
            "Un tiers ne peut retirer que s'il présente une procuration enregistrée à "
            "l'agence et sa propre pièce d'identité. Une lettre manuscrite du titulaire "
            "ne suffit pas."
        ),
        h2("Dépôt pour le compte d'un autre client"),
        p(
            "Toute personne peut déposer sur le compte d'un autre client ; son nom figure"
            " sur le bordereau. Le reçu est remis au déposant."
        ),
        h2("Opérations des salariés"),
        p(
            "Un caissier ne traite jamais une opération sur son propre compte ni sur "
            "celui d'un membre de sa famille : il s'adresse à un collègue."
        ),
    ]


def _p4() -> Page:
    theoretical = OPENING + DEPOSITS - WITHDRAWALS - TRANSFER_TO_SAFE
    return [
        h1("6. Arrêté de fin de journée"),
        p(
            "À la fermeture, chaque caissier arrête sa caisse : il compte ses espèces par "
            "coupure, édite le journal de ses opérations et compare le montant compté au "
            "solde théorique calculé par le logiciel. Le caissier principal contrôle "
            "l'arrêté avant que les fonds ne soient rangés au coffre."
        ),
        h2("Exemple d'arrêté"),
        *calculation(
            [
                ("Dotation du matin", fcfa(OPENING)),
                ("Total des dépôts de la journée", f"+ {fcfa(DEPOSITS)}"),
                ("Total des retraits de la journée", f"− {fcfa(WITHDRAWALS)}"),
                ("Versement au coffre en cours de journée", f"− {fcfa(TRANSFER_TO_SAFE)}"),
                ("Solde théorique = ligne 1 + ligne 2 − ligne 3 − ligne 4", fcfa(theoretical)),
                ("Espèces comptées (billetage)", fcfa(theoretical)),
                ("Écart = ligne 6 − ligne 5", fcfa(0)),
            ],
            "Étape du calcul",
        ),
        h2("En cas d'écart"),
        p(
            "Si l'arrêté fait apparaître un écart de caisse, la caisse est recomptée devant "
            "le chef d'agence, et un procès-verbal le jour même constate le montant de "
            "l'écart, ses causes possibles et les signatures du caissier et du chef "
            "d'agence. Aucun écart n'est reporté au lendemain sans procès-verbal."
        ),
        table(
            [
                ["Écart constaté", "Traitement"],
                [
                    "Manquant",
                    "Recherche de l'erreur dans le journal ; s'il n'est pas "
                    "retrouvé, imputation au caissier selon RH-REG-01",
                ],
                [
                    "Excédent",
                    "Placé sur un compte d'attente ; jamais conservé par le "
                    "caissier ; restitué au client concerné s'il est identifié",
                ],
                ["Écart répété", "Entretien avec le chef d'agence, formation, contrôle renforcé"],
            ],
            (0.25, 0.75),
        ),
        h2("Signature de l'arrêté"),
        p(
            "L'arrêté est signé par le caissier et par le caissier principal, puis visé "
            "par le chef d'agence. Il est classé avec le journal des opérations et les "
            "bons de mouvement de la journée."
        ),
        h2("Erreur retrouvée plus tard"),
        p(
            "Si l'origine d'un écart est retrouvée après coup (opération mal saisie, reçu"
            " oublié), la correction est faite par une écriture motivée et visée par le "
            "chef d'agence, qui complète le procès-verbal initial."
        ),
    ]


def _p5() -> Page:
    return [
        h1("7. Coffre et réserve de l'agence"),
        p(
            "Le coffre contient la réserve de l'agence et les dotations des guichets en "
            "dehors des heures d'ouverture. Ses règles d'ouverture et de garde sont fixées "
            "par la procédure de sécurité des agences (voir SEC-PRO-02). Chaque mouvement "
            "est inscrit dans le registre du coffre, signé par les deux personnes présentes."
        ),
        h2("Approvisionnement et remises au siège"),
        table(
            [
                ["Situation", "Action", "Décision"],
                ["Réserve insuffisante", "Demande d'approvisionnement au siège", "Chef d'agence"],
                ["Réserve excessive", "Remise des fonds au siège", "Chef d'agence"],
                [
                    "Transport",
                    "Par le prestataire de transport de fonds, jamais par un salarié seul",
                    "Direction des opérations",
                ],
            ],
            (0.25, 0.5, 0.25),
        ),
        h2("Inventaire surprise"),
        p(
            "Le contrôle interne ou le chef d'agence peut à tout moment arrêter une caisse "
            "et la recompter, sans prévenir le caissier. Le résultat est consigné. Le refus "
            "de se soumettre à un inventaire surprise est une faute grave."
        ),
        h2("Absence du caissier"),
        p(
            "Un caissier absent ne laisse jamais sa caisse ouverte. Si l'absence est prévue, "
            "sa caisse est arrêtée la veille et rendue au caissier principal. Son remplaçant "
            "reçoit une nouvelle dotation sous son propre nom."
        ),
        h2("Clés et codes"),
        p(
            "Chaque caissier garde sur lui la clé de son tiroir. Les doubles sont conservés "
            "sous pli scellé au coffre. Les codes personnels du logiciel ne sont jamais "
            "communiqués (voir SI-CHA-01)."
        ),
        h2("Fonds en attente de transport"),
        p(
            "Les fonds préparés pour une remise au siège sont placés en sacs scellés dans"
            " le coffre. Le numéro de chaque scellé est noté sur le bordereau et dans le "
            "registre du coffre."
        ),
        h2("Contrôle mensuel"),
        p(
            "Chaque fin de mois, le chef d'agence compare le solde du coffre et des "
            "caisses au solde comptable de l'agence, en présence du caissier principal, "
            "et signe le procès-verbal de contrôle."
        ),
        h2("Monnaie et petites coupures"),
        p(
            "L'agence veille à disposer de petites coupures suffisantes pour rendre la "
            "monnaie. Les besoins sont signalés au siège avec la demande "
            "d'approvisionnement."
        ),
        h2("Accès au registre"),
        p(
            "Le registre du coffre est conservé au coffre lui-même et n'est consulté "
            "qu'en présence des deux détenteurs des combinaisons ou par le contrôle "
            "interne."
        ),
    ]


def _p6() -> Page:
    return [
        h1("8. Interdictions"),
        *bullets(
            [
                "Prêter des fonds de la caisse, même pour quelques minutes.",
                "Échanger sa caisse avec un collègue pendant la journée.",
                "Garder des espèces personnelles dans le tiroir-caisse.",
                "Payer un retrait sans vérifier l'identité, même pour un client connu.",
                "Signer un bon de mouvement sans avoir compté soi-même.",
            ]
        ),
        h2("Sanctions"),
        p(
            "Le non-respect de ces procédures expose le caissier à des sanctions "
            "disciplinaires (voir RH-REG-01). Un manquant résultant d'une procédure non "
            "respectée peut être mis à sa charge."
        ),
        h2("Formation des caissiers"),
        p(
            "Tout nouveau caissier travaille au moins deux semaines sous la supervision "
            "du caissier principal avant de tenir seul une caisse. La détection des faux "
            "billets fait partie de sa formation."
        ),
        h2("Questions des caissiers"),
        p(
            "Le caissier principal est le premier interlocuteur des caissiers pour toute "
            "question sur ces procédures. Les cas nouveaux sont signalés à la Direction "
            "des opérations, qui complète le document lors de sa révision."
        ),
        h1("9. Questions fréquentes"),
        *faq(
            [
                (
                    "Un client conteste le montant reçu après avoir quitté le guichet.",
                    "Le caissier note la réclamation ; la caisse est contrôlée à l'arrêté. Si un "
                    "excédent apparaît, il est restitué au client (voir QUA-PRO-01).",
                ),
                (
                    "Le logiciel est en panne : que faire ?",
                    "Appliquer le mode dégradé prévu par le plan de continuité d'activité (voir "
                    "PCA-01) et saisir les opérations dès le retour du système.",
                ),
                (
                    "Puis-je refuser un billet abîmé ?",
                    "Oui s'il est illisible ou incomplet ; un billet simplement usé est accepté.",
                ),
            ]
        ),
        h1("10. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["2.0", "Mars 2023", "Plafond d'encaisse et alerte du logiciel"],
                ["2.1", SPEC.approval_date, "Inventaire surprise et traitement des écarts"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
