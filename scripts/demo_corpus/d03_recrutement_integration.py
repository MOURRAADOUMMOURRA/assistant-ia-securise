"""Document n° 3 — Recrutement et intégration (RH-PRO-03, 6 pages).

Réponses attendues : période d'essai d'un agent de crédit (page 4) et remise des
identifiants du logiciel (page 5).
"""

from scripts.demo_corpus.facts import DOCUMENTS
from scripts.demo_corpus.render import Page, bullets, callout, faq, h1, h2, p, table, title_block

SPEC = DOCUMENTS[3]


def build_pages() -> list[Page]:
    """Construit les 6 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Cette procédure décrit les étapes du recrutement, depuis l'expression du besoin "
            "jusqu'à la fin de la période d'essai, et l'accueil des nouveaux salariés. Elle "
            "vise à recruter les meilleures compétences de façon transparente, et à rendre "
            "chaque nouvel arrivant opérationnel rapidement et en sécurité."
        ),
        h1("2. Principes"),
        *bullets(
            [
                "**Égalité des chances** : les candidatures sont examinées sur des critères "
                "écrits, identiques pour tous les candidats d'un même poste.",
                "**Transparence** : chaque étape est tracée dans le dossier de recrutement, "
                "conservé par la Direction des ressources humaines.",
                "**Absence de favoritisme** : un membre du jury qui a un lien de parenté avec "
                "un candidat se retire du jury.",
                "**Priorité interne** : tout poste est d'abord proposé aux salariés en place.",
            ]
        ),
        h1("3. Acteurs"),
        table(
            [
                ["Acteur", "Rôle"],
                [
                    "Responsable du service demandeur",
                    "Exprime le besoin, rédige la fiche de poste, participe au jury",
                ],
                [
                    "Direction des ressources humaines",
                    "Publie l'offre, organise la sélection, établit le contrat",
                ],
                [
                    "Directeur général",
                    "Valide la création du poste et le choix final pour les postes d'encadrement",
                ],
                ["Tuteur", "Accompagne le nouvel arrivant pendant sa période d'essai"],
            ],
            (0.35, 0.65),
        ),
        h2("Confidentialité des candidatures"),
        p(
            "Les dossiers de candidature ne sont consultés que par les personnes chargées de "
            "la sélection. Ceux des candidats non retenus sont conservés six mois, puis "
            "détruits, sauf accord écrit du candidat pour une conservation plus longue en vue "
            "d'un poste futur."
        ),
    ]


def _p2() -> Page:
    return [
        h1("4. Expression du besoin"),
        p(
            "Le responsable du service remplit la fiche de besoin F-RH-01 : intitulé du "
            "poste, missions, compétences attendues, niveau d'études, date souhaitée de prise "
            "de poste et justification (création ou remplacement). La Direction des "
            "ressources humaines vérifie que le poste est prévu au budget avant de le "
            "soumettre au Directeur général."
        ),
        h2("Recrutement interne"),
        p(
            "Un salarié en poste peut se porter candidat avec l'avis de son responsable, qui "
            "ne peut pas s'y opposer mais peut demander un délai de remplacement d'un mois "
            "au plus. À compétences égales, le candidat interne est préféré. Un salarié en "
            "période d'essai ou sanctionné dans l'année ne peut pas postuler."
        ),
        h2("Postes sensibles"),
        p(
            "Les postes de caissier, d'agent de crédit, de chef d'agence et de contrôleur "
            "interne donnent accès aux fonds ou aux décisions de crédit. Pour ces postes, "
            "les références sont toujours vérifiées et le casier judiciaire est exigé avant "
            "l'embauche."
        ),
        h1("5. Publication de l'offre"),
        table(
            [
                ["Étape", "Support", "Durée"],
                [
                    "Publication interne",
                    "Affichage dans toutes les agences et message au personnel",
                    "10 jours",
                ],
                [
                    "Publication externe",
                    "Radio locale, sites d'offres d'emploi, université, centres de formation",
                    "15 jours",
                ],
                ["Clôture", "Plus aucune candidature n'est acceptée", "—"],
            ],
            (0.25, 0.55, 0.2),
        ),
        p(
            "L'offre précise les missions, le profil recherché, le lieu de travail, les "
            "pièces à fournir et la date limite. Elle ne mentionne jamais l'âge, le sexe, la "
            "religion ou l'origine du candidat. Les candidatures sont déposées au siège ou "
            "dans une agence, sous pli fermé, et enregistrées dans un registre."
        ),
        h2("Pièces demandées aux candidats"),
        *bullets(
            [
                "Lettre de motivation et curriculum vitae.",
                "Copie des diplômes et attestations de travail.",
                "Copie d'une pièce d'identité valide.",
                "Pour les postes de caisse et de crédit : extrait de casier judiciaire de "
                "moins de trois mois, fourni avant l'embauche.",
            ]
        ),
        callout(
            "Gratuité du recrutement",
            [
                "Le recrutement est entièrement gratuit pour les candidats. Toute personne "
                "qui demande de l'argent en échange d'un poste doit être signalée à la "
                "Direction générale.",
            ],
        ),
    ]


def _p3() -> Page:
    return [
        h1("6. Sélection des candidats"),
        table(
            [
                ["Étape", "Contenu", "Responsable"],
                [
                    "Présélection",
                    "Examen des dossiers au regard des critères de l'offre",
                    "DRH et service demandeur",
                ],
                ["Test écrit", "Calcul, rédaction, cas pratique propre au métier", "DRH"],
                [
                    "Entretien",
                    "Jury de trois personnes au moins, grille d'évaluation commune",
                    "Jury",
                ],
                [
                    "Références",
                    "Contact de deux anciens employeurs, avec l'accord du candidat",
                    "DRH",
                ],
                ["Visite médicale", "Aptitude au poste", "Médecin désigné"],
            ],
            (0.2, 0.52, 0.28),
        ),
        h2("Grille d'évaluation de l'entretien"),
        table(
            [
                ["Critère", "Poids", "Ce qui est observé"],
                ["Compétences techniques", "35 %", "Maîtrise du métier, réponses au cas pratique"],
                [
                    "Connaissance du terrain",
                    "20 %",
                    "Connaissance des activités et des quartiers servis",
                ],
                ["Intégrité", "20 %", "Réactions aux mises en situation éthiques"],
                ["Communication", "15 %", "Clarté, écoute, langues parlées"],
                ["Motivation", "10 %", "Projet professionnel, connaissance de l'institution"],
            ],
            (0.3, 0.12, 0.58),
        ),
        p(
            "Chaque membre du jury note seul, puis le jury établit une note commune. Le "
            "procès-verbal de sélection classe les candidats et motive le choix. Les "
            "candidats non retenus reçoivent une réponse écrite."
        ),
        h2("Le test écrit"),
        p(
            "Le test est le même pour tous les candidats d'un poste et corrigé sans "
            "connaître le nom du candidat. Pour un agent de crédit, il comprend un calcul de "
            "capacité de remboursement à partir d'un cas réel anonymisé ; pour un caissier, "
            "un exercice de comptage et de détection d'erreurs sur un brouillard de caisse."
        ),
        h2("Vérification des références"),
        p(
            "La Direction des ressources humaines contacte les anciens employeurs indiqués "
            "par le candidat, avec son accord écrit, et note les réponses sur une fiche "
            "jointe au dossier. Elle vérifie les dates d'emploi, les fonctions exercées et "
            "le motif du départ. Une information fausse découverte après l'embauche peut "
            "justifier la rupture du contrat."
        ),
        h2("Mises en situation"),
        p(
            "L'entretien comprend au moins une mise en situation éthique, par exemple : « un "
            "client vous propose une somme pour accélérer son dossier » ou « vous constatez "
            "un écart dans la caisse d'un collègue ». La réponse attendue est toujours le "
            "refus et le signalement au responsable."
        ),
    ]


def _p4() -> Page:
    return [
        h1("7. Contrat de travail et période d'essai"),
        p(
            "Le candidat retenu reçoit une lettre d'engagement, puis signe son contrat de "
            "travail avant sa prise de poste. Le contrat précise le poste, le lieu "
            "d'affectation, la rémunération (voir RH-POL-04) et la durée de la période "
            "d'essai, fixée selon le poste."
        ),
        table(
            [
                ["Poste", "Période d'essai"],
                [
                    "Personnel d'appui (gardien, chauffeur, agent d'entretien)",
                    "1 mois, non renouvelable",
                ],
                ["Caissier, assistant administratif ou de crédit", "2 mois, renouvelable une fois"],
                ["Agent de crédit", "3 mois, renouvelable une fois"],
                ["Chef d'agence, cadre du siège", "4 mois, renouvelable une fois"],
            ],
            (0.6, 0.4),
        ),
        h2("Déroulement de la période d'essai"),
        *bullets(
            [
                "Le nouvel arrivant est suivi par un tuteur désigné avant son arrivée.",
                "Un point d'étape est fait à mi-parcours avec le responsable et le tuteur.",
                "Le renouvellement éventuel est notifié par écrit avant la fin de la "
                "première période, avec ses motifs.",
                "À la fin de la période, le responsable rédige une évaluation écrite qui "
                "conclut à la confirmation, au renouvellement ou à la fin du contrat.",
            ]
        ),
        h2("Confirmation"),
        p(
            "La confirmation dans le poste est notifiée par une lettre de la Direction des "
            "ressources humaines. Pour un agent de crédit, elle suppose notamment que les "
            "dossiers instruits pendant l'essai respectent la politique de crédit (voir "
            "CR-PRO-01) et que l'agent maîtrise le logiciel de gestion."
        ),
        h2("Rupture pendant l'essai"),
        p(
            "Pendant la période d'essai, chacune des parties peut mettre fin au contrat en "
            "respectant le délai de prévenance prévu par la réglementation. La décision de "
            "l'institution est prise par la Direction des ressources humaines, sur la base "
            "de l'évaluation écrite du responsable, et notifiée par lettre remise en main "
            "propre."
        ),
        h2("Affectation"),
        p(
            "Le lieu d'affectation figure au contrat. Un agent recruté pour Moundou ou "
            "Abéché effectue de préférence sa première semaine au siège, pour rencontrer les "
            "services centraux, avant de rejoindre son agence."
        ),
        h2("Dossier administratif d'embauche"),
        *bullets(
            [
                "Contrat signé en deux exemplaires et fiche de renseignements.",
                "Copie des diplômes, de la pièce d'identité et du casier judiciaire.",
                "Relevé d'identité du compte Kouri sur lequel le salaire sera versé.",
                "Certificat d'aptitude délivré par le médecin.",
            ]
        ),
    ]


def _p5() -> Page:
    return [
        h1("8. Accueil et intégration"),
        h2("8.1 Le premier jour"),
        table(
            [
                ["Moment", "Activité", "Avec qui"],
                ["Arrivée", "Accueil, présentation des locaux et des collègues", "Responsable"],
                [
                    "Matinée",
                    "Remise du badge, du règlement intérieur et de la charte "
                    "informatique ; signature des accusés de réception",
                    "DRH",
                ],
                ["Matinée", "Signature de la charte de confidentialité", "DRH"],
                [
                    "Après-midi",
                    "Remise des identifiants du logiciel et première prise en main",
                    "Service informatique",
                ],
                ["Fin de journée", "Bilan avec le tuteur, programme de la semaine", "Tuteur"],
            ],
            (0.18, 0.57, 0.25),
        ),
        p(
            "Les identifiants du logiciel sont remis le premier jour, après signature de la "
            "charte de confidentialité : aucun accès aux données des clients n'est ouvert "
            "avant cette signature. Les droits d'accès sont limités au strict besoin du poste "
            "(voir SI-CHA-01)."
        ),
        h2("8.2 La première semaine"),
        *bullets(
            [
                "Découverte des produits : épargne, crédit, tarifs en vigueur.",
                "Observation au guichet et, pour les agents de crédit, accompagnement du "
                "tuteur en visite de clients.",
                "Formation aux procédures de sécurité de l'agence et aux consignes "
                "d'évacuation, avec visite des issues de secours.",
                "Présentation du chef d'agence sur les objectifs de l'agence et les "
                "habitudes de sa clientèle.",
                "Inscription aux formations obligatoires du plan de formation (voir RH-PLF-2026).",
            ]
        ),
        h2("Formation aux outils"),
        p(
            "Le service informatique forme le nouvel arrivant au logiciel de gestion sur un "
            "environnement d'essai, sans données réelles, pendant ses premiers jours. "
            "L'agent de crédit reçoit sa tablette de collecte après cette formation et après "
            "la lecture commentée des règles de la charte informatique sur les appareils "
            "mobiles."
        ),
        h2("Le rôle du tuteur"),
        p(
            "Le tuteur est un salarié confirmé du même métier, volontaire, qui n'est pas le "
            "responsable hiérarchique du nouvel arrivant. Il répond à ses questions, vérifie "
            "son travail pendant les premières semaines et alerte le responsable en cas de "
            "difficulté. Il consacre au tutorat le temps nécessaire, pris sur son temps de "
            "travail. Son rôle est reconnu lors de son propre entretien annuel."
        ),
        callout(
            "Accès limités pendant l'essai",
            [
                "Pendant sa période d'essai, le nouvel arrivant n'a ni clé ni code du coffre "
                "et ne valide seul aucune opération : ses saisies sont contrôlées par un "
                "collègue habilité.",
            ],
        ),
    ]


def _p6() -> Page:
    return [
        h2("8.3 Le parcours d'intégration"),
        table(
            [
                ["Période", "Objectif", "Validation"],
                [
                    "Semaines 1 et 2",
                    "Connaître l'institution, ses produits et ses règles",
                    "Questionnaire du tuteur",
                ],
                [
                    "Semaines 3 à 6",
                    "Réaliser les tâches courantes sous supervision",
                    "Point d'étape du responsable",
                ],
                [
                    "Jusqu'à la fin de l'essai",
                    "Travailler en autonomie sur son portefeuille ou sa caisse",
                    "Évaluation de fin d'essai",
                ],
            ],
            (0.25, 0.5, 0.25),
        ),
        h2("8.4 Évaluation de fin d'essai"),
        p(
            "Deux semaines avant la fin de la période d'essai, le responsable remplit la "
            "fiche d'évaluation avec l'avis du tuteur : maîtrise des tâches, respect des "
            "procédures, comportement avec les clients et l'équipe. Il en discute avec le "
            "salarié, qui signe la fiche et peut y ajouter ses observations."
        ),
        h1("9. Questions fréquentes"),
        *faq(
            [
                (
                    "Un salarié de Kouri peut-il recommander un candidat ?",
                    "Oui, mais il ne participe pas à sa sélection et le candidat suit le même "
                    "parcours que les autres.",
                ),
                (
                    "Un stagiaire peut-il être embauché à la fin de son stage ?",
                    "Oui, s'il postule à une offre publiée et réussit la sélection ; la durée du "
                    "stage peut alors être prise en compte dans la période d'essai.",
                ),
                (
                    "Que se passe-t-il si le nouvel arrivant n'a pas encore signé la charte ?",
                    "Il ne reçoit aucun accès au logiciel tant que la signature n'est pas faite.",
                ),
                (
                    "Combien de temps dure un recrutement ?",
                    "En général six à huit semaines entre la publication de l'offre et la prise "
                    "de poste, selon le nombre de candidatures reçues.",
                ),
                (
                    "Un candidat peut-il connaître les motifs de son échec ?",
                    "Oui, sur demande écrite, la Direction des ressources humaines lui indique "
                    "les critères sur lesquels sa candidature a été moins bien notée.",
                ),
            ]
        ),
        h1("10. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Février 2021", "Création de la procédure"],
                [
                    "1.2",
                    SPEC.approval_date,
                    "Grille d'évaluation commune et parcours d'intégration",
                ],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
