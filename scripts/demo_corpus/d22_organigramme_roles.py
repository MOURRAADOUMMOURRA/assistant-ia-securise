"""Document n° 22 — Organigramme et rôles des services (ORG-01, 4 pages).

Réponses attendues : nombre et répartition des agences (page 1) et rattachement du
responsable de la conformité (page 3).
"""

from scripts.demo_corpus.facts import AGENCIES, DOCUMENTS, STAFF_COUNT_2025
from scripts.demo_corpus.render import Page, bullets, callout, h1, h2, p, table, title_block

SPEC = DOCUMENTS[22]


def build_pages() -> list[Page]:
    """Construit les 4 pages du document."""
    return [_p1(), _p2(), _p3(), _p4()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Présentation de l'institution"),
        p(
            "Kouri Épargne & Crédit S.A. est un établissement de microfinance de 2e "
            "catégorie dont le siège est à N'Djamena. Il compte six agences : 4 à N'Djamena, "
            f"1 à Moundou et 1 à Abéché, et emploie {STAFF_COUNT_2025} salariés. Son nom "
            "rappelle le kouri, race bovine du lac Tchad : au Sahel, le bétail est la forme "
            "traditionnelle de l'épargne."
        ),
        h2("Le réseau d'agences"),
        table(
            [
                ["Agence", "Ville", "Particularités"],
                [AGENCIES[0], "N'Djamena", "Siège social et services centraux"],
                [
                    AGENCIES[1],
                    "N'Djamena",
                    "Clientèle de commerçants ; horaires adaptés lors de certaines périodes",
                ],
                [AGENCIES[2], "N'Djamena", "Forte clientèle de groupements solidaires"],
                [AGENCIES[3], "N'Djamena", "Zone d'activités artisanales et de transport"],
                [AGENCIES[4], "Moundou", "Crédit agricole et commerce régional"],
                [AGENCIES[5], "Abéché", "Commerce et élevage"],
            ],
            (0.28, 0.17, 0.55),
        ),
        h1("2. Objet du document"),
        p(
            "Ce document présente l'organisation de l'institution : instances de "
            "gouvernance, directions et services, rattachements hiérarchiques et rôles en "
            "agence. Il permet à chaque salarié de savoir à qui s'adresser et qui décide. "
            "Il est mis à jour à chaque changement d'organisation."
        ),
        callout(
            "Mission",
            [
                "Offrir aux micro-entrepreneurs, aux ménages et aux groupements des services "
                "d'épargne et de crédit sûrs, transparents et adaptés, dans le respect de "
                "la dignité de chaque client.",
            ],
        ),
        h2("Valeurs"),
        p(
            "Proximité avec les clients, rigueur dans la gestion de leur argent, "
            "transparence des conditions, respect de chacun : ces valeurs guident le "
            "comportement de tous les salariés et figurent dans le règlement intérieur."
        ),
    ]


def _p2() -> Page:
    return [
        h1("3. Gouvernance"),
        table(
            [
                ["Instance", "Composition", "Rôle principal"],
                [
                    "Assemblée générale",
                    "Actionnaires",
                    "Approuve les comptes, nomme les administrateurs et le commissaire aux comptes",
                ],
                [
                    "Conseil d'administration",
                    "Administrateurs, dont des indépendants",
                    "Fixe la stratégie, les politiques et les grilles tarifaires ; contrôle la "
                    "Direction générale",
                ],
                [
                    "Comité d'audit et des risques",
                    "Trois administrateurs",
                    "Supervise l'audit interne, les risques et la conformité",
                ],
                [
                    "Direction générale",
                    "Directeur général",
                    "Dirige l'institution et met en œuvre la stratégie",
                ],
            ],
            (0.25, 0.3, 0.45),
        ),
        h1("4. Directions et services du siège"),
        table(
            [
                ["Direction ou service", "Missions principales"],
                [
                    "Direction du crédit",
                    "Politique de crédit, comité du siège, suivi du "
                    "portefeuille, recouvrement et contentieux",
                ],
                [
                    "Direction des opérations",
                    "Réseau d'agences, caisse, sécurité, continuité d'activité",
                ],
                [
                    "Direction financière",
                    "Comptabilité, trésorerie, budget, tarification, frais de mission",
                ],
                ["Direction des ressources humaines", "Recrutement, paie, formation, discipline"],
                [
                    "Direction de la conformité",
                    "Lutte anti-blanchiment, protection des données, veille réglementaire",
                ],
                ["Service informatique", "Logiciel de gestion, réseau, sécurité informatique"],
                ["Service qualité", "Réclamations, satisfaction des clients"],
                ["Audit interne", "Contrôle indépendant de toutes les activités"],
            ],
            (0.35, 0.65),
        ),
        h2("Comités internes"),
        p(
            "La Direction générale réunit chaque semaine un comité de direction avec les "
            "directeurs. Le comité de crédit du siège et le comité de gestion des risques "
            "se réunissent selon leurs propres procédures (voir CR-PRO-02)."
        ),
        h2("Rôle du Conseil d'administration"),
        p(
            "Le Conseil approuve chaque année le budget, la grille des taux et frais et "
            "le plan de formation. Il adopte les politiques de crédit, de conformité et "
            "de protection des données, et nomme le Directeur général."
        ),
        h2("Comité de direction"),
        p(
            "Le comité de direction suit chaque semaine l'activité, les indicateurs de "
            "risque et les projets en cours. Ses décisions sont consignées dans un compte"
            " rendu diffusé aux directeurs et aux chefs d'agence."
        ),
    ]


def _p3() -> Page:
    return [
        h1("5. Rattachements hiérarchiques"),
        p(
            "Les directeurs sont rattachés au Directeur général, qui est lui-même nommé par "
            "le Conseil d'administration et lui rend compte. Deux fonctions de contrôle "
            "bénéficient de garanties particulières d'indépendance."
        ),
        h2("La conformité"),
        p(
            "Le responsable de la conformité est rattaché directement au Directeur général, "
            "sans intermédiaire. Il dispose en outre d'un accès direct au comité d'audit et "
            "des risques, qu'il peut saisir de sa propre initiative sur toute question grave. "
            "Ce double accès garantit qu'aucun directeur opérationnel ne peut freiner une "
            "alerte ou une déclaration."
        ),
        h2("L'audit interne"),
        p(
            "Le responsable de l'audit interne rend compte fonctionnellement au comité "
            "d'audit et des risques, qui approuve son programme annuel, et "
            "administrativement au Directeur général. Il peut contrôler toutes les "
            "activités, y compris celles de la Direction générale."
        ),
        table(
            [
                ["Fonction", "Rattachement", "Accès complémentaire"],
                ["Directeurs opérationnels", "Directeur général", "—"],
                [
                    "Responsable de la conformité",
                    "Directeur général",
                    "Comité d'audit et des risques",
                ],
                [
                    "Responsable de l'audit interne",
                    "Comité d'audit et des risques",
                    "Directeur général (administratif)",
                ],
                [
                    "Chefs d'agence",
                    "Directeur des opérations",
                    "Directeur du crédit pour les dossiers de crédit",
                ],
                ["Service qualité", "Directeur général", "—"],
            ],
            (0.32, 0.32, 0.36),
        ),
        h2("Intérim"),
        p(
            "En l'absence du Directeur général, l'intérim est assuré par le directeur "
            "désigné par écrit ; il ne peut pas modifier l'organisation ni les "
            "rattachements."
        ),
        h2("Chefs d'agence et services centraux"),
        p(
            "Le chef d'agence dépend du Directeur des opérations pour l'organisation de "
            "son agence, la caisse et la sécurité. Pour les dossiers de crédit, il "
            "applique les décisions de la Direction du crédit et lui transmet les "
            "dossiers qui dépassent sa compétence."
        ),
        h2("Relations entre services"),
        p(
            "Les services du siège apportent leur appui aux agences : conseil juridique "
            "pour le contentieux, assistance informatique, formation. Chaque demande "
            "d'une agence reçoit une réponse dans les meilleurs délais, par la personne "
            "compétente."
        ),
        h2("Organigramme affiché"),
        p(
            "Un organigramme nominatif, avec les noms et les numéros internes des "
            "responsables, est affiché dans chaque agence et mis à jour par la Direction "
            "des ressources humaines à chaque mouvement."
        ),
    ]


def _p4() -> Page:
    return [
        h1("6. Rôles en agence"),
        table(
            [
                ["Fonction", "Rôle"],
                [
                    "Chef d'agence",
                    "Dirige l'agence, décide dans sa compétence de crédit, "
                    "garantit la sécurité et la qualité du service",
                ],
                [
                    "Chef d'agence adjoint",
                    "Remplace le chef d'agence, supervise l'accueil et les comptes",
                ],
                [
                    "Caissier principal",
                    "Gère la réserve, contrôle les caissiers, co-détient l'accès au coffre",
                ],
                ["Caissiers", "Opérations au guichet (voir OP-PRO-02)"],
                [
                    "Agents de crédit",
                    "Instruisent les dossiers, suivent leur portefeuille, animent les groupements",
                ],
                ["Chargé de clientèle", "Accueil, ouverture de comptes, conseil en épargne"],
                ["Agent de sécurité", "Contrôle de l'accès et surveillance des abords"],
            ],
            (0.28, 0.72),
        ),
        h2("Principes d'organisation"),
        *bullets(
            [
                "Chaque salarié a un seul responsable hiérarchique direct.",
                "Les fonctions incompatibles (caisse et crédit, saisie et validation) sont "
                "séparées, même dans les petites agences.",
                "Toute délégation de pouvoir est écrite, datée et limitée dans le temps.",
            ]
        ),
        h2("Remplacements en agence"),
        p(
            "En l'absence du chef d'agence, son adjoint assure l'intérim ; en l'absence "
            "des deux, le Directeur des opérations désigne un remplaçant. Le caissier "
            "principal est remplacé par un caissier habilité désigné par écrit."
        ),
        h2("Réunion d'agence"),
        p(
            "Chaque semaine, le chef d'agence réunit son équipe pour faire le point sur "
            "l'activité, les retards de remboursement, les réclamations et les consignes "
            "reçues du siège."
        ),
        h2("Évolution de l'organisation"),
        p(
            "Toute modification de l'organisation est proposée par le Directeur général, "
            "approuvée par le Conseil d'administration lorsqu'elle touche les directions, "
            "puis présentée au personnel."
        ),
        h2("Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["3.0", "Janvier 2024", "Création de la Direction de la conformité"],
                ["4.0", SPEC.approval_date, "Comité d'audit et des risques, rôles en agence"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
