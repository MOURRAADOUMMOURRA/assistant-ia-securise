"""Document n° 10 — Politique et procédure d'octroi de crédit (CR-PRO-01, 10 pages).

Réponses attendues : plafond d'un premier crédit (page 4) et mensualité maximale
en part du revenu net mensuel (page 6). Les taux, frais et plafonds d'autorisation
ne sont pas recopiés : le document renvoie à TAR-2026 et à CR-PRO-02.
"""

from scripts.demo_corpus.facts import (
    DOCUMENTS,
    FIRST_LOAN_CAP_FCFA,
    MAX_INSTALLMENT_RATIO_PCT,
    DocumentSpec,
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

SPEC: DocumentSpec = DOCUMENTS[10]

# Exemple de capacité de remboursement (page 6) : montants mensuels en FCFA.
SALES = 950_000
PURCHASES = 610_000
MARKET_FEES = 35_000
TRANSPORT = 45_000
OTHER_INCOME = 25_000
CURRENT_INSTALLMENTS = 30_000

# Exemple de renouvellement (page 4).
PREVIOUS_LOAN = 400_000
SECOND_LOAN_FACTOR = 1.5


def build_pages() -> list[Page]:
    """Construit les 10 pages du document."""
    return [
        _page_1(),
        _page_2(),
        _page_3(),
        _page_4(),
        _page_5(),
        _page_6(),
        _page_7(),
        _page_8(),
        _page_9(),
        _page_10(),
    ]


def _page_1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "La présente politique fixe les règles suivies par Kouri Épargne & Crédit pour "
            "accorder un crédit : qui peut emprunter, pour quel montant, avec quelles pièces, "
            "comment la capacité de remboursement est analysée et qui décide. Elle poursuit "
            "trois objectifs : servir durablement les micro-entrepreneurs de nos zones "
            "d'intervention, protéger l'épargne des membres en limitant le risque d'impayés, "
            "et garantir à chaque demandeur un traitement égal, écrit et motivé."
        ),
        h1("2. Champ d'application"),
        p(
            "Elle s'applique à tous les crédits individuels accordés par les agences et par le "
            "siège : crédit pour activité génératrice de revenus (AGR), crédit équipement, "
            "crédit agricole de campagne et crédit scolaire. Le crédit solidaire aux "
            "groupements suit en plus sa procédure propre (voir CR-PRO-03). Les prêts au "
            "personnel relèvent de la politique de rémunération (voir RH-POL-04) et ne sont "
            "pas traités ici."
        ),
        p(
            "Elle s'impose aux agents de crédit, aux chefs d'agence, aux membres du comité de "
            "crédit, aux caissiers et au contrôle interne. Toute dérogation doit être "
            "demandée par écrit et accordée par le niveau d'autorisation supérieur à celui "
            "qui aurait normalement décidé."
        ),
        h1("3. Documents de référence"),
        table(
            [
                ["Référence", "Document", "Ce qu'on y trouve"],
                [
                    "CR-PRO-02",
                    "Comité de crédit et plafonds d'autorisation",
                    "Qui décide, selon le montant du crédit",
                ],
                [
                    "CR-PRO-03",
                    "Crédit solidaire aux groupements",
                    "Règles propres aux prêts de groupe",
                ],
                ["CR-PRO-04", "Recouvrement des impayés", "Conduite à tenir en cas de retard"],
                [
                    "TAR-2026",
                    "Grille des taux et frais 2026",
                    "Taux d'intérêt, frais de dossier, assurance, exemple de mensualité",
                ],
                [
                    "CONF-POL-01",
                    "Connaissance client (KYC) et lutte anti-blanchiment",
                    "Identification du client et devoir de vigilance",
                ],
                [
                    "OP-PRO-01",
                    "Procédure d'ouverture de compte",
                    "Pièces d'identité et ouverture du compte",
                ],
            ],
            (0.16, 0.42, 0.42),
        ),
        callout(
            "Règle d'or",
            [
                "Aucun crédit n'est décaissé sans dossier complet, sans analyse écrite de la "
                "capacité de remboursement et sans décision signée par le niveau "
                "d'autorisation compétent."
            ],
        ),
    ]


def _page_2() -> Page:
    return [
        h1("4. Principes généraux"),
        *bullets(
            [
                "**Connaissance du client.** L'agent rencontre le demandeur, visite son "
                "activité et vérifie son identité avant toute analyse (voir CONF-POL-01).",
                "**Capacité avant garantie.** Un crédit est accordé parce que le client peut le "
                "rembourser avec ses revenus, jamais parce qu'une garantie couvre le risque.",
                "**Séparation des fonctions.** L'agent qui instruit un dossier ne le décide pas "
                "seul ; le caissier qui décaisse n'a pas instruit le dossier.",
                "**Transparence.** Avant la signature, le client reçoit par écrit le tableau "
                "d'amortissement, le coût total du crédit et la liste des frais.",
                "**Progressivité.** Le montant accordé augmente avec l'historique de "
                "remboursement du client, cycle après cycle (section 7).",
                "**Non-discrimination.** Aucune décision ne repose sur l'ethnie, la religion, "
                "le sexe ou l'appartenance politique du demandeur.",
            ]
        ),
        h1("5. Produits couverts et définitions"),
        table(
            [
                ["Produit", "Public visé", "Remboursement"],
                [
                    "Crédit AGR",
                    "Commerçants, artisans, prestataires de services",
                    "Mensualités constantes",
                ],
                [
                    "Crédit équipement",
                    "Entrepreneurs ayant au moins un cycle remboursé",
                    "Mensualités constantes",
                ],
                [
                    "Crédit agricole de campagne",
                    "Producteurs et coopératives agricoles",
                    "En une ou deux échéances après la récolte",
                ],
                [
                    "Crédit scolaire",
                    "Parents d'élèves salariés ou commerçants",
                    "Mensualités constantes",
                ],
            ],
            (0.27, 0.43, 0.30),
        ),
        p(
            "Les taux et les frais de chaque produit ne figurent pas dans la présente "
            "politique : ils sont fixés chaque année par la grille des taux et frais en "
            "vigueur (voir TAR-2026). En cas de doute, l'agent consulte toujours la grille la "
            "plus récente et ne s'appuie jamais sur un tarif retenu de mémoire."
        ),
        table(
            [
                ["Terme", "Définition"],
                [
                    "Premier crédit",
                    "Tout crédit accordé à un client qui n'a jamais emprunté chez "
                    "Kouri, ou dont le dernier crédit a été soldé depuis plus de 24 mois.",
                ],
                [
                    "Revenu net mensuel",
                    "Revenu de l'activité après déduction des charges "
                    "d'exploitation, augmenté des autres revenus réguliers et justifiés.",
                ],
                ["Mensualité", "Somme du capital et des intérêts remboursés chaque mois."],
                ["Cycle", "Un crédit intégralement remboursé, du décaissement au solde."],
                [
                    "Plan de financement",
                    "Tableau qui présente le besoin, l'apport du client et le montant demandé.",
                ],
            ],
            (0.25, 0.75),
        ),
    ]


def _page_3() -> Page:
    return [
        h1("6. Conditions d'éligibilité"),
        p(
            "Une demande n'est instruite que si toutes les conditions ci-dessous sont remplies. "
            "L'agent les vérifie dès le premier entretien, avant la visite de l'activité, pour "
            "ne pas faire attendre inutilement un demandeur qui ne pourrait pas être financé."
        ),
        table(
            [
                ["Condition", "Exigence", "Justificatif"],
                [
                    "Capacité juridique",
                    "Être majeur et juridiquement capable",
                    "Pièce d'identité (voir OP-PRO-01)",
                ],
                [
                    "Compte",
                    "Détenir un compte actif chez Kouri depuis au moins deux mois",
                    "Historique du compte dans le logiciel",
                ],
                [
                    "Activité",
                    "Exercer l'activité financée depuis au moins 12 mois",
                    "Visite sur place, carnet de ventes, voisins de marché",
                ],
                [
                    "Zone",
                    "Résider ou travailler dans la zone d'intervention de l'agence",
                    "Facture d'eau ou d'électricité, contrat de bail",
                ],
                [
                    "Épargne préalable",
                    "Avoir constitué une épargne égale à 10 % du montant demandé",
                    "Solde du compte d'épargne",
                ],
                [
                    "Endettement",
                    "Aucun crédit en cours ailleurs sans déclaration écrite",
                    "Déclaration sur l'honneur, centrale des risques",
                ],
                [
                    "Antécédents",
                    "Aucun impayé non régularisé chez Kouri",
                    "Historique de crédit dans le logiciel",
                ],
            ],
            (0.2, 0.43, 0.37),
        ),
        h2("Cas d'exclusion"),
        *bullets(
            [
                "Activités illicites ou contraires à la réglementation, ainsi que le change "
                "informel de devises.",
                "Remboursement d'une dette contractée ailleurs (rachat de crédit), sauf "
                "rééchelonnement approuvé chez Kouri (section 12).",
                "Demande présentée par un membre du comité qui statue, ou par un de ses parents "
                "jusqu'au deuxième degré : le membre concerné se retire de la séance.",
                "Demandeur inscrit sur une liste de sanctions ou présentant un risque élevé non "
                "levé par la conformité (voir CONF-POL-01).",
            ]
        ),
        h2("Vérification de l'endettement"),
        p(
            "L'agent interroge la centrale des risques lorsque la consultation est possible et "
            "fait signer la déclaration sur l'honneur dans tous les cas. Un crédit en cours "
            "dans une autre institution n'est pas un motif de refus en soi : ses mensualités "
            "sont simplement ajoutées dans l'analyse de la capacité de remboursement."
        ),
        callout(
            "Bon à savoir",
            [
                "Un refus pour non-éligibilité est toujours motivé par écrit et remis au "
                "demandeur. Celui-ci peut déposer une nouvelle demande dès que la condition "
                "manquante est remplie : il n'y a pas de délai de carence.",
                "L'épargne préalable reste la propriété du client. Elle est bloquée en garantie "
                "pendant la durée du crédit, puis libérée au remboursement complet.",
            ],
        ),
    ]


def _page_4() -> Page:
    second_loan = round(PREVIOUS_LOAN * SECOND_LOAN_FACTOR)
    return [
        h1("7. Montants et durées"),
        h2("7.1 Premier crédit"),
        p(
            f"Pour un premier crédit, le montant maximal accordé est de "
            f"{fcfa(FIRST_LOAN_CAP_FCFA)}, quel que soit le produit (hors crédit solidaire, "
            "voir CR-PRO-03). Ce plafond protège le client autant que l'institution : il permet "
            "de vérifier, sur un premier cycle, que l'activité dégage réellement le revenu "
            "déclaré. La durée d'un premier crédit ne dépasse pas 12 mois."
        ),
        h2("7.2 Crédits suivants (renouvellement)"),
        p(
            "À chaque nouveau cycle, le montant peut augmenter si le client a remboursé sans "
            "incident. L'augmentation n'est jamais automatique : elle reste soumise à "
            "l'analyse de la capacité de remboursement (section 9)."
        ),
        table(
            [
                ["Cycle", "Montant maximal", "Condition"],
                [
                    "2e crédit",
                    "150 % du montant du crédit précédent",
                    "Aucun retard de plus de 10 jours sur le cycle précédent",
                ],
                [
                    "3e crédit",
                    "200 % du montant du crédit précédent",
                    "Même condition, et visite de suivi favorable",
                ],
                [
                    "4e crédit et suivants",
                    "Selon la capacité de remboursement",
                    "Aucun incident sur les deux derniers cycles ; plafonds de CR-PRO-02",
                ],
            ],
            (0.2, 0.35, 0.45),
        ),
        p(
            f"Exemple : un client a remboursé sans incident un premier crédit de "
            f"{fcfa(PREVIOUS_LOAN)}. Son deuxième crédit peut atteindre "
            f"{fmt_int(PREVIOUS_LOAN)} × {decimal_fr(SECOND_LOAN_FACTOR, 1)} = "
            f"{fcfa(second_loan)}, à condition que sa capacité de remboursement le permette."
        ),
        h2("7.3 Durées maximales"),
        table(
            [
                ["Produit", "Durée maximale", "Différé de remboursement possible"],
                ["Crédit AGR", "18 mois", "1 mois au plus"],
                ["Crédit équipement", "24 mois", "2 mois au plus"],
                ["Crédit agricole de campagne", "10 mois", "Jusqu'à la récolte"],
                ["Crédit scolaire", "9 mois", "Aucun"],
            ],
            (0.34, 0.24, 0.42),
        ),
        h2("7.4 Montant minimal et arrondi"),
        p(
            f"Aucun crédit individuel n'est accordé pour moins de {fcfa(50_000)} : en dessous, "
            "les frais de gestion deviennent disproportionnés pour le client. Les montants "
            f"accordés sont arrondis au multiple de {fcfa(5_000)} inférieur, afin de simplifier "
            "le tableau d'amortissement et les versements au guichet."
        ),
        callout(
            "Attention",
            [
                "Le montant accordé ne dépasse jamais le besoin réel justifié par le plan de "
                "financement, même si le plafond du cycle le permettrait. Un crédit trop "
                "important pour l'activité est la première cause de surendettement.",
                "Le plafond d'un cycle est un maximum, pas un droit : le client n'a aucune "
                "garantie d'obtenir ce montant s'il ne correspond pas à sa capacité.",
            ],
        ),
    ]


def _page_5() -> Page:
    return [
        h1("8. Constitution du dossier"),
        p(
            "L'agent de crédit constitue le dossier avec le client lors du premier entretien, "
            "puis le complète après la visite de l'activité. Il utilise la liste ci-dessous "
            "comme liste de contrôle et coche chaque pièce reçue."
        ),
        h2("Points à aborder lors du premier entretien"),
        *bullets(
            [
                "L'objet précis du crédit et le calendrier des dépenses prévues.",
                "Le fonctionnement de l'activité : fournisseurs, clients, saisonnalité, stock.",
                "Les charges du ménage et les autres sources de revenus du foyer.",
                "Les crédits en cours, y compris auprès de tontines ou de commerçants.",
                "Le coût total du crédit et les conséquences d'un retard de paiement.",
            ]
        ),
        table(
            [
                ["Pièce", "Obligatoire", "Remarque"],
                ["Formulaire de demande signé", "Oui", "Modèle F-CR-01"],
                ["Pièce d'identité et justificatifs KYC", "Oui", "Voir OP-PRO-01 et CONF-POL-01"],
                ["Plan de financement", "Oui", "Besoin, apport du client, montant demandé"],
                [
                    "Fiche de visite de l'activité",
                    "Oui",
                    "Avec photos du stock ou du local, si le client l'accepte",
                ],
                [
                    "Carnet ou relevés de ventes des 3 derniers mois",
                    "Oui",
                    "À défaut, reconstitution des ventes par l'agent",
                ],
                [
                    "Justificatifs des autres revenus",
                    "Si déclarés",
                    "Bulletin de salaire, contrat de location",
                ],
                ["Documents de garantie", "Selon le montant", "Voir section 10"],
                ["Déclaration sur l'honneur d'endettement", "Oui", "Modèle F-CR-02"],
            ],
            (0.42, 0.16, 0.42),
        ),
        h2("Délais de traitement"),
        p(
            "Un dossier complet est instruit sous 5 jours ouvrables à compter de sa réception. "
            "Le client est informé de la décision au plus tard 2 jours ouvrables après la "
            "séance du niveau compétent. Un dossier incomplet n'est pas présenté : l'agent "
            "remet au client la liste des pièces manquantes, datée et signée."
        ),
        h2("Contrôle qualité du dossier"),
        *bullets(
            [
                "Le chef d'agence vérifie la complétude et la cohérence du dossier avant toute "
                "présentation pour décision.",
                "Les montants du plan de financement, de la fiche de visite et de l'analyse "
                "doivent concorder ; tout écart est expliqué par écrit.",
                "Le dossier physique et sa copie numérique sont archivés à l'agence ; aucune "
                "pièce originale du client n'est conservée, seulement des copies.",
            ]
        ),
        h2("Demande déposée par un tiers"),
        p(
            "Une demande ne peut pas être déposée par un intermédiaire rémunéré. Un proche peut "
            "apporter des pièces, mais l'entretien, la visite et la signature se font toujours "
            "en présence du demandeur lui-même. Toute sollicitation d'argent par une personne "
            "se présentant comme « facilitateur » est signalée au chef d'agence."
        ),
    ]


def _page_6() -> Page:
    activity_income = SALES - PURCHASES - MARKET_FEES - TRANSPORT
    net_income = activity_income + OTHER_INCOME
    ratio = MAX_INSTALLMENT_RATIO_PCT / 100
    max_installment = round(net_income * ratio)
    available = max_installment - CURRENT_INSTALLMENTS
    return [
        h1("9. Analyse de la capacité de remboursement"),
        p(
            "La mensualité de l'ensemble des crédits du client, y compris celui demandé, ne "
            f"doit pas dépasser {pct(MAX_INSTALLMENT_RATIO_PCT)} du revenu net mensuel. "
            "Le reste du revenu couvre les dépenses du ménage et les imprévus. Le revenu est "
            "établi à partir du carnet de ventes et de la visite, jamais sur la seule "
            "déclaration du client."
        ),
        h2("Exemple chiffré : une commerçante de pagnes au marché"),
        *calculation(
            [
                ("Recettes mensuelles moyennes, relevées dans le carnet de ventes", fcfa(SALES)),
                ("Achats de marchandises du mois", f"− {fcfa(PURCHASES)}"),
                ("Loyer de l'étal et taxes de marché", f"− {fcfa(MARKET_FEES)}"),
                ("Transport et frais divers", f"− {fcfa(TRANSPORT)}"),
                ("Revenu net de l'activité = ligne 1 − lignes 2, 3 et 4", fcfa(activity_income)),
                (
                    "Autres revenus réguliers justifiés (location d'une pièce)",
                    f"+ {fcfa(OTHER_INCOME)}",
                ),
                ("Revenu net mensuel = ligne 5 + ligne 6", fcfa(net_income)),
                (
                    f"Mensualité maximale = ligne 7 × {decimal_fr(ratio, 2)} (ratio ci-dessus)",
                    fcfa(max_installment),
                ),
                ("Mensualités des crédits déjà en cours", f"− {fcfa(CURRENT_INSTALLMENTS)}"),
                (
                    "Mensualité disponible pour le nouveau crédit = ligne 8 − ligne 9",
                    fcfa(available),
                ),
            ],
            "Étape du calcul",
        ),
        p(
            "La mensualité du crédit demandé, calculée avec le taux de la grille en vigueur "
            f"(voir l'exemple chiffré de TAR-2026), doit être inférieure ou égale à "
            f"{fcfa(available)}. Si elle est supérieure, l'agent propose un montant plus faible "
            "ou une durée plus longue, dans les limites de la section 7."
        ),
        h2("Cas d'un demandeur salarié"),
        p(
            "Pour un salarié, le revenu net mensuel est le salaire net figurant sur les trois "
            "derniers bulletins de paie, augmenté des revenus annexes justifiés. Les primes "
            "exceptionnelles ne sont pas retenues. Un engagement de domiciliation du salaire "
            "sur le compte Kouri est demandé lorsque l'employeur l'accepte."
        ),
        h2("Si la règle n'est pas respectée"),
        p(
            "Aucun dossier dépassant le ratio n'est présenté pour décision. L'agent explique "
            "au client pourquoi le montant demandé l'exposerait au surendettement et lui "
            "propose une solution adaptée : montant réduit, durée allongée dans les limites de "
            "la section 7, ou report de la demande après le remboursement d'un crédit en cours."
        ),
        callout(
            "Points de vigilance",
            [
                "Revenus saisonniers : on retient la moyenne des 12 derniers mois, pas le "
                "meilleur mois.",
                "Revenus non justifiés : ils sont exclus du calcul, même s'ils sont probables.",
                "Plusieurs activités : chacune est analysée séparément, puis les revenus nets "
                "sont additionnés.",
            ],
        ),
    ]


def _page_7() -> Page:
    return [
        h1("10. Garanties"),
        p(
            "Les garanties réduisent la perte en cas de défaillance, mais elles ne remplacent "
            "jamais l'analyse de la capacité de remboursement. Un dossier dont la capacité est "
            "insuffisante est refusé, même si les garanties proposées sont abondantes."
        ),
        table(
            [
                ["Montant du crédit", "Garanties minimales exigées"],
                [
                    f"Jusqu'à {fcfa(750_000)}",
                    "Épargne préalable bloquée (section 6) et caution personnelle d'un tiers "
                    "solvable",
                ],
                [
                    f"De {fcfa(750_001)} à {fcfa(3_000_000)}",
                    "Garanties ci-dessus et gage sur matériel ou stock d'une valeur au moins égale "
                    "à 120 % du crédit",
                ],
                [
                    f"Au-delà de {fcfa(3_000_000)}",
                    "Garanties ci-dessus et hypothèque, nantissement d'un titre foncier ou dépôt à "
                    "terme bloqué",
                ],
            ],
            (0.34, 0.66),
        ),
        h2("Règles pratiques"),
        *bullets(
            [
                "La caution est une personne majeure dont les revenus ont été vérifiés ; elle "
                "signe l'acte de caution devant le chef d'agence, après lecture à voix haute.",
                "Une même personne ne peut cautionner plus de deux crédits en cours chez Kouri.",
                "Les biens gagés sont inventoriés, photographiés et décrits dans un acte signé "
                "par le client ; ils restent chez le client, qui s'engage à ne pas les vendre.",
                "L'assurance décès-invalidité est obligatoire pour tout crédit ; sa prime est "
                "fixée par la grille des taux et frais en vigueur.",
                "Les garanties sont levées par écrit dans les 5 jours ouvrables qui suivent le "
                "remboursement complet du crédit.",
                "Un salarié de Kouri ne peut se porter caution pour un client, ni un client "
                "pour un salarié, afin d'éviter tout conflit d'intérêts.",
            ]
        ),
        h2("Évaluation des biens"),
        p(
            "L'agent estime la valeur des biens gagés à leur prix de revente rapide sur le "
            "marché local, et non à leur prix d'achat. Pour le matériel de plus de trois ans, "
            "la valeur retenue ne dépasse pas la moitié du prix d'achat. Au-delà de "
            f"{fcfa(3_000_000)}, l'évaluation d'un bien immobilier est confiée à un expert "
            "agréé, à la charge du client."
        ),
        h2("Mainlevée des garanties"),
        p(
            "À la fin du crédit, le chef d'agence signe la mainlevée de chaque garantie, remet "
            "au client et à ses cautions une attestation de remboursement, et débloque "
            "l'épargne préalable. Si un nouveau crédit est accordé aussitôt, les garanties "
            "peuvent être reconduites, à condition que le client et les cautions signent un "
            "nouvel acte : une garantie n'est jamais transférée tacitement d'un crédit à "
            "l'autre."
        ),
    ]


def _page_8() -> Page:
    return [
        h1("11. Circuit de décision et décaissement"),
        table(
            [
                ["Étape", "Responsable", "Action", "Délai"],
                [
                    "1. Accueil",
                    "Agent de crédit",
                    "Vérifie les conditions de la section 6",
                    "Le jour même",
                ],
                [
                    "2. Instruction",
                    "Agent de crédit",
                    "Visite de l'activité, analyse, fiche de synthèse",
                    "3 jours ouvrables",
                ],
                [
                    "3. Contrôle",
                    "Chef d'agence",
                    "Complétude et cohérence du dossier",
                    "1 jour ouvrable",
                ],
                [
                    "4. Décision",
                    "Niveau compétent (voir CR-PRO-02)",
                    "Accord, ajournement ou refus motivé",
                    "Séance suivante",
                ],
                [
                    "5. Information",
                    "Agent de crédit",
                    "Notification écrite, tableau d'amortissement, coût total",
                    "2 jours ouvrables",
                ],
                [
                    "6. Signature",
                    "Client, cautions, chef d'agence",
                    "Contrat, acte de caution, acte de gage",
                    "Sur rendez-vous",
                ],
                [
                    "7. Décaissement",
                    "Caissier",
                    "Versement sur le compte du client",
                    "Après contrôle",
                ],
                [
                    "8. Archivage",
                    "Assistant de crédit",
                    "Dossier physique et numérique",
                    "Sous 3 jours",
                ],
            ],
            (0.16, 0.24, 0.40, 0.20),
        ),
        p(
            "Les niveaux d'autorisation (chef d'agence, comité de crédit, Direction générale, "
            "Conseil d'administration) et leurs plafonds sont définis exclusivement dans "
            "CR-PRO-02. Ils ne sont pas repris ici, pour éviter toute divergence entre deux "
            "documents."
        ),
        h2("Séparation des fonctions"),
        *bullets(
            [
                "L'agent qui a instruit le dossier le présente, mais ne vote pas lorsqu'il "
                "siège au comité.",
                "Le caissier décaisse uniquement sur présentation de la décision signée et du "
                "contrat, après contrôle de l'identité du client.",
                "Le décaissement se fait toujours par crédit du compte du client, jamais en "
                "espèces remises de la main à la main par l'agent.",
            ]
        ),
        h2("Contrôles du caissier avant décaissement"),
        *bullets(
            [
                "La décision porte la signature du niveau compétent et la date de la séance.",
                "Le montant, la durée et la date de première échéance du contrat sont "
                "identiques à ceux de la décision.",
                "Les frais de dossier et la prime d'assurance sont prélevés conformément à la "
                "grille en vigueur, et le montant net versé est indiqué au client.",
            ]
        ),
        callout(
            "Interdit",
            [
                "Décaisser avant la signature du contrat et des actes de garantie.",
                "Faire décider un dossier par une personne en situation de conflit d'intérêts.",
                "Fractionner un crédit en plusieurs prêts pour contourner un plafond "
                "d'autorisation.",
                "Accepter une commission, un cadeau ou un service d'un demandeur, avant ou "
                "après la décision.",
            ],
        ),
    ]


def _page_9() -> Page:
    return [
        h1("12. Suivi du crédit et cas particuliers"),
        h2("12.1 Visite de suivi"),
        p(
            "Dans les 30 jours qui suivent le décaissement, l'agent visite le client pour "
            "vérifier que les fonds ont servi à l'objet prévu. Il note ses constats dans la "
            "fiche de suivi. Un usage non conforme est signalé au chef d'agence le jour même."
        ),
        h2("12.2 Retards de paiement"),
        p(
            "Dès le premier jour de retard, l'agent contacte le client par téléphone pour en "
            "connaître la cause. La suite de la procédure (relances, visites, mise en demeure "
            "et contentieux) est décrite dans CR-PRO-04, qui seul fixe les étapes et leurs "
            "délais."
        ),
        h2("12.3 Remboursement anticipé"),
        p(
            "Le client peut rembourser tout ou partie de son crédit à tout moment. Les intérêts "
            "cessent de courir sur le capital remboursé. Les conditions financières éventuelles "
            "figurent dans la grille des taux et frais en vigueur."
        ),
        h2("12.4 Rééchelonnement"),
        p(
            "Le rééchelonnement reste exceptionnel. Il n'est envisagé qu'après un événement "
            "subi par le client et dûment constaté : maladie grave, inondation, incendie, vol "
            "du stock. Il est décidé par le niveau supérieur à celui qui a accordé le crédit, "
            "une seule fois par crédit, et donne lieu à un nouveau tableau d'amortissement "
            "signé par le client et ses cautions."
        ),
        h2("12.5 Décès ou invalidité de l'emprunteur"),
        p(
            "L'assurance décès-invalidité rembourse le capital restant dû. La famille remet à "
            "l'agence l'acte de décès ou le certificat médical ; aucune somme n'est réclamée "
            "aux héritiers ni aux cautions pour la partie couverte par l'assurance."
        ),
        h2("12.6 Conflits d'intérêts"),
        p(
            "Tout salarié qui a un lien familial, commercial ou amical étroit avec un "
            "demandeur le déclare par écrit à son responsable. Le dossier est alors confié à "
            "un autre agent et décidé par le niveau supérieur. L'absence de déclaration "
            "constitue une faute au sens du règlement intérieur (voir RH-REG-01)."
        ),
        h2("12.7 Changement de situation du client"),
        p(
            "Le client informe l'agence de tout déménagement, changement d'activité ou "
            "fermeture de son commerce. L'agent met à jour le dossier, vérifie que la capacité "
            "de remboursement reste suffisante et, si besoin, propose un rendez-vous avec le "
            "chef d'agence pour adapter le suivi."
        ),
        h2("12.8 Rapport mensuel"),
        p(
            "Chaque mois, le chef d'agence transmet à la Direction du crédit le nombre de "
            "dossiers reçus, accordés, ajournés et refusés, ainsi que les motifs de refus les "
            "plus fréquents. Ces chiffres servent à adapter les produits aux besoins réels."
        ),
    ]


def _page_10() -> Page:
    return [
        h1("13. Questions fréquentes"),
        *faq(
            [
                (
                    "Un client peut-il avoir deux crédits Kouri en même temps ?",
                    "Oui, au plus deux, si le total des mensualités respecte la règle de la "
                    "section 9 et si le premier crédit est déjà remboursé à moitié.",
                ),
                (
                    "Un ancien client revient après trois ans sans emprunter. Quel plafond ?",
                    "Sa demande est traitée comme un premier crédit, car son dernier crédit a été "
                    "soldé depuis plus de 24 mois (définitions de la section 5).",
                ),
                (
                    "Peut-on accorder un crédit à une personne qui n'a pas de compte chez Kouri ?",
                    "Non. Elle doit d'abord ouvrir un compte (voir OP-PRO-01) et le faire "
                    "fonctionner pendant la durée minimale prévue à la section 6.",
                ),
                (
                    "Qui fixe les taux d'intérêt ?",
                    "Le Conseil d'administration, chaque année, par la grille des taux et frais. "
                    "Seule la grille la plus récente s'applique aux nouveaux contrats.",
                ),
                (
                    "Le client peut-il choisir la date de ses échéances ?",
                    "Oui, entre le 1er et le 28 du mois, selon le rythme de ses rentrées "
                    "d'argent. La date choisie figure dans le contrat.",
                ),
                (
                    "Que faire si le client conteste un refus ?",
                    "L'agent lui explique les motifs écrits et l'oriente vers la procédure de "
                    "réclamation (voir QUA-PRO-01).",
                ),
                (
                    "Un client peut-il rembourser à la place d'un autre ?",
                    "Un tiers peut déposer de l'argent sur le compte de l'emprunteur, mais le "
                    "crédit reste au nom de l'emprunteur, seul responsable du remboursement.",
                ),
                (
                    "Le crédit peut-il servir à acheter un terrain ou une maison ?",
                    "Non. Les produits de la présente politique financent une activité, un "
                    "équipement, une campagne agricole ou la rentrée scolaire uniquement.",
                ),
            ]
        ),
        h1("14. Historique des versions"),
        table(
            [
                ["Version", "Date", "Principales modifications"],
                ["1.0", "Mars 2022", "Création de la politique de crédit"],
                ["2.0", "Janvier 2024", "Ajout du crédit scolaire et du crédit agricole"],
                [
                    "3.0",
                    "Janvier 2026",
                    "Refonte de l'analyse de capacité, renvois vers CR-PRO-02 et TAR-2026",
                ],
            ],
            (0.14, 0.2, 0.66),
        ),
        p(
            "Les questions sur l'application de cette politique sont adressées à la Direction "
            "du crédit, au siège, par l'intermédiaire du chef d'agence. Les propositions "
            "d'amélioration sont examinées lors de la révision annuelle du document."
        ),
    ]
