"""Document n° 5 — Frais de mission (FIN-PRO-05, 5 pages).

Réponses attendues : indemnité hors de N'Djamena (page 3) et délai de remise des
justificatifs (page 4).
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

SPEC = DOCUMENTS[5]
DAILY_ALLOWANCE = 15_000
HOTEL_CAP = 20_000
CITY_MEAL = 3_000
KM_RATE = 150
KM_EXAMPLE = 120

# Exemple : mission de trois jours à Moundou.
EXAMPLE_DAYS = 3
EXAMPLE_NIGHTS = 2
EXAMPLE_HOTEL = 18_000
EXAMPLE_BUS = 12_500
ADVANCE_RATIO = 0.8


def build_pages() -> list[Page]:
    """Construit les 5 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Cette procédure fixe les règles de prise en charge des frais engagés par le "
            "personnel lors des déplacements professionnels : visites d'agences, formations, "
            "réunions, contrôles, collecte sur le terrain. Elle garantit au salarié qu'il ne "
            "supporte aucune dépense pour le compte de l'institution, et à l'institution que "
            "chaque franc dépensé est justifié."
        ),
        h2("Champ d'application"),
        p(
            "La procédure s'applique à tous les salariés et stagiaires envoyés en mission "
            "par l'institution. Les déplacements des administrateurs et des consultants "
            "extérieurs suivent leurs propres conventions, sur la base du même barème."
        ),
        h1("2. Définitions"),
        table(
            [
                ["Terme", "Définition"],
                [
                    "Mission",
                    "Déplacement professionnel autorisé hors du lieu de travail "
                    "habituel, d'au moins une demi-journée",
                ],
                [
                    "Ordre de mission",
                    "Document signé qui autorise la mission et en fixe "
                    "l'objet, la destination, les dates et le budget",
                ],
                [
                    "Indemnité journalière",
                    "Somme forfaitaire qui couvre les repas et les "
                    "petits frais d'une journée de mission",
                ],
                [
                    "Frais réels",
                    "Dépenses remboursées sur justificatif : hébergement, "
                    "transport, frais exceptionnels autorisés",
                ],
            ],
            (0.25, 0.75),
        ),
        h1("3. Principes"),
        *bullets(
            [
                "Aucune mission sans ordre de mission signé avant le départ.",
                "Le moyen de transport le plus économique et le plus sûr est choisi.",
                "Les frais sont limités au strict besoin de la mission.",
                "Toute dépense est justifiée par une pièce originale, sauf l'indemnité "
                "journalière, qui est forfaitaire.",
            ]
        ),
    ]


def _p2() -> Page:
    return [
        h1("4. L'ordre de mission"),
        table(
            [
                ["Étape", "Responsable", "Délai"],
                [
                    "Rédaction de l'ordre (objet, destination, dates, budget estimé)",
                    "Salarié ou son responsable",
                    "3 jours ouvrables avant le départ",
                ],
                [
                    "Signature",
                    "Responsable hiérarchique ; Directeur général pour les chefs de service",
                    "Avant le départ",
                ],
                ["Visa budgétaire", "Direction financière", "1 jour ouvrable"],
                ["Versement de l'avance", "Caisse du siège ou de l'agence", "La veille du départ"],
            ],
            (0.45, 0.35, 0.2),
        ),
        h2("Avance sur frais"),
        p(
            "À sa demande, le salarié reçoit une avance égale à 80 % du budget estimé de la "
            "mission. L'avance est versée sur son compte ou, exceptionnellement, en espèces "
            "contre reçu. Une nouvelle avance n'est pas accordée tant que la précédente n'a "
            "pas été régularisée."
        ),
        h2("Mission en groupe"),
        p(
            "Lorsque plusieurs salariés partent ensemble, un seul ordre de mission collectif "
            "est établi, avec la liste des participants. Le plus ancien dans le grade le plus "
            "élevé est désigné chef de mission : il gère l'avance commune et remet un état de "
            "frais unique au retour."
        ),
        h1("5. Transport"),
        table(
            [
                ["Moyen", "Quand l'utiliser", "Prise en charge"],
                [
                    "Véhicule de service",
                    "Missions des équipes du siège, transport groupé",
                    "Carburant payé par l'institution",
                ],
                [
                    "Car interurbain",
                    "Missions individuelles entre villes",
                    "Billet remboursé sur justificatif",
                ],
                [
                    "Moto-taxi ou taxi",
                    "Déplacements courts en ville",
                    "Remboursé sur état signé du responsable",
                ],
                [
                    "Véhicule personnel",
                    "Avec accord écrit préalable seulement",
                    f"Indemnité de {fmt_int(KM_RATE)} FCFA par kilomètre",
                ],
                ["Avion", "Sur décision du Directeur général", "Billet en classe économique"],
            ],
            (0.22, 0.43, 0.35),
        ),
        h2("Choix de l'itinéraire"),
        p(
            "L'itinéraire le plus direct est retenu, sauf consigne de sécurité contraire. "
            "Un détour pour convenance personnelle reste à la charge du salarié, de même que "
            "les jours supplémentaires passés sur place en dehors des dates de la mission."
        ),
        callout(
            "Sécurité",
            [
                "Les trajets de nuit entre villes sont interdits, sauf urgence autorisée par "
                "le Directeur général. Aucun salarié ne transporte de fonds de l'institution "
                "pendant une mission, sauf procédure spéciale de transfert.",
            ],
        ),
    ]


def _p3() -> Page:
    nights = EXAMPLE_NIGHTS * EXAMPLE_HOTEL
    allowances = EXAMPLE_DAYS * DAILY_ALLOWANCE
    transport = 2 * EXAMPLE_BUS
    total = allowances + nights + transport
    advance = round(total * ADVANCE_RATIO)
    return [
        h1("6. Barème des indemnités"),
        table(
            [
                ["Type de mission", "Indemnité journalière", "Hébergement"],
                [
                    "Dans N'Djamena, hors du lieu de travail habituel",
                    f"{fcfa(CITY_MEAL)} par repas pris sur place",
                    "Non pris en charge",
                ],
                [
                    "Hors de N'Djamena",
                    f"{fcfa(DAILY_ALLOWANCE)} par jour",
                    f"Frais réels, plafonnés à {fcfa(HOTEL_CAP)} par nuit",
                ],
                [
                    "À l'étranger",
                    "Fixée par décision du Directeur général",
                    "Fixé par la même décision",
                ],
            ],
            (0.38, 0.3, 0.32),
        ),
        p(
            "L'indemnité journalière est due pour chaque jour de mission, jour de départ et "
            "jour de retour compris. Elle n'est pas due lorsque les repas sont fournis par "
            "l'organisateur d'une formation ou d'un séminaire. L'hébergement est choisi dans "
            "un établissement sûr ; si le prix dépasse le plafond, la différence reste à la "
            "charge du salarié, sauf autorisation écrite préalable."
        ),
        h2("Exemple : mission de trois jours à Moundou"),
        *calculation(
            [
                (
                    f"Indemnités journalières = {EXAMPLE_DAYS} jours × {fmt_int(DAILY_ALLOWANCE)}",
                    fcfa(allowances),
                ),
                (
                    f"Hébergement = {EXAMPLE_NIGHTS} nuits × {fmt_int(EXAMPLE_HOTEL)} "
                    "(sous le plafond)",
                    fcfa(nights),
                ),
                (f"Car aller et retour = 2 × {fmt_int(EXAMPLE_BUS)}", fcfa(transport)),
                ("Coût total de la mission = lignes 1 + 2 + 3", fcfa(total)),
                ("Avance versée avant le départ = ligne 4 × 0,8", fcfa(advance)),
                ("Solde versé au retour = ligne 4 − ligne 5", fcfa(total - advance)),
            ],
            "Étape du calcul",
        ),
        h2("Missions de longue durée"),
        p(
            "Au-delà de quinze jours consécutifs au même endroit, l'hébergement est organisé "
            "par l'institution (location meublée ou convention avec un hôtel) et "
            "l'indemnité journalière est réduite d'un tiers à partir du seizième jour, les "
            "frais du salarié étant alors moins élevés."
        ),
        h2("Repas d'affaires"),
        p(
            "Un repas offert à un partenaire (autorité locale, responsable d'un groupement) "
            "n'est remboursé que s'il a été autorisé à l'avance par le Directeur général, "
            "sur facture mentionnant le nombre et la qualité des convives."
        ),
        h2("Frais exceptionnels"),
        p(
            "Les frais non prévus au barème (traversée par bac, droits de passage, "
            "communication téléphonique urgente) sont remboursés sur justificatif lorsqu'ils "
            "sont nécessaires à la mission et autorisés par le responsable, au besoin par "
            "téléphone puis par écrit."
        ),
    ]


def _p4() -> Page:
    return [
        h1("7. Justification et remboursement"),
        p(
            "Le salarié remet son état de frais et ses justificatifs à la Direction "
            "financière dans les 7 jours ouvrables suivant son retour. Passé ce délai, le "
            "responsable est informé et le remboursement est suspendu jusqu'à la remise des "
            "pièces. Une avance non justifiée dans le mois qui suit le retour est retenue "
            "sur le salaire."
        ),
        h2("Pièces à joindre à l'état de frais"),
        table(
            [
                ["Dépense", "Justificatif accepté"],
                ["Hébergement", "Facture originale au nom de Kouri Épargne & Crédit"],
                ["Car ou avion", "Billet original ou carte d'embarquement"],
                ["Taxi, moto-taxi", "État récapitulatif visé par le responsable"],
                ["Véhicule personnel", "Relevé des kilomètres visé par le responsable"],
                ["Frais exceptionnels", "Facture et autorisation écrite préalable"],
            ],
            (0.3, 0.7),
        ),
        h2("Contrôle"),
        *bullets(
            [
                "La Direction financière vérifie la conformité au barème et à l'ordre de mission.",
                "Le solde dû au salarié est versé sur son compte dans les cinq jours "
                "ouvrables qui suivent le contrôle.",
                "Un trop-perçu est reversé par le salarié ou retenu sur son salaire suivant.",
                "Un justificatif falsifié constitue une faute grave (voir RH-REG-01).",
            ]
        ),
        h2("Justificatif perdu"),
        p(
            "Si un justificatif est perdu, le salarié remet une déclaration sur l'honneur "
            "indiquant la date, le montant et la nature de la dépense, visée par son "
            "responsable. Ce cas reste exceptionnel : au-delà de deux déclarations dans "
            "l'année, plus aucune dépense sans justificatif n'est remboursée."
        ),
        h2("Contestation"),
        p(
            "Si la Direction financière refuse une dépense, elle en indique le motif par "
            "écrit. Le salarié peut demander un réexamen à la Direction générale, avec les "
            "explications et pièces complémentaires utiles, dans le mois qui suit."
        ),
        h2("Comptabilisation"),
        p(
            "La Direction financière enregistre chaque mission sur le compte du service "
            "demandeur. Un état des frais de mission par service est présenté chaque "
            "trimestre à la Direction générale, avec la comparaison au budget."
        ),
        callout(
            "Régularisation des avances",
            [
                "Une avance non justifiée bloque toute nouvelle mission du salarié jusqu'à "
                "sa régularisation. Le chef d'agence vérifie ce point avant de signer un "
                "nouvel ordre de mission.",
            ],
        ),
    ]


def _p5() -> Page:
    return [
        h1("8. Cas particuliers"),
        table(
            [
                ["Situation", "Règle"],
                [
                    "Mission annulée",
                    "L'avance est restituée dans les deux jours ouvrables ; "
                    "les frais déjà engagés sont remboursés sur justificatif",
                ],
                [
                    "Mission prolongée",
                    "La prolongation est autorisée par téléphone puis "
                    "confirmée par un avenant à l'ordre de mission",
                ],
                [
                    "Accident ou maladie",
                    "Les frais médicaux d'urgence sont avancés par "
                    "l'institution ; l'accident est déclaré comme accident du travail",
                ],
                [
                    "Mission de formation",
                    "Les frais pris en charge par l'organisateur ne "
                    "sont pas remboursés une seconde fois",
                ],
            ],
            (0.25, 0.75),
        ),
        h2("Exemple : indemnité kilométrique"),
        *calculation(
            [
                (
                    "Distance aller et retour relevée au compteur, au départ et au retour",
                    f"{fmt_int(KM_EXAMPLE)} km",
                ),
                (
                    "Contrôle : distance cohérente avec l'itinéraire de l'ordre de mission",
                    "Conforme",
                ),
                (
                    f"Indemnité = ligne 1 × {fmt_int(KM_RATE)} FCFA (carburant et usure compris)",
                    fcfa(KM_EXAMPLE * KM_RATE),
                ),
            ],
            "Étape du calcul",
        ),
        h1("9. Questions fréquentes"),
        *faq(
            [
                (
                    "Puis-je loger chez de la famille et toucher le plafond d'hébergement ?",
                    "Non. L'hébergement est remboursé aux frais réels uniquement ; sans facture, "
                    "rien n'est remboursé.",
                ),
                (
                    "L'indemnité journalière est-elle due pour une mission d'une demi-journée ?",
                    "Hors de N'Djamena, oui : elle est due pour chaque jour entamé.",
                ),
                (
                    "Qui signe l'ordre de mission d'un chef d'agence ?",
                    "Le Directeur des opérations, ou le Directeur général en son absence.",
                ),
                (
                    "Les frais de visa ou de vaccination sont-ils remboursés ?",
                    "Oui, pour une mission à l'étranger, sur justificatif, s'ils sont exigés "
                    "pour le pays de destination.",
                ),
            ]
        ),
        h1("10. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Avril 2020", "Création de la procédure"],
                ["1.4", SPEC.approval_date, "Nouveau barème et règles de sécurité des trajets"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
