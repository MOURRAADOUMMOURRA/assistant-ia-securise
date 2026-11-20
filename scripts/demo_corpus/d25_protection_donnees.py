"""Document n° 25 — Protection des données personnelles (CONF-POL-02, 5 pages).

Réponses attendues : référent données personnelles (page 2) et conservation des
données d'un ancien client (page 3).
"""

from scripts.demo_corpus.facts import DOCUMENTS
from scripts.demo_corpus.render import Page, bullets, callout, faq, h1, h2, p, table, title_block

SPEC = DOCUMENTS[25]


def build_pages() -> list[Page]:
    """Construit les 5 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Kouri Épargne & Crédit collecte de nombreuses informations sur ses clients, ses "
            "salariés et ses partenaires : identité, adresse, revenus, opérations, "
            "photographies. Cette politique fixe les règles qui protègent ces données "
            "personnelles, conformément à la réglementation applicable, et les droits des "
            "personnes concernées."
        ),
        h1("2. Principes"),
        table(
            [
                ["Principe", "Ce qu'il signifie en pratique"],
                [
                    "Finalité",
                    "Collecter une donnée seulement pour un but précis : ouvrir un "
                    "compte, analyser un crédit, payer un salaire",
                ],
                ["Minimisation", "Ne demander que les informations nécessaires à ce but"],
                ["Exactitude", "Tenir les données à jour et corriger les erreurs"],
                [
                    "Conservation limitée",
                    "Supprimer les données à la fin de la durée prévue (section 5)",
                ],
                [
                    "Sécurité",
                    "Protéger les données contre la perte, le vol et l'accès non autorisé",
                ],
                ["Transparence", "Informer les personnes de l'usage de leurs données"],
            ],
            (0.27, 0.73),
        ),
        h2("Champ d'application"),
        p(
            "La politique s'applique à toutes les données personnelles traitées par "
            "l'institution, sur papier comme dans le logiciel, au siège comme en agence, et "
            "à toute personne qui y a accès, y compris les prestataires."
        ),
        h2("Données sensibles"),
        p(
            "Certaines données exigent une protection renforcée : informations de santé "
            "(par exemple pour l'assurance décès-invalidité), données judiciaires, "
            "données sur les enfants. Elles ne sont accessibles qu'aux personnes qui en "
            "ont strictement besoin."
        ),
        h2("Base légale"),
        p(
            "Chaque traitement repose sur une base légale : exécution d'un contrat, "
            "obligation légale, intérêt légitime de l'institution ou consentement de la "
            "personne."
        ),
    ]


def _p2() -> Page:
    return [
        h1("3. Rôles et responsabilités"),
        p(
            "Le référent données personnelles est le responsable de la conformité. Il "
            "conseille les services, tient le registre des traitements, traite les demandes "
            "des personnes concernées et gère les violations de données. Il rend compte "
            "chaque année au comité d'audit et des risques."
        ),
        table(
            [
                ["Acteur", "Responsabilité"],
                ["Direction générale", "Responsable des traitements au nom de l'institution"],
                ["Responsable de la conformité", "Pilotage de la politique (voir ci-dessus)"],
                ["Service informatique", "Sécurité technique, sauvegardes, droits d'accès"],
                ["Chefs de service et d'agence", "Application de la politique dans leur périmètre"],
                [
                    "Chaque salarié",
                    "Confidentialité et usage des données pour le seul besoin du service",
                ],
            ],
            (0.35, 0.65),
        ),
        h1("4. Données traitées"),
        table(
            [
                ["Catégorie de personnes", "Exemples de données", "Finalité"],
                [
                    "Clients",
                    "Identité, adresse, activité, revenus, opérations",
                    "Gestion des comptes et des crédits, obligations légales",
                ],
                ["Cautions", "Identité, revenus, engagement signé", "Garantie des crédits"],
                ["Salariés", "Identité, contrat, paie, évaluation", "Gestion du personnel"],
                ["Candidats", "Curriculum vitae, résultats des tests", "Recrutement"],
                ["Visiteurs", "Images de vidéosurveillance", "Sécurité des agences"],
            ],
            (0.22, 0.42, 0.36),
        ),
        h2("Registre des traitements"),
        p(
            "Le registre décrit chaque traitement : finalité, catégories de données, "
            "personnes ayant accès, durée de conservation, mesures de sécurité. Il est "
            "mis à jour à chaque nouveau traitement."
        ),
        h2("Nouveaux projets"),
        p(
            "Tout nouveau projet qui implique des données personnelles (nouvelle "
            "application, nouveau formulaire) est soumis au responsable de la conformité "
            "avant sa mise en œuvre."
        ),
        h2("Formation"),
        p(
            "Tout le personnel est formé à la protection des données lors de son "
            "intégration, puis lors de la formation annuelle prévue au plan de formation."
        ),
    ]


def _p3() -> Page:
    return [
        h1("5. Durées de conservation"),
        p(
            "Les données d'un ancien client sont conservées 10 ans après la clôture du "
            "compte, pour répondre aux obligations légales et comptables et aux éventuels "
            "litiges. Passé ce délai, elles sont détruites ou rendues anonymes. Les autres "
            "durées sont les suivantes :"
        ),
        table(
            [
                ["Données", "Durée de conservation"],
                ["Dossier d'un client en activité", "Pendant toute la relation"],
                ["Dossier de crédit remboursé", "Avec le dossier du client"],
                ["Candidatures non retenues", "Six mois, sauf accord du candidat"],
                ["Images de vidéosurveillance", "Un mois, sauf incident"],
                ["Dossiers de réclamation", "Cinq ans"],
                ["Dossiers du personnel", "Durée légale après le départ du salarié"],
            ],
            (0.5, 0.5),
        ),
        h2("Destruction"),
        p(
            "Les documents papier sont détruits au broyeur ou par un prestataire qui remet "
            "un certificat de destruction. Les données numériques sont effacées de façon "
            "définitive, y compris des sauvegardes lors de leur rotation. Le registre des "
            "destructions est tenu par le service informatique."
        ),
        h2("Archives"),
        p(
            "Les dossiers clos sont transférés aux archives du siège, dans un local fermé "
            "dont l'accès est enregistré. Ils ne sont consultés que pour un motif précis : "
            "contrôle, litige, demande d'une autorité."
        ),
        h2("Calcul de la durée"),
        p(
            "La durée de conservation court à partir de l'événement indiqué : clôture du "
            "compte, fin du contrat de travail, décision sur une candidature. La date est"
            " notée dans le logiciel pour permettre la suppression automatique."
        ),
        h2("Gel des données"),
        p(
            "En cas de litige ou de demande d'une autorité, la destruction des données "
            "concernées est suspendue jusqu'à la fin de la procédure, sur décision du "
            "responsable de la conformité."
        ),
        h2("Contrôle"),
        p(
            "Chaque année, le service informatique et la conformité vérifient que les "
            "données arrivées en fin de durée ont bien été supprimées."
        ),
        h2("Données des cautions"),
        p(
            "Les données d'une caution sont conservées avec le dossier du crédit qu'elle "
            "a garanti, puis supprimées selon la même règle que les données du client."
        ),
    ]


def _p4() -> Page:
    return [
        h1("6. Droits des personnes"),
        table(
            [
                ["Droit", "Contenu"],
                ["Information", "Savoir quelles données sont collectées et pourquoi"],
                ["Accès", "Obtenir une copie des données qui la concernent"],
                ["Rectification", "Faire corriger une donnée inexacte"],
                ["Opposition", "S'opposer à certains usages, par exemple aux messages commerciaux"],
                [
                    "Effacement",
                    "Demander la suppression des données qui ne sont plus "
                    "nécessaires, sous réserve des obligations de conservation",
                ],
            ],
            (0.25, 0.75),
        ),
        h2("Exercer ses droits"),
        p(
            "La personne adresse sa demande à son agence ou au siège, par écrit, avec une "
            "copie de sa pièce d'identité. La demande est transmise le jour même au "
            "responsable de la conformité, qui y répond dans un délai d'un mois. La réponse "
            "est gratuite."
        ),
        h2("Information des clients"),
        p(
            "À l'ouverture du compte, le client reçoit une notice qui explique l'usage de ses "
            "données, leur durée de conservation et la façon d'exercer ses droits. La "
            "notice est affichée dans chaque agence."
        ),
        callout(
            "Secret professionnel",
            [
                "Les droits des personnes ne remettent pas en cause le secret professionnel : "
                "un client n'obtient jamais les données d'un autre client, même membre de sa "
                "famille.",
            ],
        ),
        h2("Vérification de l'identité du demandeur"),
        p(
            "Avant toute réponse, l'agence vérifie que le demandeur est bien la personne "
            "concernée, ou son représentant légal muni d'un justificatif. Aucune "
            "information n'est donnée par téléphone."
        ),
        h2("Refus d'une demande"),
        p(
            "Une demande peut être refusée lorsqu'elle porte atteinte aux droits d'un "
            "tiers ou lorsque la loi impose la conservation des données. Le refus est "
            "motivé par écrit."
        ),
        h2("Messages commerciaux"),
        p(
            "Les messages présentant de nouveaux produits ne sont envoyés qu'aux clients "
            "qui ne s'y sont pas opposés. Chaque message indique comment ne plus en "
            "recevoir."
        ),
        h2("Rectification"),
        p(
            "Une donnée inexacte est corrigée dès que le justificatif est fourni. La "
            "correction est datée dans le logiciel et la personne en est informée."
        ),
    ]


def _p5() -> Page:
    return [
        h1("7. Sécurité et violations de données"),
        p(
            "Une violation de données est un incident qui entraîne la perte, la divulgation "
            "ou l'accès non autorisé à des données personnelles : tablette volée, document "
            "envoyé à la mauvaise personne, accès frauduleux. Tout salarié qui en constate "
            "une la signale immédiatement au service informatique et à la conformité."
        ),
        *bullets(
            [
                "La conformité évalue la gravité et les personnes concernées.",
                "Les mesures pour limiter les conséquences sont prises sans délai.",
                "Les personnes concernées et les autorités sont informées lorsque la "
                "réglementation l'exige.",
                "L'incident est inscrit dans le registre des violations.",
            ]
        ),
        h2("Prestataires"),
        p(
            "Un prestataire qui accède à des données personnelles signe un engagement de "
            "confidentialité et de sécurité. Il ne peut utiliser les données que pour la "
            "mission confiée et doit les restituer ou les détruire à la fin du contrat."
        ),
        h2("Transferts hors du pays"),
        p(
            "Aucune donnée de client n'est transférée hors du pays, sauf obligation "
            "légale ou accord écrit de la Direction générale après avis de la conformité."
        ),
        h2("Sanctions"),
        p(
            "Le non-respect de la politique constitue une faute disciplinaire (voir RH-"
            "REG-01) et peut engager la responsabilité de son auteur."
        ),
        h2("Sauvegarde des engagements"),
        p(
            "Les engagements de confidentialité signés par les salariés et les "
            "prestataires sont conservés par la Direction des ressources humaines et la "
            "conformité."
        ),
        h1("8. Questions fréquentes"),
        *faq(
            [
                (
                    "Un parent demande le solde du compte de son fils majeur.",
                    "Refusez poliment : seule une procuration permet de lui répondre.",
                ),
                (
                    "Puis-je photographier la pièce d'identité d'un client avec mon téléphone ?",
                    "Non. Utilisez uniquement l'application prévue sur la tablette de service.",
                ),
            ]
        ),
        h1("9. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Juillet 2023", "Création de la politique"],
                ["1.2", SPEC.approval_date, "Durées de conservation et violations"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
