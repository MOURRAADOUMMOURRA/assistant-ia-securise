"""Document n° 2 — Procédure de demande de congés (RH-PRO-02, 5 pages).

Réponses attendues : congé pour mariage (page 2) et délai de dépôt d'un congé de
plus de 5 jours (page 3).
"""

from scripts.demo_corpus.facts import DOCUMENTS
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

SPEC = DOCUMENTS[2]
DAYS_PER_MONTH = 2
MONTHS_WORKED = 7
DAYS_TAKEN = 5


def build_pages() -> list[Page]:
    """Construit les 5 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet et champ d'application"),
        p(
            "Cette procédure explique comment demander, valider et suivre les congés du "
            "personnel de Kouri Épargne & Crédit. Elle s'applique à tous les salariés, au "
            "siège et en agence. Elle complète le règlement intérieur (voir RH-REG-01), dont "
            "elle précise l'article 8."
        ),
        h1("2. Les différents congés"),
        table(
            [
                ["Type de congé", "Principe", "Section"],
                [
                    "Congé annuel payé",
                    f"{DAYS_PER_MONTH} jours ouvrables acquis par mois de service effectif",
                    "Section 4",
                ],
                [
                    "Congé pour événement familial",
                    "Durée fixe selon l'événement, payée",
                    "Section 3",
                ],
                [
                    "Congé de maternité",
                    "14 semaines, dont une partie avant l'accouchement",
                    "Section 3",
                ],
                ["Congé de maladie", "Sur certificat médical (voir RH-REG-01, article 7)", "—"],
                [
                    "Permission exceptionnelle",
                    "Absence courte, accordée par le responsable, récupérable",
                    "Section 5",
                ],
                ["Congé sans solde", "Sur demande motivée, accordé par la DRH", "Section 5"],
            ],
            (0.3, 0.52, 0.18),
        ),
        h1("3. Principes communs"),
        *bullets(
            [
                "Un congé n'est acquis qu'après validation écrite : un départ sans validation "
                "est une absence irrégulière.",
                "Les congés sont décomptés en jours ouvrables : du lundi au samedi, hors "
                "jours fériés.",
                "Le planning des congés annuels est établi en début d'année pour garantir la "
                "présence d'au moins un caissier et un agent de crédit par agence.",
                "Les congés des membres d'une même équipe sont échelonnés : deux salariés "
                "occupant le même poste dans une agence ne partent pas en même temps.",
            ]
        ),
        h2("Qui contacter"),
        p(
            "Le responsable direct répond aux questions sur les dates et le remplacement. La "
            "Direction des ressources humaines répond aux questions sur les droits, le solde "
            "et les justificatifs. Le salarié peut consulter son solde de congés à tout "
            "moment auprès d'elle ; il figure aussi chaque mois sur le bulletin de paie."
        ),
    ]


def _p2() -> Page:
    return [
        h1("4. Congés pour événements familiaux"),
        p(
            "Ces congés sont accordés de droit, sur présentation d'un justificatif. Ils sont "
            "payés et ne sont pas déduits du congé annuel. Ils doivent être pris au moment de "
            "l'événement, ou dans les quinze jours qui le suivent."
        ),
        table(
            [
                ["Événement", "Durée", "Justificatif"],
                ["Mariage du salarié", "4 jours ouvrables", "Acte de mariage"],
                ["Mariage d'un enfant du salarié", "2 jours ouvrables", "Acte de mariage"],
                ["Naissance d'un enfant (pour le père)", "3 jours ouvrables", "Acte de naissance"],
                ["Décès du conjoint ou d'un enfant", "5 jours ouvrables", "Acte de décès"],
                ["Décès du père ou de la mère", "3 jours ouvrables", "Acte de décès"],
                ["Décès d'un frère ou d'une sœur", "2 jours ouvrables", "Acte de décès"],
                [
                    "Baptême ou circoncision d'un enfant",
                    "1 jour ouvrable",
                    "Attestation de la famille",
                ],
            ],
            (0.45, 0.22, 0.33),
        ),
        h2("Congé de maternité"),
        p(
            "La salariée enceinte bénéficie d'un congé de maternité de 14 semaines. Elle "
            "informe la Direction des ressources humaines au plus tard trois mois avant la "
            "date prévue de l'accouchement, avec un certificat médical. Pendant les quinze "
            "mois qui suivent la naissance, elle dispose d'une heure par jour pour "
            "l'allaitement, à organiser avec son responsable."
        ),
        h2("Justificatifs"),
        p(
            "Le justificatif est remis à la Direction des ressources humaines, en original "
            "ou en copie certifiée, au plus tard dans le mois qui suit l'événement. Sans "
            "justificatif, les jours sont décomptés du congé annuel. Les informations "
            "familiales communiquées sont confidentielles et classées dans le dossier "
            "individuel du salarié."
        ),
        h2("Enfant malade"),
        p(
            "Le salarié parent peut s'absenter pour soigner un enfant malade de moins de "
            "douze ans, sur présentation d'un certificat médical, dans la limite de trois "
            "jours par année civile. Ces jours sont payés et ne réduisent pas le congé "
            "annuel. Au-delà, l'absence est imputée sur le congé annuel ou prise sans solde."
        ),
        h2("Cumul des congés familiaux"),
        p(
            "Lorsque deux événements surviennent en même temps, les durées ne se cumulent "
            "pas : le salarié bénéficie de la durée la plus longue. Un événement qui survient "
            "pendant un congé annuel ne prolonge pas ce congé, sauf décès d'un proche, pour "
            "lequel le congé familial s'ajoute au congé annuel."
        ),
        callout(
            "Événement imprévu",
            [
                "En cas de décès ou d'hospitalisation d'un proche, le salarié prévient son "
                "responsable par téléphone et part sans attendre ; le formulaire et le "
                "justificatif sont remis à son retour.",
            ],
        ),
    ]


def _p3() -> Page:
    return [
        h1("5. Demander un congé annuel"),
        h2("5.1 Délais de dépôt"),
        table(
            [
                ["Durée demandée", "Délai minimal de dépôt avant le départ"],
                ["Jusqu'à 5 jours ouvrables", "3 jours ouvrables"],
                ["Plus de 5 jours ouvrables", "15 jours calendaires"],
            ],
            (0.45, 0.55),
        ),
        p(
            "Une demande déposée hors délai peut être acceptée si le service le permet, mais "
            "elle n'est jamais prioritaire. Pendant les périodes chargées (fins de mois, "
            "rentrée scolaire), le responsable peut refuser une demande tardive."
        ),
        h2("5.2 Circuit de validation"),
        table(
            [
                ["Étape", "Qui", "Action", "Délai de réponse"],
                [
                    "1",
                    "Salarié",
                    "Remplit le formulaire F-RH-03 et le remet à son responsable",
                    "—",
                ],
                [
                    "2",
                    "Responsable direct",
                    "Vérifie le planning et le remplacement, vise ou refuse",
                    "2 jours ouvrables",
                ],
                [
                    "3",
                    "Direction des ressources humaines",
                    "Contrôle le solde et enregistre le congé",
                    "2 jours ouvrables",
                ],
                [
                    "4",
                    "Salarié",
                    "Reçoit la copie validée ; organise la passation",
                    "Avant le départ",
                ],
            ],
            (0.08, 0.28, 0.44, 0.2),
        ),
        h2("5.3 Passation avant le départ"),
        *bullets(
            [
                "Le salarié remet à son remplaçant la liste des dossiers en cours et des "
                "rendez-vous prévus.",
                "Le caissier clôture sa caisse et remet ses clés selon les procédures de "
                "caisse (voir OP-PRO-02).",
                "L'agent de crédit signale les échéances sensibles de son portefeuille.",
            ]
        ),
        h2("5.4 Refus ou report"),
        p(
            "Un refus est toujours motivé par écrit sur le formulaire : besoins du service, "
            "remplacement impossible, solde insuffisant. Le responsable propose alors "
            "d'autres dates. Un congé déjà validé ne peut être reporté par l'institution "
            "qu'en cas de nécessité impérieuse, et les frais déjà engagés par le salarié "
            "(billet de transport non remboursable) sont alors pris en charge."
        ),
        h2("5.5 Archivage"),
        p(
            "Le formulaire validé est classé dans le dossier individuel du salarié. La "
            "Direction des ressources humaines met à jour le solde dans le logiciel de paie "
            "le jour de l'enregistrement, afin que le bulletin du mois soit exact. Le "
            "responsable conserve une copie pour le planning de son équipe."
        ),
    ]


def _p4() -> Page:
    acquired = DAYS_PER_MONTH * MONTHS_WORKED
    return [
        h1("6. Calcul des droits"),
        p(
            f"Le congé annuel s'acquiert à raison de {DAYS_PER_MONTH} jours ouvrables par mois "
            "de service effectif. Les absences pour congé payé, maladie justifiée, accident "
            "du travail ou maternité comptent comme du service effectif."
        ),
        h2("Exemple : salarié embauché en cours d'année"),
        *calculation(
            [
                ("Mois de service effectif depuis l'embauche", f"{MONTHS_WORKED} mois"),
                (
                    f"Droits acquis = ligne 1 × {DAYS_PER_MONTH} jours",
                    f"{acquired} jours ouvrables",
                ),
                ("Jours déjà pris", f"{DAYS_TAKEN} jours ouvrables"),
                (
                    "Solde disponible = ligne 2 − ligne 3",
                    f"{acquired - DAYS_TAKEN} jours ouvrables",
                ),
            ],
            "Étape du calcul",
        ),
        h1("7. Règles particulières"),
        h2("Fractionnement et report"),
        p(
            "Le congé annuel peut être pris en plusieurs fois, à condition qu'une période "
            "d'au moins douze jours ouvrables consécutifs soit prise dans l'année. Le report "
            "sur l'année suivante n'est possible qu'avec l'accord écrit de la Direction des "
            "ressources humaines, et dans la limite de la moitié des droits."
        ),
        h2("Maladie pendant le congé"),
        p(
            "Si le salarié tombe malade pendant son congé, il envoie un certificat médical "
            "dans les deux jours. Les jours de maladie ne sont pas décomptés du congé, qui "
            "est prolongé d'autant ou reporté selon les besoins du service."
        ),
        h2("Rappel pendant le congé"),
        p(
            "Un salarié ne peut être rappelé qu'en cas de nécessité impérieuse du service. "
            "Les frais de retour sont alors pris en charge et les jours non pris sont "
            "reportés."
        ),
        h2("Indemnité de congé"),
        p(
            "Pendant son congé annuel, le salarié perçoit son salaire habituel : salaire de "
            "base, prime d'ancienneté et indemnités fixes. Les primes liées à la présence ou "
            "à la performance du trimestre sont calculées selon la politique de rémunération "
            "(voir RH-POL-04)."
        ),
        h2("Congé pendant la période d'essai"),
        p(
            "Pendant la période d'essai, les droits s'acquièrent normalement, mais leur prise "
            "est limitée aux congés pour événements familiaux et aux urgences, afin que "
            "l'évaluation de fin d'essai porte sur une période de travail suffisante (voir "
            "RH-PRO-03)."
        ),
        h2("Départ de l'institution"),
        p(
            "Le salarié qui quitte l'institution solde ses congés pendant son préavis, si le "
            "service le permet. À défaut, les jours acquis et non pris sont payés sous forme "
            "d'indemnité compensatrice dans le solde de tout compte."
        ),
    ]


def _p5() -> Page:
    return [
        h1("8. Permissions et congé sans solde"),
        p(
            "Une permission exceptionnelle de quelques heures peut être accordée par le "
            "responsable pour une démarche administrative ou un rendez-vous médical. Elle est "
            "récupérée dans le mois. Le congé sans solde, d'une durée maximale de trois mois, "
            "est accordé par la Direction des ressources humaines sur demande motivée."
        ),
        h2("Contenu du formulaire F-RH-03"),
        table(
            [
                ["Rubrique", "À remplir par"],
                ["Type de congé, dates de départ et de retour, nombre de jours", "Salarié"],
                ["Nom du remplaçant et dossiers transmis", "Salarié et responsable"],
                ["Avis et signature, motif en cas de refus", "Responsable direct"],
                ["Solde avant et après le congé, date d'enregistrement", "DRH"],
            ],
            (0.7, 0.3),
        ),
        h1("9. Questions fréquentes"),
        *faq(
            [
                (
                    "Puis-je annuler un congé déjà validé ?",
                    "Oui, en prévenant le responsable au plus tôt ; les jours sont recrédités "
                    "sur le solde.",
                ),
                (
                    "Puis-je accoler un congé pour événement familial à mon congé annuel ?",
                    "Oui, à condition de déposer la demande de congé annuel dans les délais de "
                    "la section 5.1.",
                ),
                (
                    "Mon responsable peut-il refuser mes dates ?",
                    "Oui, pour les besoins du service, mais il doit proposer d'autres dates dans "
                    "le mois qui suit.",
                ),
                (
                    "Puis-je transformer des jours de congé en argent ?",
                    "Non, sauf au départ de l'institution : le congé annuel est fait pour se "
                    "reposer et doit être pris.",
                ),
                (
                    "Comment poser un congé si mon responsable est absent ?",
                    "Le formulaire est visé par son remplaçant désigné ou, à défaut, par le "
                    "responsable de niveau supérieur.",
                ),
                (
                    "Les jours fériés pendant mon congé sont-ils décomptés ?",
                    "Non. Un jour férié qui tombe pendant le congé n'est pas décompté.",
                ),
            ]
        ),
        h1("10. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Juin 2020", "Création de la procédure"],
                ["1.3", SPEC.approval_date, "Nouveau formulaire F-RH-03 et circuit en deux étapes"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
