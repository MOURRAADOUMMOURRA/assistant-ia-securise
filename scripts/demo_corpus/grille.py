"""Modèle commun des grilles des taux et frais (documents n° 13 et 14, 4 pages chacun).

Le texte est strictement le même d'une année à l'autre : seuls les chiffres,
lus dans `facts.GRIDS`, changent. Les rubriques des grilles 2025 et 2026 sont
donc identiques par construction (le vérificateur le contrôle en masquant les
chiffres). Les calculs sont effectués ici puis présentés ligne par ligne.
"""

from dataclasses import dataclass

from scripts.demo_corpus.facts import (
    DOCUMENTS,
    EXAMPLE_LOAN_FCFA,
    EXAMPLE_LOAN_MONTHS,
    TariffGrid,
    decimal_fr,
    fcfa,
    fmt_int,
    pct,
)
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

STATEMENTS_PER_YEAR = 2
"""Nombre de relevés à la demande dans l'exemple de coût annuel d'un compte."""


@dataclass(frozen=True)
class LoanExample:
    """Résultats de l'exemple chiffré d'un crédit AGR."""

    monthly_rate: float
    installment: int
    total_repaid: int
    interest: int
    dossier_fee: int
    insurance: int
    total_cost: int
    net_disbursed: int


def compute_loan_example(grid: TariffGrid) -> LoanExample:
    """Calcule la mensualité constante et le coût total du crédit AGR de l'exemple."""
    principal, months = EXAMPLE_LOAN_FCFA, EXAMPLE_LOAN_MONTHS
    monthly_rate = grid.agr_rate_pct / 100 / 12
    installment = round(principal * monthly_rate / (1 - (1 + monthly_rate) ** -months))
    total_repaid = installment * months
    interest = total_repaid - principal
    dossier_fee = max(round(principal * grid.dossier_fee_pct / 100), grid.dossier_fee_min_fcfa)
    insurance = round(principal * grid.insurance_pct / 100)
    return LoanExample(
        monthly_rate=monthly_rate,
        installment=installment,
        total_repaid=total_repaid,
        interest=interest,
        dossier_fee=dossier_fee,
        insurance=insurance,
        total_cost=interest + dossier_fee + insurance,
        net_disbursed=principal - dossier_fee - insurance,
    )


def build_grid_pages(grid: TariffGrid) -> list[Page]:
    """Construit les 4 pages de la grille d'une année."""
    return [_page_1(grid), _page_2(grid), _page_3(grid), _page_4(grid)]


def _page_1(grid: TariffGrid) -> Page:
    spec = DOCUMENTS[grid.document]
    return [
        *title_block(spec),
        h1("1. Objet"),
        p(
            "La présente grille fixe les taux d'intérêt et les frais appliqués par Kouri "
            f"Épargne & Crédit S.A. à compter du {spec.effective_date}. Elle remplace la grille "
            f"{grid.replaces_reference}, qui cesse de s'appliquer aux nouveaux contrats à cette "
            "date. Elle est approuvée chaque année par le Conseil d'administration, sur "
            "proposition de la Direction financière."
        ),
        h1("2. Champ d'application"),
        *bullets(
            [
                "**Nouveaux crédits** : tout contrat signé à partir de la date d'application "
                "suit les taux et frais de la présente grille.",
                "**Crédits en cours** : un contrat signé sous une grille antérieure garde son "
                "taux jusqu'à son terme ; seuls les frais de services ci-dessous changent.",
                "**Services de compte** : les tarifs de la section 7 s'appliquent à tous les "
                "comptes, anciens et nouveaux, dès la date d'application.",
                "**Épargne** : les taux de rémunération de l'épargne ne figurent pas ici ; ils "
                "sont publiés dans le Catalogue des produits d'épargne (voir EP-CAT-01).",
            ]
        ),
        h1("3. Principes de calcul"),
        *bullets(
            [
                "Les taux sont des taux nominaux annuels, calculés sur le capital restant dû.",
                "Le taux mensuel est égal au taux annuel divisé par 12.",
                "Les crédits sont remboursés par mensualités constantes, arrondies au franc le "
                "plus proche ; le crédit agricole suit le calendrier de la récolte.",
                "Les frais de dossier et l'assurance sont prélevés une seule fois, le jour du "
                "décaissement, sur le montant versé au client.",
                "Les frais s'entendent hors taxes ; les taxes prévues par la réglementation en "
                "vigueur s'y ajoutent.",
            ]
        ),
        callout(
            "À retenir",
            [
                "En cas de différence entre cette grille et un document plus ancien, c'est "
                "toujours la grille la plus récente qui s'applique. Avant toute simulation, "
                "l'agent vérifie l'année de la grille qu'il consulte.",
            ],
        ),
    ]


def _page_2(grid: TariffGrid) -> Page:
    example = compute_loan_example(grid)
    rows = [["Produit", "Durée maximale", "Taux nominal annuel"]]
    rows += [
        [rate.product, rate.max_duration, f"{pct(rate.annual_rate_pct)} par an"]
        for rate in grid.credit_rates
    ]
    principal = fmt_int(EXAMPLE_LOAN_FCFA)
    return [
        h1("4. Taux d'intérêt des crédits"),
        table(rows, (0.56, 0.18, 0.26)),
        h1("5. Frais liés au crédit"),
        table(
            [
                ["Frais", "Montant", "Prélèvement"],
                [
                    "Frais de dossier",
                    f"{pct(grid.dossier_fee_pct)} du montant du crédit, minimum "
                    f"{fcfa(grid.dossier_fee_min_fcfa)}",
                    "Au décaissement",
                ],
                [
                    "Assurance décès-invalidité",
                    f"{pct(grid.insurance_pct)} du capital emprunté",
                    "Au décaissement",
                ],
                [
                    "Pénalité de retard",
                    f"{pct(grid.late_penalty_pct)} de l'échéance impayée, par mois de retard",
                    "À la régularisation",
                ],
                [
                    "Rééchelonnement accordé",
                    fcfa(grid.rescheduling_fee_fcfa),
                    "À la signature de l'avenant",
                ],
                ["Remboursement anticipé", "Sans frais", "—"],
            ],
            (0.3, 0.46, 0.24),
        ),
        h2("6. Exemple chiffré : crédit AGR"),
        *calculation(
            [
                ("Montant emprunté (C)", fcfa(EXAMPLE_LOAN_FCFA)),
                ("Durée (n)", f"{EXAMPLE_LOAN_MONTHS} mensualités"),
                (
                    f"Taux mensuel t = taux annuel AGR ÷ 12 = "
                    f"{decimal_fr(grid.agr_rate_pct / 100, 4)} ÷ 12",
                    decimal_fr(example.monthly_rate, 4),
                ),
                (
                    "Mensualité = C × t ÷ (1 − (1 + t) puissance −n), arrondie au franc",
                    fcfa(example.installment),
                ),
                (
                    f"Total remboursé = mensualité × {EXAMPLE_LOAN_MONTHS}",
                    fcfa(example.total_repaid),
                ),
                ("Intérêts = total remboursé − C", fcfa(example.interest)),
                (
                    f"Frais de dossier = {decimal_fr(grid.dossier_fee_pct / 100, 4)} × {principal} "
                    "(supérieur au minimum)",
                    fcfa(example.dossier_fee),
                ),
                (
                    f"Assurance = {decimal_fr(grid.insurance_pct / 100, 4)} × {principal}",
                    fcfa(example.insurance),
                ),
                ("Coût total du crédit = lignes 6 + 7 + 8", fcfa(example.total_cost)),
                ("Montant net versé au client = C − lignes 7 et 8", fcfa(example.net_disbursed)),
            ],
            "Étape du calcul",
        ),
        p(
            "Comment lire cet exemple : le client reçoit le montant de la ligne 10 sur son "
            "compte, puis rembourse chaque mois la mensualité de la ligne 4. Le coût total de "
            "la ligne 9 est le montant que l'agent doit annoncer au client, par écrit, avant la "
            "signature du contrat. Pour un autre montant ou une autre durée, l'agent refait le "
            "calcul dans le logiciel avec le taux du produit concerné."
        ),
    ]


def _page_3(grid: TariffGrid) -> Page:
    rows = [["Service", "Tarif"]]
    rows.append(["Tenue de compte courant", f"{fcfa(grid.account_fee_monthly_fcfa)} par mois"])
    rows.append(["Tenue de livret d'épargne", "Gratuit"])
    rows += [[service.service, fcfa(service.fee_fcfa)] for service in grid.services]
    rows.append(["Retrait ou dépôt au guichet de son agence", "Gratuit"])
    statement, attestation = grid.services[0].fee_fcfa, grid.services[1].fee_fcfa
    yearly_account = 12 * grid.account_fee_monthly_fcfa
    statements = STATEMENTS_PER_YEAR * statement
    return [
        h1("7. Frais de tenue de compte et de services"),
        p(
            "Les tarifs ci-dessous s'appliquent aux comptes des particuliers, des "
            "entrepreneurs individuels et des groupements. Ils sont affichés dans chaque "
            "agence, à la vue des clients, et remis sur simple demande. Aucun autre frais que "
            "ceux de la présente grille ne peut être prélevé sur un compte."
        ),
        table(rows, (0.66, 0.34)),
        h1("8. Exemple : coût annuel d'un compte courant"),
        *calculation(
            [
                (
                    f"Tenue de compte = 12 mois × {fmt_int(grid.account_fee_monthly_fcfa)}",
                    fcfa(yearly_account),
                ),
                (
                    f"Relevés à la demande = {STATEMENTS_PER_YEAR} × {fmt_int(statement)}",
                    fcfa(statements),
                ),
                ("Une attestation de solde", fcfa(attestation)),
                (
                    "Coût annuel total = lignes 1 + 2 + 3",
                    fcfa(yearly_account + statements + attestation),
                ),
            ],
            "Étape du calcul",
        ),
        h1("9. Règles d'application des frais"),
        *bullets(
            [
                "La tenue de compte est prélevée le dernier jour ouvrable de chaque mois. Le "
                "premier mois qui suit l'ouverture du compte est offert.",
                "Si le solde ne suffit pas, aucun découvert n'est créé : les frais sont "
                "prélevés au prochain dépôt et apparaissent sur le relevé.",
                "Les virements entre deux comptes d'un même client sont gratuits ; le tarif de "
                "la grille s'applique aux virements vers le compte d'un autre client.",
                "Toute exonération exceptionnelle est accordée par écrit par le chef d'agence "
                "et enregistrée dans le logiciel, avec son motif.",
                "Un compte sans aucun mouvement pendant 12 mois devient inactif : la tenue de "
                "compte n'est plus prélevée, et le client est invité à le réactiver ou à le "
                "clôturer.",
            ]
        ),
    ]


def _page_4(grid: TariffGrid) -> Page:
    spec = DOCUMENTS[grid.document]
    return [
        h1("10. Entrée en vigueur et révision"),
        p(
            f"La présente grille entre en vigueur le {spec.effective_date}. Elle reste "
            "applicable jusqu'à la publication de la grille suivante, en principe au début de "
            "l'année civile. En cours d'année, une modification n'est possible qu'après "
            "décision du Conseil d'administration ; elle est alors affichée en agence au moins "
            "un mois avant sa date d'effet."
        ),
        p(
            "Les clients sont informés de chaque nouvelle grille par affichage en agence, par "
            "message aux titulaires d'un compte courant et lors de tout nouvel entretien de "
            "crédit. L'agent remet la grille en vigueur avec chaque offre de crédit."
        ),
        h1("11. Questions fréquentes"),
        *faq(
            [
                (
                    f"Mon crédit a été signé avant le {spec.effective_date}. "
                    "Quel taux s'applique ?",
                    "Le taux de votre contrat reste celui de la grille en vigueur à la date de "
                    "signature, jusqu'à la fin du contrat.",
                ),
                (
                    "La tenue de compte s'applique-t-elle à un livret d'épargne ?",
                    "Non. La tenue d'un livret d'épargne est gratuite (section 7).",
                ),
                (
                    "Où trouver les taux de rémunération de l'épargne ?",
                    "Dans le Catalogue des produits d'épargne (voir EP-CAT-01).",
                ),
                (
                    "Un remboursement anticipé est-il pénalisé ?",
                    "Non. Il est sans frais, et les intérêts cessent de courir sur le capital "
                    "remboursé.",
                ),
                (
                    "Comment contester un frais prélevé ?",
                    "Adressez une réclamation à votre agence (voir QUA-PRO-01). Le frais est "
                    "remboursé s'il a été prélevé à tort.",
                ),
                (
                    "Les frais de dossier sont-ils remboursés si je renonce au crédit ?",
                    "Ils ne sont prélevés qu'au décaissement. Si vous renoncez avant, aucun frais "
                    "n'est dû.",
                ),
                (
                    "Les taux sont-ils négociables ?",
                    "Non. Les taux et frais de la grille s'appliquent de la même façon à tous les "
                    "clients, sans négociation individuelle, pour garantir l'égalité de "
                    "traitement.",
                ),
            ]
        ),
        h1("12. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                [
                    spec.version,
                    spec.approval_date,
                    f"Grille {grid.year} approuvée par le Conseil d'administration ; remplace "
                    f"{grid.replaces_reference}",
                ],
            ],
            (0.14, 0.24, 0.62),
        ),
        p(
            "Pour toute question sur l'application de la grille, l'agent s'adresse à son chef "
            "d'agence, qui saisit si nécessaire la Direction financière au siège."
        ),
    ]
