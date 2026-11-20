"""Document n° 18 — Catalogue des produits d'épargne (EP-CAT-01, 5 pages).

Réponses attendues : taux d'un dépôt à terme de 12 mois (page 3) et retrait avant
l'échéance (page 4).
"""

from scripts.demo_corpus.facts import DOCUMENTS, decimal_fr, fcfa, fmt_int
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

SPEC = DOCUMENTS[18]
SAVINGS_RATE = 0.02
TERM_12_RATE = 0.045
PLAN_RATE = 0.03
EXAMPLE_BALANCE = 200_000
EXAMPLE_DEPOSIT = 400_000
MONTHS_BEFORE_WITHDRAWAL = 8
PLAN_MONTHLY = 10_000


def build_pages() -> list[Page]:
    """Construit les 5 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Ce catalogue présente les produits d'épargne de Kouri Épargne & Crédit, leurs "
            "conditions et leur rémunération. Il sert de référence aux chargés de clientèle "
            "et aux caissiers pour conseiller les clients. Les frais de tenue de compte "
            "figurent dans la grille des taux et frais en vigueur (voir TAR-2026) ; les taux "
            "de rémunération de l'épargne figurent uniquement ici."
        ),
        h1("2. Pourquoi épargner chez Kouri"),
        *bullets(
            [
                "**Sécurité** : l'argent est conservé au coffre et inscrit au nom du client ; "
                "il n'est plus exposé au vol ou à l'incendie à la maison.",
                "**Rémunération** : la plupart des produits rapportent des intérêts.",
                "**Accès au crédit** : une épargne régulière est un atout pour obtenir un "
                "crédit (voir CR-PRO-01).",
                "**Discipline** : les produits à échéance aident à atteindre un objectif.",
            ]
        ),
        h1("3. La gamme"),
        table(
            [
                ["Produit", "Pour qui", "Disponibilité des fonds", "Section"],
                ["Compte courant", "Tous les clients, salariés, commerçants", "Immédiate", "4"],
                ["Livret d'épargne", "Épargne de précaution", "Immédiate, avec limites", "4"],
                [
                    "Dépôt à terme",
                    "Sommes dont on n'a pas besoin pendant une période",
                    "À l'échéance",
                    "5",
                ],
                [
                    "Plan d'épargne projet",
                    "Préparer une dépense : scolarité, fête, équipement",
                    "À l'échéance du plan",
                    "6",
                ],
            ],
            (0.22, 0.38, 0.28, 0.12),
        ),
        callout(
            "Conseil au client",
            [
                "Le chargé de clientèle aide le client à répartir son épargne : une part "
                "disponible pour les imprévus, une part placée pour mieux rapporter.",
            ],
        ),
    ]


def _p2() -> Page:
    yearly_interest = round(EXAMPLE_BALANCE * SAVINGS_RATE)
    return [
        h1("4. Compte courant et livret d'épargne"),
        h2("Compte courant"),
        p(
            "Le compte courant reçoit les dépôts, les salaires et les crédits décaissés, et "
            "permet les retraits à tout moment pendant les heures d'ouverture. Il n'est pas "
            "rémunéré. Il est soumis aux frais de tenue de compte de la grille en vigueur."
        ),
        h2("Livret d'épargne"),
        p(
            f"Le livret d'épargne est rémunéré au taux de {decimal_fr(SAVINGS_RATE * 100, 1)} "
            "% l'an, calculé sur le solde moyen de chaque mois et versé à la fin de chaque "
            "trimestre. Sa tenue est gratuite. Deux retraits par mois sont autorisés ; au-delà, "
            "les intérêts du mois ne sont pas versés."
        ),
        h2("Exemple : intérêts d'une année sur un livret"),
        *calculation(
            [
                ("Solde moyen sur l'année", fcfa(EXAMPLE_BALANCE)),
                (
                    f"Taux annuel du livret = {decimal_fr(SAVINGS_RATE, 2)}",
                    decimal_fr(SAVINGS_RATE, 2),
                ),
                ("Intérêts de l'année = ligne 1 × ligne 2", fcfa(yearly_interest)),
                ("Versés chaque trimestre = ligne 3 ÷ 4", fcfa(yearly_interest // 4)),
            ],
            "Étape du calcul",
        ),
        h2("Conditions communes"),
        table(
            [
                ["Condition", "Compte courant", "Livret d'épargne"],
                ["Dépôt initial", fcfa(2_000), fcfa(1_000)],
                ["Solde minimal", "Aucun", fcfa(1_000)],
                ["Retraits", "Libres", "Deux par mois"],
                ["Rémunération", "Aucune", "Voir ci-dessus"],
            ],
            (0.3, 0.35, 0.35),
        ),
        p(
            "Le livret peut être ouvert au nom d'un enfant mineur, selon les règles de la "
            "procédure d'ouverture de compte (voir OP-PRO-01)."
        ),
        h2("Relevés de compte"),
        p(
            "Le client peut demander un relevé de ses opérations à tout moment au "
            "guichet. Les intérêts versés sur le livret y apparaissent sur une ligne "
            "distincte, à la fin de chaque trimestre."
        ),
        h2("Ouverture d'un livret"),
        p(
            "Le livret est ouvert en même temps que le compte courant ou plus tard, sur "
            "simple demande au guichet. Le client reçoit un carnet où sont inscrits ses "
            "dépôts et retraits."
        ),
    ]


def _p3() -> Page:
    interest = round(EXAMPLE_DEPOSIT * TERM_12_RATE)
    return [
        h1("5. Dépôt à terme"),
        p(
            "Le dépôt à terme bloque une somme pendant une durée choisie par le client, en "
            "échange d'une meilleure rémunération. Les intérêts sont versés à l'échéance, en "
            "une fois, sur le compte courant du client. Le montant minimal est de "
            f"{fcfa(100_000)}."
        ),
        p(
            "Un dépôt à terme de 12 mois est rémunéré à 4,5 % par an. Les autres durées sont "
            "rémunérées selon le tableau ci-dessous. Le taux est fixé à la souscription et ne "
            "change pas jusqu'à l'échéance, même si le catalogue est modifié entre-temps."
        ),
        table(
            [
                ["Durée", "Taux annuel", "Montant minimal"],
                ["3 mois", "3 %", fcfa(100_000)],
                ["6 mois", "3,5 %", fcfa(100_000)],
                ["12 mois", "Voir ci-dessus", fcfa(100_000)],
                ["24 mois", "5,5 %", fcfa(250_000)],
            ],
            (0.3, 0.35, 0.35),
        ),
        h2("Exemple : dépôt à terme de 12 mois"),
        *calculation(
            [
                ("Montant déposé", fcfa(EXAMPLE_DEPOSIT)),
                (
                    f"Taux annuel pour 12 mois = {decimal_fr(TERM_12_RATE, 3)}",
                    decimal_fr(TERM_12_RATE, 3),
                ),
                ("Intérêts à l'échéance = ligne 1 × ligne 2", fcfa(interest)),
                (
                    "Somme disponible à l'échéance = ligne 1 + ligne 3",
                    fcfa(EXAMPLE_DEPOSIT + interest),
                ),
            ],
            "Étape du calcul",
        ),
        h2("Souscription"),
        p(
            "Le client signe un certificat de dépôt qui indique le montant, la durée, le taux "
            "et la date d'échéance. Une copie lui est remise ; l'original est classé à "
            "l'agence. Le dépôt peut être fait en espèces ou par virement depuis son compte."
        ),
        h2("Montant des intérêts et durée réelle"),
        p(
            "Les intérêts sont calculés sur le nombre exact de mois écoulés entre la date"
            " de dépôt et l'échéance. Si l'échéance tombe un jour de fermeture, les fonds"
            " sont disponibles le premier jour ouvrable suivant, sans perte d'intérêts."
        ),
        h2("Qui peut souscrire"),
        p(
            "Tout titulaire d'un compte chez Kouri, particulier, groupement ou "
            "entreprise. Un dépôt à terme au nom d'un mineur est signé par son "
            "représentant légal."
        ),
    ]


def _p4() -> Page:
    full = EXAMPLE_DEPOSIT * TERM_12_RATE * MONTHS_BEFORE_WITHDRAWAL / 12
    reduced = round(full / 2)
    return [
        h1("5 (suite). Retrait avant l'échéance"),
        p(
            "Un retrait avant l'échéance est possible, sur demande écrite du client, avec un "
            "préavis de deux jours ouvrables. Dans ce cas, les intérêts acquis sont réduits "
            "de moitié : ils sont calculés au taux du contrat pour la durée réellement "
            "écoulée, puis divisés par deux. Le capital reste intégralement remboursé."
        ),
        h2("Exemple : retrait après huit mois"),
        *calculation(
            [
                ("Montant du dépôt à terme de 12 mois", fcfa(EXAMPLE_DEPOSIT)),
                ("Durée écoulée avant le retrait", f"{MONTHS_BEFORE_WITHDRAWAL} mois"),
                (
                    f"Intérêts acquis = ligne 1 × {decimal_fr(TERM_12_RATE, 3)} × "
                    f"{MONTHS_BEFORE_WITHDRAWAL} ÷ 12",
                    fcfa(round(full)),
                ),
                ("Intérêts versés après réduction = ligne 3 ÷ 2", fcfa(reduced)),
                ("Somme remise au client = ligne 1 + ligne 4", fcfa(EXAMPLE_DEPOSIT + reduced)),
            ],
            "Étape du calcul",
        ),
        h2("À l'échéance"),
        p(
            "Sans instruction du client, le dépôt est renouvelé automatiquement pour la "
            "même durée, au taux du catalogue en vigueur à la date du renouvellement. Le "
            "client est prévenu une semaine avant l'échéance par message ou par téléphone."
        ),
        h2("Dépôt à terme en garantie d'un crédit"),
        p(
            "Un dépôt à terme peut garantir un crédit (voir CR-PRO-01, section 10). Il est "
            "alors bloqué jusqu'au remboursement complet du crédit et ne peut faire l'objet "
            "d'aucun retrait anticipé, même partiel, sans l'accord du comité qui a accordé "
            "le crédit."
        ),
        callout(
            "Bon conseil",
            [
                f"Plutôt que de placer toute son épargne sur une seule durée, le client peut "
                f"répartir ses placements, par exemple {fmt_int(EXAMPLE_DEPOSIT // 2)} FCFA "
                "sur six mois et le reste sur douze mois, pour garder de la souplesse.",
            ],
        ),
        h2("Retrait partiel"),
        p(
            "Un retrait partiel n'est pas possible : le client qui a besoin d'une partie "
            "de la somme clôture son dépôt et peut en ouvrir un nouveau pour le reste, au"
            " taux en vigueur ce jour-là."
        ),
        h2("Décès du titulaire"),
        p(
            "En cas de décès du titulaire, le dépôt est remis aux héritiers avec les "
            "intérêts calculés au taux du contrat jusqu'à la date du décès, sans "
            "réduction."
        ),
        h2("Préavis"),
        p(
            "Le préavis de deux jours ouvrables permet à l'agence de préparer les fonds. "
            "En cas d'urgence grave et justifiée (hospitalisation), le chef d'agence peut"
            " autoriser un retrait le jour même."
        ),
    ]


def _p5() -> Page:
    plan_total = PLAN_MONTHLY * 12
    return [
        h1("6. Plan d'épargne projet"),
        p(
            "Le plan d'épargne projet aide le client à préparer une dépense prévue : "
            "rentrée scolaire, mariage, achat d'équipement, pèlerinage. Le client s'engage à "
            "verser chaque mois un montant fixe pendant 6 à 24 mois. L'épargne est rémunérée "
            f"à {decimal_fr(PLAN_RATE * 100, 1)} % l'an, versés à la fin du plan."
        ),
        *calculation(
            [
                ("Versement mensuel choisi", fcfa(PLAN_MONTHLY)),
                ("Durée du plan", "12 mois"),
                ("Total versé = ligne 1 × 12", fcfa(plan_total)),
            ],
            "Étape du calcul",
        ),
        p(
            "Si le client manque trois versements, le plan est transformé en livret "
            "d'épargne ordinaire. Le plan peut être ouvert par un groupement pour un projet "
            "collectif."
        ),
        h2("Épargne des groupements"),
        p(
            "Un groupement peut ouvrir un livret ou un plan d'épargne à son nom pour "
            "financer un projet collectif. Les retraits demandent deux signatures de "
            "membres du bureau."
        ),
        h2("Évolution des taux"),
        p(
            "Les taux de ce catalogue sont révisés au plus une fois par an, par la "
            "Direction générale. Un changement s'applique aux nouvelles souscriptions et,"
            " pour le livret, à partir du trimestre suivant."
        ),
        h1("7. Questions fréquentes"),
        *faq(
            [
                (
                    "Mon épargne est-elle disponible en cas d'urgence ?",
                    "Oui pour le compte courant et le livret ; pour un dépôt à terme, un retrait "
                    "anticipé est possible avec réduction des intérêts (section 5).",
                ),
                (
                    "Les intérêts sont-ils imposés ?",
                    "Ils sont soumis à la fiscalité prévue par la réglementation, retenue à la "
                    "source par l'institution le cas échéant.",
                ),
                (
                    "Puis-je épargner pour mon enfant ?",
                    "Oui, sur un livret ouvert à son nom (voir OP-PRO-01).",
                ),
            ]
        ),
        h1("8. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Janvier 2022", "Création du catalogue"],
                ["2.0", SPEC.approval_date, "Plan d'épargne projet et dépôt à 24 mois"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
