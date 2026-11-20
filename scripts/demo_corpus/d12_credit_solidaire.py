"""Document n° 12 — Crédit solidaire aux groupements (CR-PRO-03, 5 pages).

Réponses attendues : taille d'un groupement (page 2) et conséquence du défaut d'un
membre (page 3).
"""

from scripts.demo_corpus.facts import DOCUMENTS, fcfa, fmt_int
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

SPEC = DOCUMENTS[12]
GROUP_SIZE_EXAMPLE = 9
MISSED_INSTALLMENT = 16_000


def build_pages() -> list[Page]:
    """Construit les 5 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Le crédit solidaire permet à des personnes qui n'ont pas de garantie matérielle "
            "d'emprunter ensemble, en se portant garantes les unes des autres. Il s'adresse "
            "en particulier aux femmes commerçantes et aux membres de tontines, qui se "
            "connaissent et se font confiance. Cette procédure complète la politique "
            "d'octroi de crédit (voir CR-PRO-01) pour tout ce qui concerne les groupements."
        ),
        h1("2. Principe de la caution solidaire"),
        p(
            "Chaque membre reçoit un crédit individuel, mais tous les membres s'engagent, "
            "par un acte signé ensemble, à rembourser la totalité des crédits du groupe. La "
            "pression amicale du groupe remplace la garantie matérielle : chacun choisit ses "
            "partenaires et veille à ce que tous remboursent."
        ),
        h2("Avantages pour les membres"),
        *bullets(
            [
                "Accès au crédit sans gage ni hypothèque.",
                "Montants qui augmentent à chaque cycle réussi.",
                "Réunions régulières qui permettent d'échanger conseils et contacts.",
                "Constitution progressive d'une épargne personnelle.",
            ]
        ),
        h2("Public visé"),
        p(
            "Les groupements sont formés de personnes qui exercent une activité génératrice "
            "de revenus de petite taille : vente au marché, transformation de produits "
            "agricoles, restauration, couture, petit élevage. Les salariés peuvent en faire "
            "partie s'ils exercent aussi une activité propre. Une personne qui a déjà un "
            "crédit individuel en cours chez Kouri ne peut pas rejoindre un groupement."
        ),
        callout(
            "À retenir",
            [
                "Le crédit solidaire n'est pas un crédit au groupe : chaque membre a son "
                "propre crédit, mais tous en garantissent ensemble le remboursement.",
            ],
        ),
    ]


def _p2() -> Page:
    return [
        h1("3. Constitution d'un groupement"),
        p(
            "Un groupement compte de 5 à 15 membres. En dessous, la solidarité pèse trop "
            "lourd sur chacun ; au-dessus, les membres ne se connaissent plus assez pour se "
            "garantir mutuellement. Les membres se choisissent librement ; l'agent de crédit "
            "ne compose jamais un groupe à leur place."
        ),
        h2("Conditions à respecter"),
        table(
            [
                ["Condition", "Raison"],
                [
                    "Habiter ou travailler dans le même quartier ou le même marché",
                    "Les membres doivent pouvoir se réunir et se rendre visite facilement",
                ],
                [
                    "Au plus deux membres d'une même famille proche",
                    "Éviter qu'un problème familial bloque tout le groupe",
                ],
                [
                    "Exercer chacun sa propre activité",
                    "Un seul échec d'activité ne doit pas toucher plusieurs membres",
                ],
                ["Être membre d'aucun autre groupement Kouri", "Éviter les engagements croisés"],
                ["Détenir chacun un compte chez Kouri", "Recevoir le crédit et épargner"],
            ],
            (0.48, 0.52),
        ),
        h2("Organisation interne"),
        p(
            "Le groupement élit un bureau de trois membres : une présidente ou un président, "
            "un secrétaire et un trésorier. Le bureau anime les réunions, tient la liste de "
            "présence et collecte les remboursements quand ils sont faits en réunion. Le "
            "groupement adopte un règlement intérieur simple, signé par tous : jour et lieu "
            "des réunions, amendes de retard décidées par le groupe, règles de remplacement "
            "d'un membre."
        ),
        h2("Formation préalable"),
        p(
            "Avant le premier crédit, l'agent anime quatre séances d'une heure : principe de "
            "la caution solidaire, calcul des remboursements, gestion d'une petite activité "
            "et règles de l'institution. Un membre absent à plus d'une séance ne peut pas "
            "recevoir de crédit au premier cycle."
        ),
        h2("Visite de reconnaissance"),
        p(
            "Avant le premier cycle, l'agent visite l'activité de chaque membre, comme pour "
            "un crédit individuel, et vérifie que le montant demandé correspond au besoin. Il "
            "s'assure aussi que chaque membre a choisi librement de rejoindre le groupe et "
            "comprend son engagement envers les autres."
        ),
        h2("Validation du groupement"),
        p(
            "Le chef d'agence valide la constitution du groupement sur la base de la liste "
            "des membres, du procès-verbal d'élection du bureau, du règlement intérieur signé "
            "et de l'attestation de formation. Les crédits des membres sont ensuite décidés "
            "selon les plafonds de CR-PRO-02, en cumulant les montants du groupe."
        ),
    ]


def _p3() -> Page:
    share = MISSED_INSTALLMENT // (GROUP_SIZE_EXAMPLE - 1)
    return [
        h1("4. Fonctionnement de la caution solidaire"),
        p(
            "Si un membre ne rembourse pas, les autres membres remboursent à sa place pour "
            "que l'échéance du groupe soit payée en totalité. Tant qu'une échéance d'un "
            "membre reste impayée, le groupe ne peut plus emprunter : aucun nouveau crédit "
            "n'est accordé à aucun de ses membres. Le membre défaillant reste débiteur des "
            "sommes avancées par les autres, qui peuvent les lui réclamer."
        ),
        h2("Exemple : un membre ne paie pas son échéance"),
        *calculation(
            [
                ("Nombre de membres du groupement", str(GROUP_SIZE_EXAMPLE)),
                ("Échéance non payée par un membre", fcfa(MISSED_INSTALLMENT)),
                ("Membres qui se partagent l'échéance = ligne 1 − 1", str(GROUP_SIZE_EXAMPLE - 1)),
                ("Part de chaque membre = ligne 2 ÷ ligne 3", fcfa(share)),
            ],
            "Étape du calcul",
        ),
        h2("Conduite à tenir par l'agent de crédit"),
        table(
            [
                ["Moment", "Action"],
                [
                    "Jour de l'échéance",
                    "Constater le manquant en réunion et demander au groupe de le couvrir",
                ],
                [
                    "Dans la semaine",
                    "Rendre visite au membre défaillant avec un membre du "
                    "bureau pour comprendre la cause",
                ],
                [
                    "Échéance suivante",
                    "Si le défaut persiste, appliquer la procédure de "
                    "recouvrement (voir CR-PRO-04)",
                ],
            ],
            (0.25, 0.75),
        ),
        h2("Épargne de garantie"),
        p(
            "Chaque membre dépose avant le décaissement une épargne de garantie égale à "
            "10 % de son crédit. Elle reste bloquée jusqu'au remboursement complet de tout "
            f"le groupe. Exemple : pour un crédit de {fmt_int(100_000)} FCFA, l'épargne de "
            f"garantie est de {fcfa(10_000)}."
        ),
        h2("Membre en difficulté de bonne foi"),
        p(
            "Si un membre ne peut plus payer à la suite d'un événement grave (maladie, "
            "incendie de son étal), le groupe peut demander à l'agence un rééchelonnement de "
            "son crédit, décidé selon CR-PRO-01. En attendant, la solidarité du groupe "
            "continue de s'appliquer."
        ),
        h2("Récupération des sommes avancées"),
        p(
            "Le membre défaillant rembourse au groupe les sommes avancées par les autres, "
            "selon un échéancier convenu en réunion et noté au procès-verbal. L'institution "
            "n'intervient pas dans ce remboursement interne, mais l'agent veille à ce qu'il "
            "se fasse sans violence ni humiliation."
        ),
    ]


def _p4() -> Page:
    return [
        h1("5. Montants, durées et remboursements"),
        table(
            [
                ["Cycle", "Montant par membre", "Durée"],
                ["1er cycle", f"De {fcfa(50_000)} à {fcfa(150_000)}", "4 à 6 mois"],
                ["2e cycle", f"Jusqu'à {fcfa(250_000)}", "6 à 9 mois"],
                ["3e cycle et suivants", f"Jusqu'à {fcfa(400_000)}", "6 à 12 mois"],
            ],
            (0.25, 0.5, 0.25),
        ),
        p(
            "Le passage au cycle supérieur suppose que tout le groupe ait remboursé le "
            "cycle précédent sans recours prolongé à la solidarité. Les montants peuvent "
            "différer d'un membre à l'autre, selon l'activité et la capacité de chacun. Le "
            "taux d'intérêt et les frais sont ceux de la ligne « Crédit solidaire » de la "
            "grille des taux et frais en vigueur (voir TAR-2026)."
        ),
        h2("Réunions de remboursement"),
        p(
            "Les remboursements ont lieu lors de réunions tous les quinze jours, au lieu "
            "choisi par le groupe, en présence de l'agent de crédit. Chaque membre verse sa "
            "part au trésorier, qui remet la somme totale à l'agent contre un reçu "
            "numéroté. Les montants sont reportés le jour même dans le logiciel."
        ),
        h2("Sécurité de la collecte"),
        *bullets(
            [
                "L'agent ne transporte jamais seul une somme importante : au-delà du seuil "
                "fixé par l'agence, le versement est fait par le trésorier au guichet.",
                "Chaque reçu indique le montant, la date et le nom du groupement ; une copie "
                "reste au carnet.",
                "Le versement individuel direct au guichet reste toujours possible.",
            ]
        ),
        h2("Décaissement"),
        p(
            "Les crédits de tous les membres sont décaissés le même jour, sur leurs comptes "
            "individuels, en présence du bureau du groupement. Chaque membre signe son "
            "contrat et reçoit son tableau d'amortissement, expliqué en réunion."
        ),
        h2("Épargne régulière"),
        p(
            "En plus de l'épargne de garantie, chaque membre est encouragé à verser une "
            "petite épargne libre à chaque réunion. Cette épargne reste disponible et sert "
            "souvent à faire face aux imprévus sans manquer une échéance."
        ),
        callout(
            "Signal d'alerte",
            [
                "Un groupe qui couvre souvent les échéances d'un même membre est fragile : "
                "l'agent en informe le chef d'agence avant le cycle suivant.",
            ],
        ),
    ]


def _p5() -> Page:
    return [
        h1("6. Vie du groupement"),
        h2("Départ et remplacement d'un membre"),
        p(
            "Un membre qui a remboursé son crédit peut quitter le groupe à la fin d'un "
            "cycle. Le groupe peut accueillir un nouveau membre, qui suit la formation "
            "préalable. Un membre ne peut pas quitter le groupe en cours de cycle tant qu'un "
            "crédit d'un autre membre reste dû."
        ),
        h2("Dissolution"),
        p(
            "Le groupe peut décider sa dissolution à la fin d'un cycle, une fois tous les "
            "crédits remboursés. L'épargne de garantie est alors libérée et chaque membre "
            "peut demander un crédit individuel s'il remplit les conditions de CR-PRO-01."
        ),
        h2("Rôle de l'agent de crédit"),
        p(
            "L'agent anime le groupe sans le diriger : il rappelle les règles, contrôle les "
            "remboursements, conseille les membres et repère les difficultés. Il ne garde "
            "jamais l'argent, les carnets ou les pièces d'identité des membres."
        ),
        h1("7. Questions fréquentes"),
        *faq(
            [
                (
                    "Un membre peut-il être exclu du groupe ?",
                    "Oui, par décision des deux tiers des membres à la fin d'un cycle, après "
                    "remboursement de sa dette envers le groupe.",
                ),
                (
                    "La tontine du groupe est-elle gérée par Kouri ?",
                    "Non. La tontine reste l'affaire des membres ; Kouri ne gère que les "
                    "comptes et les crédits.",
                ),
                (
                    "Un groupe d'hommes ou mixte est-il possible ?",
                    "Oui, le crédit solidaire est ouvert à tous.",
                ),
                (
                    "Un membre peut-il demander un crédit individuel plus tard ?",
                    "Oui, après au moins deux cycles réussis, s'il remplit les conditions de "
                    "CR-PRO-01 ; ses cycles en groupe comptent dans son historique.",
                ),
            ]
        ),
        h1("8. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Mars 2021", "Création du produit"],
                ["1.5", SPEC.approval_date, "Épargne de garantie et sécurité de la collecte"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
