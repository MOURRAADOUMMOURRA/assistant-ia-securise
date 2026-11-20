"""Document n° 11 — Comité de crédit et plafonds d'autorisation (CR-PRO-02, 5 pages).

Réponses attendues : plafond d'approbation du chef d'agence seul (page 2) et
approbation au-delà du plafond du comité du siège (page 4).
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

SPEC = DOCUMENTS[11]
BRANCH_MANAGER_CAP = 1_000_000
BRANCH_COMMITTEE_CAP = 3_000_000
HEAD_OFFICE_CAP = 10_000_000
EXAMPLE_OUTSTANDING = 800_000
EXAMPLE_REQUEST = 400_000


def build_pages() -> list[Page]:
    """Construit les 5 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Cette procédure fixe qui peut accorder un crédit chez Kouri Épargne & Crédit, "
            "selon son montant, et comment fonctionnent les comités de crédit. Elle complète "
            "la politique d'octroi de crédit (voir CR-PRO-01), qui définit les conditions "
            "d'éligibilité, l'analyse du dossier et les garanties. Les plafonds ci-dessous "
            "sont les seuls applicables : aucun autre document ne les reprend."
        ),
        h1("2. Principes"),
        *bullets(
            [
                "**Collégialité** : au-delà du premier niveau, un crédit est toujours décidé "
                "par plusieurs personnes réunies en comité.",
                "**Séparation des fonctions** : l'agent qui présente un dossier ne vote pas.",
                "**Traçabilité** : chaque décision est écrite, motivée et signée.",
                "**Cumul des encours** : le niveau compétent dépend du total des crédits du "
                "client, et non du seul montant demandé (section 4).",
                "**Prudence** : en cas de doute sur le niveau compétent, le dossier est "
                "présenté au niveau supérieur.",
            ]
        ),
        h1("3. Les instances de décision"),
        table(
            [
                ["Instance", "Composition", "Réunion"],
                ["Chef d'agence", "Seul, sur dossier", "À tout moment"],
                [
                    "Comité de crédit d'agence",
                    "Chef d'agence, deux agents de crédit n'ayant pas instruit le dossier",
                    "Chaque semaine",
                ],
                [
                    "Comité de crédit du siège",
                    "Directeur général, Directeur du crédit, "
                    "Directeur financier, responsable de la conformité",
                    "Tous les quinze jours",
                ],
                [
                    "Conseil d'administration",
                    "Administrateurs, sur rapport du Directeur général",
                    "Session ordinaire ou consultation écrite",
                ],
            ],
            (0.26, 0.5, 0.24),
        ),
        callout(
            "Rappel",
            [
                "Un dossier ne peut être présenté pour décision qu'après le contrôle de "
                "complétude du chef d'agence (voir CR-PRO-01, section 8).",
            ],
        ),
    ]


def _p2() -> Page:
    total = EXAMPLE_OUTSTANDING + EXAMPLE_REQUEST
    return [
        h1("4. Plafonds d'autorisation"),
        p(
            f"Le chef d'agence peut approuver seul les crédits jusqu'à "
            f"{fcfa(BRANCH_MANAGER_CAP)}, encours du client compris. Au-dessus, la décision "
            "relève d'un comité, selon le tableau suivant. Les montants s'apprécient toujours "
            "en cumulant le crédit demandé et le capital restant dû sur les crédits en cours "
            "du même client."
        ),
        table(
            [
                ["Total des encours du client après le nouveau crédit", "Instance compétente"],
                [f"{fcfa(BRANCH_MANAGER_CAP)} au plus", "Chef d'agence seul"],
                [
                    f"De {fcfa(BRANCH_MANAGER_CAP + 1)} à {fcfa(BRANCH_COMMITTEE_CAP)}",
                    "Comité de crédit d'agence",
                ],
                [
                    f"De {fcfa(BRANCH_COMMITTEE_CAP + 1)} à {fcfa(HEAD_OFFICE_CAP)}",
                    "Comité de crédit du siège",
                ],
                [f"Plus de {fcfa(HEAD_OFFICE_CAP)}", "Conseil d'administration (section 6)"],
            ],
            (0.6, 0.4),
        ),
        h2("Exemple : client qui a déjà un crédit en cours"),
        *calculation(
            [
                ("Capital restant dû sur le crédit en cours", fcfa(EXAMPLE_OUTSTANDING)),
                ("Nouveau crédit demandé", fcfa(EXAMPLE_REQUEST)),
                ("Total des encours = ligne 1 + ligne 2", fcfa(total)),
                (
                    f"Comparaison : ligne 3 supérieure à {fcfa(BRANCH_MANAGER_CAP)}",
                    "Comité de crédit d'agence",
                ),
            ],
            "Étape du calcul",
        ),
        p(
            "Dans cet exemple, le montant demandé seul resterait dans la compétence du chef "
            "d'agence ; c'est le cumul avec le crédit en cours qui impose le passage en "
            "comité. Le fractionnement d'une demande en plusieurs crédits pour rester sous "
            "un plafond est interdit."
        ),
        h2("Crédits liés"),
        p(
            "Les crédits accordés à des personnes liées (conjoints, associés d'une même "
            "entreprise, membres d'un même ménage) sont additionnés pour déterminer le "
            "niveau compétent lorsque leurs remboursements dépendent de la même activité."
        ),
        h2("Absence du titulaire"),
        p(
            "En l'absence du chef d'agence, sa compétence propre est exercée par son adjoint "
            "désigné par écrit, dans les mêmes limites. Un agent de crédit ne reçoit jamais "
            "de délégation pour décider seul d'un crédit, même de faible montant."
        ),
        h2("Contrôle a posteriori"),
        p(
            "La Direction du crédit examine chaque mois un échantillon des crédits accordés "
            "par les chefs d'agence seuls. Si la politique de crédit n'a pas été respectée, "
            "la compétence propre du chef d'agence peut être suspendue jusqu'à nouvel ordre."
        ),
    ]


def _p3() -> Page:
    return [
        h1("5. Le comité de crédit d'agence"),
        h2("Composition et quorum"),
        p(
            "Le comité d'agence est présidé par le chef d'agence. Il comprend deux agents de "
            "crédit qui n'ont pas instruit les dossiers examinés ; dans les petites agences, "
            "un agent d'une agence voisine peut siéger à distance. Le comité ne délibère que "
            "si ses trois membres sont présents. Les décisions sont prises à l'unanimité ; à "
            "défaut, le dossier est transmis au comité du siège."
        ),
        h2("Déroulement d'une séance"),
        table(
            [
                ["Étape", "Contenu"],
                [
                    "Présentation",
                    "L'agent instructeur présente le client, l'activité, "
                    "l'analyse de capacité et les garanties, puis répond aux questions",
                ],
                [
                    "Délibération",
                    "L'agent instructeur sort de la salle ; les membres échangent et votent",
                ],
                [
                    "Décision",
                    "Accord, accord sous conditions, ajournement ou refus, avec motif écrit",
                ],
                [
                    "Procès-verbal",
                    "Rédigé en séance, signé par les trois membres, classé au dossier",
                ],
            ],
            (0.22, 0.78),
        ),
        h2("Questions examinées systématiquement"),
        *bullets(
            [
                "Le revenu retenu est-il justifié par le carnet de ventes et la visite ?",
                "La mensualité respecte-t-elle la règle de capacité de CR-PRO-01 ?",
                "Le montant correspond-il au besoin réel du plan de financement ?",
                "Les garanties sont-elles réelles, évaluées et documentées ?",
                "Le client a-t-il des crédits ailleurs, et sont-ils déclarés ?",
            ]
        ),
        h2("Calendrier"),
        p(
            "Le comité se réunit chaque semaine, à jour fixe affiché dans l'agence. Une séance "
            "exceptionnelle peut être convoquée pour un crédit agricole dont la date de "
            "semis approche. Les dossiers sont remis aux membres la veille de la séance."
        ),
        h2("Visite préalable par un membre"),
        p(
            "Pour un dossier important ou atypique, le président peut demander qu'un membre "
            "du comité visite l'activité du client avant la séance. Son compte rendu écrit "
            "est joint au dossier et lu en séance."
        ),
        h2("Confidentialité des délibérations"),
        p(
            "Les débats du comité sont confidentiels. Seule la décision motivée est "
            "communiquée au client, par l'agent instructeur. Un membre qui divulgue le "
            "contenu des échanges commet une faute au sens du règlement intérieur."
        ),
    ]


def _p4() -> Page:
    return [
        h1("6. Comité du siège et Conseil d'administration"),
        h2("Comité de crédit du siège"),
        p(
            "Le comité du siège est présidé par le Directeur général. Il examine les "
            "dossiers qui dépassent la compétence du comité d'agence, les dossiers transmis "
            "faute d'unanimité et les demandes de dérogation. Le chef d'agence présente "
            "le dossier, avec l'agent instructeur ; le responsable de la conformité donne "
            "un avis écrit sur les clients à risque élevé."
        ),
        h2("Conseil d'administration"),
        p(
            f"Au-delà de {fcfa(HEAD_OFFICE_CAP)} d'encours pour un même client, le crédit "
            "est approuvé par le Conseil d'administration, sur rapport du comité du siège. "
            "En cas d'urgence motivée, le Conseil peut statuer par consultation écrite de "
            "ses membres ; la décision est alors ratifiée lors de la session suivante."
        ),
        h2("Crédits aux personnes liées à l'institution"),
        p(
            "Tout crédit à un administrateur, à un dirigeant, à un salarié occupant un poste "
            "de direction ou à un membre de leur famille proche est décidé par le Conseil "
            "d'administration, quel que soit son montant, en dehors de la présence de "
            "l'intéressé. Les prêts ordinaires au personnel suivent la politique de "
            "rémunération (voir RH-POL-04)."
        ),
        h2("Limites de concentration"),
        table(
            [
                ["Règle", "Objet"],
                [
                    "Encours d'un seul client",
                    "Plafonné à une part des fonds propres fixée "
                    "par la réglementation et rappelée chaque année par le Conseil",
                ],
                [
                    "Encours d'un même secteur d'activité",
                    "Suivi trimestriel ; alerte au "
                    "comité du siège si un secteur dépasse le quart du portefeuille",
                ],
                ["Encours d'une même agence", "Suivi mensuel par la Direction du crédit"],
                [
                    "Encours des vingt plus gros clients",
                    "Présenté chaque trimestre au Conseil d'administration",
                ],
            ],
            (0.34, 0.66),
        ),
        h2("Information du Conseil"),
        p(
            "Chaque trimestre, le Directeur général présente au Conseil la liste des crédits "
            "accordés par le comité du siège, les dérogations consenties et l'évolution des "
            "plus gros encours du portefeuille. Le Conseil peut demander l'examen détaillé "
            "de tout dossier figurant sur cette liste."
        ),
        callout(
            "Dérogations",
            [
                "Toute dérogation à la politique de crédit (âge de l'activité, garanties, "
                "durée) est décidée par l'instance immédiatement supérieure à celle qui "
                "serait normalement compétente, et motivée dans le procès-verbal.",
            ],
        ),
    ]


def _p5() -> Page:
    return [
        h1("7. Décisions et suivi"),
        table(
            [
                ["Décision", "Suite donnée"],
                [
                    "Accord",
                    "Notification au client, préparation du contrat (CR-PRO-01, section 11)",
                ],
                [
                    "Accord sous conditions",
                    "Décaissement seulement quand les conditions "
                    "sont levées et vérifiées par le chef d'agence",
                ],
                ["Ajournement", "Dossier complété puis représenté ; motif écrit"],
                [
                    "Refus",
                    "Lettre motivée au client, qui peut présenter une réclamation "
                    "(voir QUA-PRO-01)",
                ],
            ],
            (0.28, 0.72),
        ),
        h2("Registre des décisions"),
        p(
            "Chaque agence tient un registre des décisions de crédit : date, client, montant, "
            "instance, décision. Le contrôle interne le compare chaque trimestre aux "
            "décaissements enregistrés dans le logiciel, pour vérifier qu'aucun crédit n'a "
            "été décaissé sans décision de l'instance compétente."
        ),
        h2("Délais de décision"),
        p(
            "Un dossier complet reçoit une décision à la séance suivante de l'instance "
            "compétente. Si le comité du siège ou le Conseil doit se prononcer, le client "
            "est informé du délai prévisible dès la transmission du dossier."
        ),
        h1("8. Questions fréquentes"),
        *faq(
            [
                (
                    "Le chef d'agence peut-il décider seul en l'absence des agents ?",
                    "Seulement dans les limites de sa compétence propre. Au-delà, le comité est "
                    "reporté ou complété par un agent d'une agence voisine.",
                ),
                (
                    "Un comité peut-il réduire le montant demandé ?",
                    "Oui. L'accord peut porter sur un montant inférieur, si le client l'accepte.",
                ),
                (
                    "Un dossier refusé peut-il être représenté ?",
                    "Oui, après trois mois, ou plus tôt si un élément nouveau répond au motif du "
                    "refus.",
                ),
                (
                    "Que faire si un membre du comité connaît bien le client ?",
                    "Il le déclare avant la séance et se retire ; il est remplacé pour ce dossier.",
                ),
            ]
        ),
        h1("9. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["2.0", "Janvier 2024", "Création du comité du siège"],
                ["2.2", SPEC.approval_date, "Cumul des encours et crédits liés"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
