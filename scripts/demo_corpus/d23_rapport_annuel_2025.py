"""Document n° 23 — Rapport annuel 2025 (RA-2025, 10 pages).

Réponses attendues : clients actifs fin 2025 (page 2) et portefeuille à risque à
30 jours fin 2025 (page 6). Tous les totaux sont calculés ici, à partir des postes.
"""

from scripts.demo_corpus.facts import (
    ACTIVE_CLIENTS_2025,
    AGENCIES,
    DOCUMENTS,
    PAR30_2025_PCT,
    STAFF_COUNT_2025,
    decimal_fr,
    fmt_int,
    pct,
)
from scripts.demo_corpus.render import (
    Page,
    bullets,
    calculation,
    callout,
    h1,
    h2,
    p,
    table,
    title_block,
)

SPEC = DOCUMENTS[23]
MILLION = 1_000_000

ACTIVE_CLIENTS_2024 = 16_900
CLIENTS_BY_AGENCY = (4_300, 4_100, 3_200, 2_900, 2_300, 1_600)
PAR30_BY_AGENCY = (5.1, 7.9, 6.2, 5.6, 9.4, 8.3)
PAR30_2024 = 5.9

LOANS_2024 = 6_020
LOANS_2025 = 6_850
SAVINGS_2024 = 4_310
SAVINGS_2025 = 4_920
DISBURSED_COUNT = 9_870
DISBURSED_AMOUNT = 8_450

INCOME = (("Produits d'intérêts sur crédits", 1_640), ("Commissions et frais", 210))
EXPENSES = (
    ("Charges financières (intérêts versés)", 260),
    ("Charges de personnel", 540),
    ("Autres charges d'exploitation", 410),
    ("Dotations nettes aux provisions", 230),
    ("Impôt sur le résultat", 120),
)
ASSETS = (
    ("Trésorerie et dépôts bancaires", 1_450),
    ("Crédits à la clientèle, nets de provisions", 6_530),
    ("Immobilisations", 410),
    ("Autres actifs", 160),
)
LIABILITIES = (
    ("Dépôts de la clientèle", 4_920),
    ("Emprunts auprès de partenaires", 1_980),
    ("Autres dettes", 240),
    ("Fonds propres", 1_410),
)


def millions(value: int) -> str:
    """Montant en millions de FCFA."""
    return f"{fmt_int(value)} millions FCFA"


def growth(old: float, new: float) -> str:
    """Taux de croissance en pourcentage, une décimale."""
    return pct(round((new - old) / old * 100, 1))


def net_result() -> int:
    """Résultat net = produits − charges."""
    return sum(v for _, v in INCOME) - sum(v for _, v in EXPENSES)


def build_pages() -> list[Page]:
    """Construit les 10 pages du rapport."""
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6(), _p7(), _p8(), _p9(), _p10()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("Message du Président du Conseil d'administration"),
        p(
            "L'année 2025 a été une année de croissance maîtrisée pour Kouri Épargne & "
            "Crédit. Malgré des inondations qui ont touché plusieurs quartiers de N'Djamena "
            "en fin de saison des pluies et la hausse des prix de certains produits de base, "
            "nos clients ont continué à épargner et à rembourser leurs crédits. Je tiens à "
            "saluer leur confiance, ainsi que l'engagement de tout le personnel."
        ),
        p(
            "Le Conseil a approuvé en décembre une nouvelle grille des taux et frais pour "
            "2026, avec une baisse des taux sur la plupart des crédits, rendue possible par "
            "la maîtrise de nos charges. Il a également renforcé le dispositif de conformité "
            "et la gouvernance, avec la création d'un comité d'audit et des risques."
        ),
        p(
            "La qualité du portefeuille s'est toutefois légèrement dégradée, sous l'effet "
            "des inondations et de difficultés dans le commerce régional. Le Conseil a "
            "demandé à la Direction générale un plan d'action, présenté à la fin du présent "
            "rapport. Notre ambition reste la même : une institution solide, utile et "
            "proche de ses clients."
        ),
        h2("Sommaire"),
        table(
            [
                ["Partie", "Page"],
                ["Chiffres clés de l'année", "2"],
                ["Faits marquants et activité des agences", "3"],
                ["Épargne et crédit", "4 et 5"],
                ["Qualité du portefeuille", "6"],
                ["Résultats financiers et bilan", "7 et 8"],
                ["Ressources humaines, gouvernance, conformité", "9"],
                ["Perspectives 2026", "10"],
            ],
            (0.8, 0.2),
        ),
        h2("Mot du Directeur général"),
        p(
            "Les équipes ont fait preuve d'un engagement remarquable pendant la période "
            "des inondations, en maintenant l'ouverture des agences et en accompagnant "
            "les clients sinistrés. Je les en remercie."
        ),
    ]


def _p2() -> Page:
    new_clients = ACTIVE_CLIENTS_2025 - ACTIVE_CLIENTS_2024
    return [
        h1("1. Chiffres clés de l'année 2025"),
        p(
            f"Au 31 décembre 2025, l'institution comptait {fmt_int(ACTIVE_CLIENTS_2025)} "
            f"clients actifs, soit {fmt_int(new_clients)} de plus qu'un an plus tôt "
            f"({growth(ACTIVE_CLIENTS_2024, ACTIVE_CLIENTS_2025)}). Un client actif est un "
            "client qui a effectué au moins une opération au cours des douze derniers mois "
            "ou qui a un crédit en cours."
        ),
        table(
            [
                ["Indicateur", "Fin 2024", "Fin 2025", "Évolution"],
                [
                    "Encours de crédit",
                    millions(LOANS_2024),
                    millions(LOANS_2025),
                    growth(LOANS_2024, LOANS_2025),
                ],
                [
                    "Épargne de la clientèle",
                    millions(SAVINGS_2024),
                    millions(SAVINGS_2025),
                    growth(SAVINGS_2024, SAVINGS_2025),
                ],
                ["Crédits décaissés dans l'année", "—", fmt_int(DISBURSED_COUNT), "—"],
                ["Montant décaissé dans l'année", "—", millions(DISBURSED_AMOUNT), "—"],
                ["Résultat net", "—", millions(net_result()), "—"],
                ["Effectif salarié", "—", str(STAFF_COUNT_2025), "—"],
            ],
            (0.34, 0.22, 0.22, 0.22),
        ),
        h2("Lecture des chiffres"),
        p(
            "L'épargne a progressé plus vite que le crédit, ce qui renforce l'autonomie "
            "financière de l'institution : une part croissante des crédits est financée "
            "par les dépôts des clients plutôt que par des emprunts. Le nombre de crédits "
            "décaissés reflète la forte demande des petits commerçants et des groupements."
        ),
        h2("Profil des clients"),
        *bullets(
            [
                "Près de deux clients sur trois sont des femmes, en majorité commerçantes.",
                "Les groupements solidaires représentent un emprunteur sur trois.",
                "Les clients des agences de Moundou et d'Abéché sont plus souvent agriculteurs "
                "ou éleveurs.",
            ]
        ),
        h2("Satisfaction des clients"),
        p(
            "Une enquête menée auprès d'un échantillon de clients dans toutes les agences"
            " montre une satisfaction élevée sur l'accueil et la rapidité des opérations "
            "de caisse. Les attentes portent surtout sur la rapidité de réponse aux "
            "demandes de crédit."
        ),
        h2("Inclusion financière"),
        p(
            "Une part importante des nouveaux clients ouvrait son premier compte dans une"
            " institution financière. Les groupements solidaires restent la principale "
            "porte d'entrée des femmes commerçantes vers le crédit."
        ),
        h2("Méthode"),
        p(
            "Les chiffres de ce rapport proviennent du logiciel de gestion et des états "
            "financiers certifiés. Les montants sont arrondis au million de francs CFA."
        ),
    ]


def _p3() -> Page:
    rows = [["Agence", "Clients actifs fin 2025"]]
    rows += [[name, fmt_int(n)] for name, n in zip(AGENCIES, CLIENTS_BY_AGENCY, strict=True)]
    return [
        h1("2. Faits marquants de l'année"),
        table(
            [
                ["Période", "Événement"],
                ["1er trimestre", "Déploiement des tablettes de collecte dans toutes les agences"],
                ["2e trimestre", "Refonte de la charte informatique et des procédures de caisse"],
                [
                    "3e trimestre",
                    "Inondations dans plusieurs quartiers de N'Djamena ; "
                    "suspension temporaire des relances pour les clients sinistrés",
                ],
                [
                    "4e trimestre",
                    "Création du comité d'audit et des risques ; approbation "
                    "de la grille tarifaire 2026",
                ],
            ],
            (0.2, 0.8),
        ),
        h1("3. Activité des agences"),
        table(rows, (0.6, 0.4)),
        p(
            "Les agences de N'Djamena concentrent l'essentiel de la clientèle. L'agence du "
            "Grand Marché reste la plus active en nombre d'opérations de caisse. Les agences "
            "de Moundou et d'Abéché progressent régulièrement, portées par le crédit "
            "agricole et le commerce du bétail."
        ),
        h2("Opérations de caisse"),
        p(
            "Les agences ont traité environ deux mille opérations de caisse par jour "
            "ouvrable en moyenne. Le temps d'attente moyen au guichet a diminué grâce à "
            "l'ouverture d'un guichet supplémentaire dans deux agences de N'Djamena."
        ),
        h2("Réseau"),
        p(
            "Aucune nouvelle agence n'a été ouverte en 2025 : la priorité a été donnée à "
            "la qualité du service dans les six agences existantes et à l'équipement des "
            "agents de crédit."
        ),
        h2("Sinistres"),
        p(
            "Les inondations ont contraint l'agence Chagoua à fermer pendant deux jours. "
            "Ses clients ont été servis à l'agence Centre, conformément au plan de "
            "continuité d'activité."
        ),
    ]


def _p4() -> Page:
    return [
        h1("4. Épargne"),
        p(
            f"L'épargne de la clientèle atteint {millions(SAVINGS_2025)} à la fin de "
            f"l'année, en hausse de {growth(SAVINGS_2024, SAVINGS_2025)}. La progression "
            "vient surtout des dépôts à terme, qui attirent les commerçants souhaitant "
            "placer leur trésorerie en dehors des périodes d'achat."
        ),
        table(
            [
                ["Produit", "Encours fin 2025", "Part"],
                ["Comptes courants", millions(1_720), "35 %"],
                ["Livrets d'épargne", millions(1_330), "27 %"],
                ["Dépôts à terme", millions(1_480), "30 %"],
                ["Épargne de garantie des crédits", millions(390), "8 %"],
                ["Total", millions(SAVINGS_2025), "100 %"],
            ],
            (0.45, 0.33, 0.22),
        ),
        h2("Calcul de vérification"),
        *calculation(
            [
                ("Comptes courants + livrets", millions(1_720 + 1_330)),
                ("Dépôts à terme + épargne de garantie", millions(1_480 + 390)),
                ("Total = ligne 1 + ligne 2", millions(1_720 + 1_330 + 1_480 + 390)),
            ],
            "Étape du calcul",
        ),
        h2("Rémunération versée"),
        p(
            "Les intérêts versés aux épargnants figurent dans les charges financières "
            "(page 7). Les taux appliqués sont ceux du catalogue des produits d'épargne "
            "(voir EP-CAT-01)."
        ),
        h2("Dépôts à terme"),
        p(
            "Le succès des dépôts à terme montre que les commerçants recherchent un "
            "placement sûr pour leur trésorerie saisonnière. Les durées de six et douze "
            "mois sont les plus demandées."
        ),
        h2("Livrets"),
        p(
            "Le nombre de livrets d'épargne a progressé régulièrement, notamment grâce "
            "aux livrets ouverts au nom d'enfants par leurs parents."
        ),
        h2("Concentration des dépôts"),
        p(
            "Les vingt plus gros déposants représentent une part limitée de l'épargne "
            "totale, ce qui réduit le risque de retraits importants et simultanés."
        ),
        h2("Épargne et crédit"),
        p(
            "Le rapport entre l'épargne collectée et l'encours de crédit s'est amélioré :"
            " les dépôts des clients financent désormais une part plus importante des "
            "crédits accordés."
        ),
    ]


def _p5() -> Page:
    average = round(DISBURSED_AMOUNT * MILLION / DISBURSED_COUNT)
    return [
        h1("5. Crédit"),
        p(
            f"L'encours de crédit atteint {millions(LOANS_2025)}, en hausse de "
            f"{growth(LOANS_2024, LOANS_2025)}. L'institution a décaissé "
            f"{fmt_int(DISBURSED_COUNT)} crédits pour un montant total de "
            f"{millions(DISBURSED_AMOUNT)}."
        ),
        *calculation(
            [
                ("Montant décaissé dans l'année", millions(DISBURSED_AMOUNT)),
                ("Nombre de crédits décaissés", fmt_int(DISBURSED_COUNT)),
                ("Montant moyen = ligne 1 ÷ ligne 2", f"{fmt_int(average)} FCFA"),
            ],
            "Étape du calcul",
        ),
        table(
            [
                ["Produit", "Part de l'encours fin 2025"],
                ["Crédit AGR", "48 %"],
                ["Crédit solidaire aux groupements", "21 %"],
                ["Crédit équipement", "14 %"],
                ["Crédit agricole de campagne", "11 %"],
                ["Crédit scolaire", "6 %"],
            ],
            (0.65, 0.35),
        ),
        h2("Analyse"),
        p(
            "Le crédit pour activité génératrice de revenus reste le cœur de l'activité. Le "
            "crédit solidaire progresse fortement grâce aux groupements de femmes "
            "commerçantes. Le crédit agricole a été pénalisé par une saison des pluies "
            "irrégulière dans le sud du pays."
        ),
        h2("Montants moyens"),
        p(
            "Le montant moyen des crédits reste modeste, conformément à la mission de "
            "l'institution : financer des activités de petite taille, avec des montants "
            "qui augmentent cycle après cycle."
        ),
        h2("Délais de décision"),
        p(
            "Le délai moyen entre le dépôt d'un dossier complet et la décision s'est "
            "réduit, grâce à la tenue hebdomadaire des comités d'agence."
        ),
        h2("Renouvellements"),
        p(
            "La majorité des crédits décaissés sont des renouvellements accordés à des "
            "clients ayant remboursé un précédent crédit sans incident, signe de la "
            "fidélité de la clientèle."
        ),
        h2("Crédit agricole"),
        p(
            "Les crédits agricoles accordés avant une saison des pluies irrégulière ont "
            "été suivis de près ; plusieurs ont été rééchelonnés après constat des pertes"
            " de récolte, conformément à la politique de crédit."
        ),
    ]


def _p6() -> Page:
    rows = [["Agence", "PAR 30 fin 2025"]]
    rows += [[name, pct(v)] for name, v in zip(AGENCIES, PAR30_BY_AGENCY, strict=True)]
    return [
        h1("6. Qualité du portefeuille"),
        p(
            "Le portefeuille à risque à 30 jours (PAR 30) mesure la part de l'encours de "
            "crédit dont au moins une échéance est impayée depuis plus de 30 jours. Fin "
            f"2025, le PAR 30 s'établissait à {pct(PAR30_2025_PCT)}, contre "
            f"{pct(PAR30_2024)} un an plus tôt."
        ),
        table(rows, (0.6, 0.4)),
        h2("Causes de la dégradation"),
        *bullets(
            [
                "Les inondations du 3e trimestre ont endommagé les stocks de nombreux "
                "commerçants dans les quartiers touchés.",
                "Le commerce régional a souffert de difficultés de transport vers Moundou "
                "et Abéché.",
                "Quelques groupements solidaires constitués trop rapidement ont connu des "
                "défauts en chaîne.",
            ]
        ),
        h2("Mesures prises"),
        p(
            "Un calendrier de relance renforcé a été adopté (voir CR-PRO-04), les "
            "formations des agents de crédit à l'analyse de la capacité de remboursement ont "
            "été intensifiées, et la constitution des nouveaux groupements est désormais "
            "validée par le chef d'agence après une visite de reconnaissance."
        ),
        h2("Passages en perte"),
        p(
            "Les crédits passés en perte au cours de l'année restent limités et ont été "
            "approuvés par le comité du siège. Le recouvrement se poursuit sur ces "
            "dossiers lorsque c'est possible."
        ),
        h2("Provisions"),
        p(
            "Les provisions constituées couvrent la totalité des crédits classés "
            "compromis et une part des crédits douteux, conformément aux règles "
            "prudentielles."
        ),
        h2("Suivi par agence"),
        p(
            "L'agence de Moundou, la plus touchée par les retards, fait l'objet d'un plan"
            " spécifique : visites conjointes du chef d'agence et de la Direction du "
            "crédit, et révision des dossiers de crédit agricole."
        ),
    ]


def _p7() -> Page:
    lines = [(label, millions(v)) for label, v in INCOME]
    lines.append(("Total des produits = lignes 1 + 2", millions(sum(v for _, v in INCOME))))
    lines += [(label, f"− {millions(v)}") for label, v in EXPENSES]
    lines.append(("Résultat net = ligne 3 − lignes 4 à 8", millions(net_result())))
    return [
        h1("7. Résultats financiers"),
        p(
            "Le compte de résultat simplifié ci-dessous présente les principaux produits et "
            "charges de l'exercice, en millions de francs CFA. Le résultat net est calculé "
            "ligne par ligne."
        ),
        *calculation(lines, "Poste du compte de résultat"),
        h2("Commentaires"),
        p(
            "Les produits d'intérêts progressent avec l'encours de crédit. Les dotations aux "
            "provisions augmentent sensiblement, en raison de la dégradation du portefeuille "
            "décrite en page 6. Les charges de personnel reflètent les recrutements de "
            "l'année et la nouvelle grille salariale."
        ),
        h2("Rentabilité"),
        p(
            f"Rapporté aux fonds propres de fin d'année ({millions(LIABILITIES[3][1])}), le "
            "résultat net représente une rentabilité de "
            f"{pct(round(net_result() / LIABILITIES[3][1] * 100, 1))}."
        ),
        h2("Charges d'exploitation"),
        p(
            "Les autres charges d'exploitation comprennent les loyers, l'énergie, le "
            "carburant des groupes électrogènes, la maintenance informatique, le "
            "transport de fonds et les assurances."
        ),
        h2("Efficacité"),
        p(
            "Le coût de fonctionnement rapporté à l'encours de crédit est resté stable, "
            "malgré les recrutements de l'année, grâce aux gains de productivité apportés"
            " par les tablettes de collecte."
        ),
        h2("Fiscalité"),
        p(
            "L'impôt sur le résultat a été calculé et versé conformément à la "
            "réglementation fiscale applicable."
        ),
    ]


def _p8() -> Page:
    assets = sum(v for _, v in ASSETS)
    liabilities = sum(v for _, v in LIABILITIES)
    equity_ratio = round(LIABILITIES[3][1] / assets * 100, 1)
    return [
        h1("8. Bilan simplifié au 31 décembre 2025"),
        table(
            [
                ["Actif", "Millions FCFA"],
                *[[label, fmt_int(v)] for label, v in ASSETS],
                ["Total de l'actif", fmt_int(assets)],
            ],
            (0.7, 0.3),
        ),
        table(
            [
                ["Passif", "Millions FCFA"],
                *[[label, fmt_int(v)] for label, v in LIABILITIES],
                ["Total du passif", fmt_int(liabilities)],
            ],
            (0.7, 0.3),
        ),
        h2("Ratios prudentiels"),
        *calculation(
            [
                ("Fonds propres", millions(LIABILITIES[3][1])),
                ("Total de l'actif", millions(assets)),
                ("Fonds propres ÷ actif = ligne 1 ÷ ligne 2", pct(equity_ratio)),
            ],
            "Étape du calcul",
        ),
        p(
            "Les ratios prudentiels fixés par la réglementation applicable aux "
            "établissements de microfinance ont été respectés tout au long de l'exercice."
        ),
        h2("Liquidité"),
        p(
            "La trésorerie disponible couvre une part confortable des dépôts à vue de la "
            "clientèle, ce qui permet de faire face à des retraits importants sans "
            "difficulté."
        ),
        h2("Financements extérieurs"),
        p(
            "Les emprunts auprès de partenaires financent la croissance du crédit. Leur "
            "part dans le financement total diminue au profit des dépôts de la clientèle."
        ),
        h2("Évolution du bilan"),
        p(
            "Le total du bilan progresse avec l'activité. La hausse des crédits à la "
            "clientèle est financée principalement par l'augmentation des dépôts et par "
            "le résultat mis en réserve."
        ),
    ]


def _p9() -> Page:
    return [
        h1("9. Ressources humaines"),
        p(
            f"L'effectif atteint {STAFF_COUNT_2025} salariés à la fin de l'année, dont une "
            "majorité en agence. Les recrutements ont porté principalement sur des agents de "
            "crédit et des caissiers. Une nouvelle grille salariale a été préparée et "
            "approuvée pour une application au début de 2026."
        ),
        table(
            [
                ["Fonction", "Part de l'effectif"],
                ["Agents de crédit", "38 %"],
                ["Caisse et accueil", "29 %"],
                ["Encadrement des agences", "10 %"],
                ["Services du siège", "23 %"],
            ],
            (0.65, 0.35),
        ),
        h2("Formation"),
        p(
            "Le personnel a suivi les formations prévues au plan de formation de l'année, "
            "dont la formation anti-blanchiment pour l'ensemble des salariés et la "
            "formation à l'analyse de la capacité de remboursement pour les agents de "
            "crédit."
        ),
        h2("Égalité professionnelle"),
        p(
            "Les femmes représentent une part croissante de l'encadrement des agences. "
            "Deux nouvelles cheffes d'agence ont été nommées au cours de l'année."
        ),
        h1("10. Gouvernance et contrôle"),
        p(
            "Le Conseil d'administration s'est réuni quatre fois en session ordinaire. Il a "
            "créé un comité d'audit et des risques, adopté la politique de rémunération "
            "révisée et approuvé la grille tarifaire 2026. L'audit interne a contrôlé "
            "toutes les agences au cours de l'année."
        ),
        h1("11. Conformité"),
        p(
            "Le dispositif de lutte anti-blanchiment a été renforcé : filtrage des "
            "transferts, suivi des opérations fractionnées, révision des dossiers des "
            "clients à risque élevé. L'ensemble du personnel a été formé. Le rapport annuel "
            "de la conformité a été présenté au comité d'audit et des risques."
        ),
        h2("Audit interne"),
        p(
            "Les missions d'audit ont porté sur la caisse, le crédit et la sécurité "
            "informatique. Les recommandations font l'objet d'un suivi trimestriel par le"
            " comité d'audit et des risques."
        ),
        h2("Effectif par site"),
        p(
            "Les agences regroupent la majorité du personnel. Les services du siège ont "
            "été renforcés en conformité et en informatique pour accompagner la "
            "croissance de l'activité."
        ),
    ]


def _p10() -> Page:
    reserve = round(net_result() * 0.2)
    return [
        h1("12. Perspectives 2026"),
        *bullets(
            [
                "Ramener le PAR 30 sous 5 % grâce au plan d'action sur la qualité du portefeuille.",
                "Appliquer la nouvelle grille des taux et frais, plus favorable aux clients.",
                "Lancer le plan d'épargne projet dans toutes les agences.",
                "Former chaque salarié selon le plan de formation de l'année.",
                "Expérimenter un assistant documentaire interne fonctionnant entièrement "
                "en local, pour faciliter l'accès des équipes aux procédures.",
            ]
        ),
        h2("Investissements prévus"),
        p(
            "L'institution prévoit de renouveler une partie des groupes électrogènes, de "
            "renforcer la sécurité informatique et d'équiper les agences de nouveaux "
            "détecteurs de faux billets."
        ),
        h2("Engagement envers les clients"),
        p(
            "En 2026, l'institution poursuivra sa mission avec la même exigence : des "
            "services accessibles, des conditions claires, et un accompagnement de chaque "
            "client dans la durée."
        ),
        h1("13. Affectation du résultat"),
        *calculation(
            [
                ("Résultat net de l'exercice", millions(net_result())),
                (
                    f"Réserve légale et statutaire = ligne 1 × {decimal_fr(0.2, 1)}",
                    millions(reserve),
                ),
                ("Report à nouveau = ligne 1 − ligne 2", millions(net_result() - reserve)),
            ],
            "Proposition à l'Assemblée générale",
        ),
        p(
            "Le Conseil propose de ne pas distribuer de dividende cette année et de "
            "renforcer les fonds propres de l'institution."
        ),
        h1("14. Rapport du commissaire aux comptes"),
        p(
            "Le commissaire aux comptes a certifié que les états financiers de l'exercice "
            "2025 sont réguliers et sincères et donnent une image fidèle du résultat, de la "
            "situation financière et du patrimoine de l'institution. Il n'a formulé aucune "
            "réserve ; ses observations sur le suivi des crédits agricoles ont été reprises "
            "dans le plan d'action de la Direction générale."
        ),
        callout(
            "Remerciements",
            [
                "Le Conseil remercie les clients, les partenaires financiers et l'ensemble "
                "du personnel pour leur contribution aux résultats de l'année.",
            ],
        ),
    ]
