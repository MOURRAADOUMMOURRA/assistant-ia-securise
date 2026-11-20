"""Document n° 24 — Plan de continuité d'activité (PCA-01, 6 pages).

Réponses attendues : autonomie du groupe électrogène (page 3) et retraits possibles
lorsque le logiciel est en panne (page 4).
"""

from scripts.demo_corpus.facts import DOCUMENTS, fcfa
from scripts.demo_corpus.render import Page, bullets, callout, faq, h1, h2, p, table, title_block

SPEC = DOCUMENTS[24]
DEGRADED_WITHDRAWAL_CAP = 100_000


def build_pages() -> list[Page]:
    """Construit les 6 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Le plan de continuité d'activité décrit comment Kouri Épargne & Crédit "
            "continue à servir ses clients lorsqu'un incident majeur perturbe son "
            "fonctionnement : coupure d'électricité prolongée, panne du logiciel, "
            "inondation, incendie, troubles dans un quartier. Il fixe les rôles, les "
            "solutions de repli et les délais de reprise."
        ),
        h1("2. Scénarios couverts"),
        table(
            [
                ["Scénario", "Conséquence principale", "Section"],
                ["Coupure d'électricité", "Arrêt des ordinateurs et de la climatisation", "4"],
                [
                    "Panne du logiciel ou du réseau",
                    "Impossible de consulter les comptes et d'enregistrer les opérations",
                    "5",
                ],
                ["Inondation, incendie", "Agence inutilisable pendant plusieurs jours", "6"],
                ["Troubles, insécurité", "Fermeture préventive d'une ou plusieurs agences", "6"],
                ["Absence massive de personnel", "Guichets insuffisants", "6"],
            ],
            (0.3, 0.55, 0.15),
        ),
        h1("3. Principes"),
        *bullets(
            [
                "La sécurité des personnes passe avant la continuité des opérations.",
                "Les services essentiels sont maintenus en priorité : retraits limités, "
                "dépôts, remboursements de crédit.",
                "Toute opération faite en mode de repli est ressaisie dans le logiciel dès "
                "son retour, avant toute nouvelle opération du même client.",
                "Le plan est testé chaque année et mis à jour après chaque incident réel.",
            ]
        ),
        h2("Objectifs de reprise"),
        p(
            "Les services essentiels doivent être rétablis dans la journée dans au moins "
            "une agence de chaque ville ; le fonctionnement normal doit reprendre dans la"
            " semaine, sauf destruction d'une agence."
        ),
    ]


def _p2() -> Page:
    return [
        h1("4. Organisation de crise"),
        h2("La cellule de crise"),
        p(
            "La cellule de crise est réunie par le Directeur général, ou par le Directeur "
            "des opérations en son absence, dès qu'un incident dépasse les capacités d'une "
            "agence ou dure plus d'une demi-journée. Elle se réunit au siège ou, si le siège "
            "est inaccessible, à l'agence Chagoua, désignée comme site de repli."
        ),
        table(
            [
                ["Membre", "Rôle dans la cellule"],
                ["Directeur général", "Décide et communique avec le Conseil et les autorités"],
                ["Directeur des opérations", "Coordonne les agences et les solutions de repli"],
                ["Responsable du service informatique", "Rétablit les systèmes et les données"],
                ["Directeur financier", "Gère la trésorerie et les besoins en espèces"],
                ["Responsable sécurité", "Évalue les risques pour les personnes et les fonds"],
            ],
            (0.38, 0.62),
        ),
        h2("Alerte"),
        p(
            "Le chef d'agence qui constate un incident prévient immédiatement le Directeur "
            "des opérations, puis note l'heure et la nature de l'incident. Une liste d'appel "
            "à jour, avec les numéros personnels des membres de la cellule, est conservée "
            "dans chaque agence et au domicile de chaque membre."
        ),
        h2("Communication"),
        p(
            "Seule la Direction générale communique à l'extérieur. Les clients sont informés "
            "par affichage à l'entrée des agences et par message, en indiquant l'agence la "
            "plus proche qui reste ouverte et les services disponibles."
        ),
        h2("Fin de la crise"),
        p(
            "La cellule de crise décide du retour au fonctionnement normal lorsque "
            "l'incident est maîtrisé. Elle en informe le personnel, les clients et, le "
            "cas échéant, le Conseil d'administration."
        ),
        h2("Main courante"),
        p(
            "Pendant toute la crise, un membre de la cellule tient une main courante : "
            "heure, décision, responsable. Ce document sert au retour d'expérience."
        ),
        h2("Rôle des chefs d'agence"),
        p(
            "Les chefs d'agence appliquent les consignes de la cellule, rendent compte de"
            " la situation de leur agence plusieurs fois par jour et signalent tout "
            "besoin de fonds, de carburant ou de personnel."
        ),
        h2("Relations avec les autorités"),
        p(
            "En cas d'incident grave touchant la sécurité publique, la cellule de crise "
            "se tient informée auprès des autorités locales et applique leurs consignes, "
            "notamment en matière de circulation et de fermeture des commerces."
        ),
    ]


def _p3() -> Page:
    return [
        h1("5. Coupure d'électricité"),
        p(
            "Les coupures de courant sont fréquentes. Chaque agence est équipée d'un groupe "
            "électrogène avec une autonomie de 8 heures à pleine charge, et d'onduleurs qui "
            "protègent les ordinateurs pendant le démarrage du groupe. Le réservoir est "
            "rempli chaque soir où le groupe a fonctionné."
        ),
        table(
            [
                ["Durée de la coupure", "Mesure"],
                ["Quelques minutes", "Les onduleurs prennent le relais ; aucune action"],
                [
                    "Plus de cinq minutes",
                    "Démarrage du groupe électrogène par le chef d'agence ou l'agent de sécurité",
                ],
                [
                    "Au-delà de l'autonomie du groupe",
                    "Approvisionnement en carburant "
                    "organisé par la Direction des opérations ; à défaut, mode de repli sur "
                    "papier (section 6)",
                ],
            ],
            (0.3, 0.7),
        ),
        h2("Priorités d'alimentation"),
        *bullets(
            [
                "Postes des caissiers, serveur local et équipement réseau.",
                "Éclairage des guichets et de la zone du coffre.",
                "Système d'alarme et vidéosurveillance.",
                "Climatisation du local technique, si la charge le permet.",
            ]
        ),
        h2("Entretien du groupe électrogène"),
        p(
            "Le groupe est démarré à vide chaque semaine pendant quelques minutes, révisé "
            "par un prestataire chaque trimestre, et son carnet d'entretien est tenu à "
            "jour. Une réserve de carburant est stockée hors des locaux, dans un lieu "
            "ventilé et sécurisé."
        ),
        h2("Fermeture anticipée"),
        p(
            "Si le groupe électrogène tombe en panne en cours de journée et que les "
            "onduleurs ne suffisent plus, le chef d'agence passe en mode de repli sur "
            "papier, ou ferme l'agence en accord avec la Direction des opérations."
        ),
        h2("Économie d'énergie"),
        p(
            "Pendant une coupure longue, l'éclairage des bureaux non utilisés et la "
            "climatisation des espaces publics sont coupés, afin de préserver le "
            "carburant pour les équipements essentiels."
        ),
        h2("Registre des coupures"),
        p(
            "Chaque coupure de plus d'une heure est notée dans le registre de sécurité de"
            " l'agence, avec sa durée et la consommation de carburant, pour ajuster les "
            "stocks."
        ),
        h2("Coupure au siège"),
        p(
            "Au siège, le groupe électrogène alimente en priorité le serveur central et "
            "le réseau, afin que les agences restent connectées au logiciel même si "
            "l'électricité du quartier est coupée."
        ),
    ]


def _p4() -> Page:
    return [
        h1("6. Panne du logiciel ou du réseau"),
        p(
            "Si le logiciel de gestion ou la connexion au serveur est indisponible plus "
            "d'une demi-heure, le chef d'agence active le mode de repli sur papier. Les "
            "opérations essentielles continuent, avec des limites qui protègent "
            "l'institution contre les retraits sur des comptes dont le solde ne peut être "
            "vérifié."
        ),
        h2("Opérations en mode de repli"),
        p(
            f"Un client peut retirer au plus {fcfa(DEGRADED_WITHDRAWAL_CAP)} par jour, sur "
            "bordereau papier, après vérification de son identité et de sa signature sur "
            "le carton de spécimen. Le caissier note chaque retrait dans le registre de "
            "repli, et le client signe le bordereau."
        ),
        table(
            [
                ["Opération", "En mode de repli"],
                ["Retrait", "Possible, dans la limite ci-dessus"],
                ["Dépôt", "Possible, sur reçu manuel numéroté"],
                ["Remboursement de crédit", "Possible, sur reçu manuel numéroté"],
                ["Ouverture de compte", "Suspendue"],
                ["Décaissement de crédit", "Suspendu"],
                ["Virement", "Suspendu"],
            ],
            (0.45, 0.55),
        ),
        h2("Retour à la normale"),
        p(
            "Dès que le logiciel est rétabli, les opérations du registre de repli sont "
            "saisies par ordre chronologique, sous le contrôle du chef d'agence. Les soldes "
            "sont vérifiés, et tout dépassement découvert est régularisé avec le client. Le "
            "registre est archivé avec les bordereaux."
        ),
        callout(
            "Carnets de repli",
            [
                "Chaque guichet dispose en permanence d'un carnet de bordereaux et d'un carnet "
                "de reçus numérotés, réservés au mode de repli et vérifiés chaque mois.",
            ],
        ),
        h2("Pourquoi limiter les retraits"),
        p(
            "Sans le logiciel, le caissier ne peut pas vérifier le solde du client. La "
            "limite de retrait évite qu'un client retire plus que ce qu'il possède ou "
            "qu'un fraudeur profite de la panne."
        ),
        h2("Remboursements de crédit"),
        p(
            "Les remboursements reçus en mode de repli sont imputés à leur date de "
            "paiement réelle lors de la ressaisie : le client ne subit aucune pénalité de"
            " retard due à la panne."
        ),
        h2("Panne partielle"),
        p(
            "Si seul un guichet est touché (ordinateur en panne), le caissier est "
            "réaffecté à un autre poste ou travaille sur le poste de secours de l'agence "
            ": le mode de repli n'est pas nécessaire."
        ),
    ]


def _p5() -> Page:
    return [
        h1("7. Agence inutilisable"),
        p(
            "Si une agence ne peut plus accueillir le public (inondation, incendie, "
            "insécurité), ses clients sont orientés vers l'agence la plus proche. Le "
            "personnel y est réaffecté temporairement, et un guichet est réservé aux clients "
            "de l'agence fermée."
        ),
        table(
            [
                ["Agence fermée", "Agence de repli"],
                ["Agence Grand Marché", "Agence Centre (siège)"],
                ["Agence Chagoua", "Agence Centre (siège)"],
                ["Agence Farcha", "Agence Grand Marché"],
                ["Agence Centre (siège)", "Agence Chagoua"],
                [
                    "Agence Moundou ou Abéché",
                    "Point de service temporaire en ville, sur décision de la cellule de crise",
                ],
            ],
            (0.4, 0.6),
        ),
        h2("Données et documents"),
        p(
            "Les données du logiciel sont sauvegardées chaque soir et une copie chiffrée est "
            "conservée hors du siège (voir SI-CHA-01) : la perte d'une agence n'entraîne pas "
            "la perte des comptes. Les dossiers papier des clients sont rangés dans des "
            "armoires fermées, en hauteur dans les agences exposées aux inondations."
        ),
        h2("Fonds"),
        p(
            "Les fonds d'une agence menacée sont transférés au siège par le prestataire de "
            "transport de fonds dès que la menace est connue, si cela peut se faire sans "
            "danger. Le coffre n'est jamais ouvert dans l'urgence au détriment de la "
            "sécurité (voir SEC-PRO-02)."
        ),
        h2("Absence massive de personnel"),
        p(
            "En cas d'épidémie ou de difficultés de transport, les guichets ouverts sont "
            "regroupés dans les agences les mieux dotées et les horaires peuvent être "
            "réduits par note de service."
        ),
        h2("Personnel"),
        p(
            "Le personnel de l'agence fermée est réaffecté dans l'agence de repli ou, si "
            "nécessaire, mis en congé exceptionnel payé sur décision de la Direction "
            "générale."
        ),
        h2("Information des clients"),
        p(
            "Une affiche à l'entrée de l'agence fermée indique l'agence de repli, son "
            "adresse et ses horaires. Les agents de crédit informent leurs clients lors "
            "des visites."
        ),
        h2("Réouverture"),
        p(
            "L'agence fermée ne rouvre qu'après vérification de l'état des locaux, du "
            "coffre, de l'électricité et des équipements informatiques, et après accord "
            "de la cellule de crise."
        ),
    ]


def _p6() -> Page:
    return [
        h1("8. Tests et mise à jour du plan"),
        table(
            [
                ["Test", "Fréquence", "Responsable"],
                ["Démarrage du groupe électrogène en charge", "Chaque mois", "Chef d'agence"],
                [
                    "Exercice de mode de repli sur papier",
                    "Une fois par an et par agence",
                    "Direction des opérations",
                ],
                ["Restauration d'une sauvegarde", "Chaque trimestre", "Service informatique"],
                ["Réunion simulée de la cellule de crise", "Une fois par an", "Directeur général"],
            ],
            (0.45, 0.28, 0.27),
        ),
        p(
            "Après chaque test ou incident réel, un compte rendu identifie ce qui a "
            "fonctionné et ce qui doit être amélioré. Le plan est révisé en conséquence et "
            "présenté au comité d'audit et des risques."
        ),
        h2("Formation du personnel"),
        p(
            "Chaque salarié connaît son rôle en cas de crise : le mode de repli et la "
            "liste d'appel sont présentés lors de l'intégration et rappelés lors des "
            "exercices annuels."
        ),
        h2("Documents de crise"),
        p(
            "Chaque agence conserve dans un classeur rouge la liste d'appel, les carnets "
            "de repli, les consignes de démarrage du groupe électrogène et le plan "
            "d'évacuation."
        ),
        h2("Liens avec les autres procédures"),
        p(
            "Le plan s'articule avec les consignes incendie (voir SEC-CON-01), la "
            "sécurité des agences (voir SEC-PRO-02) et la charte informatique (voir SI-"
            "CHA-01)."
        ),
        h1("9. Questions fréquentes"),
        *faq(
            [
                (
                    "Un client conteste la limite de retrait en mode de repli.",
                    "Expliquez qu'elle protège tous les clients pendant la panne ; il pourra "
                    "retirer le reste dès le rétablissement du logiciel.",
                ),
                (
                    "Le groupe électrogène ne démarre pas.",
                    "Prévenez la Direction des opérations et passez en mode de repli dès que les "
                    "onduleurs s'arrêtent.",
                ),
            ]
        ),
        h1("10. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Mai 2022", "Création du plan"],
                ["1.3", SPEC.approval_date, "Site de repli et agences de repli"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
