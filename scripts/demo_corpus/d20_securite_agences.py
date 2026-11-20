"""Document n° 20 — Sécurité des agences (SEC-PRO-02, 5 pages).

Réponses attendues : personnes nécessaires pour ouvrir le coffre (page 2) et
conduite en cas de braquage (page 4).
"""

from scripts.demo_corpus.facts import DOCUMENTS
from scripts.demo_corpus.render import Page, bullets, callout, faq, h1, h2, p, table, title_block

SPEC = DOCUMENTS[20]


def build_pages() -> list[Page]:
    """Construit les 5 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Cette procédure protège les personnes, les fonds et les informations dans les "
            "agences de Kouri Épargne & Crédit. Elle couvre la garde du coffre, l'ouverture "
            "et la fermeture des locaux, les transports de fonds et la conduite à tenir en "
            "cas d'agression. Sa première règle est simple : la vie et la santé des personnes "
            "passent toujours avant les fonds, qui sont assurés."
        ),
        h1("2. Dispositifs de sécurité"),
        table(
            [
                ["Dispositif", "Rôle", "Vérification"],
                [
                    "Vidéosurveillance",
                    "Filmer l'entrée, les guichets et l'accès au coffre ; "
                    "images conservées un mois",
                    "Chaque semaine",
                ],
                [
                    "Système d'alarme",
                    "Détecter les intrusions hors des heures d'ouverture et "
                    "alerter en cas d'agression",
                    "Chaque mois",
                ],
                [
                    "Coffre-fort",
                    "Double serrure à code et temporisation d'ouverture",
                    "Chaque année",
                ],
                ["Guichets protégés", "Vitrage et passe-documents", "Chaque année"],
                [
                    "Gardiennage",
                    "Agent de sécurité aux heures d'ouverture et de nuit",
                    "Rapport quotidien",
                ],
            ],
            (0.22, 0.56, 0.22),
        ),
        h2("Responsabilités"),
        p(
            "Le chef d'agence est responsable de la sécurité de son agence. Le responsable "
            "sécurité de l'institution fixe les règles, contrôle leur application et "
            "organise les formations. Chaque salarié applique les consignes et signale toute "
            "anomalie : porte forcée, caméra en panne, comportement suspect."
        ),
        callout(
            "Discrétion",
            [
                "Les horaires des transports de fonds, les codes et l'emplacement des "
                "dispositifs de sécurité ne sont jamais évoqués devant des clients ni hors de "
                "l'agence, y compris en famille ou sur les réseaux sociaux.",
            ],
        ),
        h2("Assurance"),
        p(
            "Les fonds en caisse, au coffre et en transport sont assurés. L'assurance ne "
            "joue que si les procédures ont été respectées, d'où l'importance de les "
            "appliquer à la lettre."
        ),
    ]


def _p2() -> Page:
    return [
        h1("3. Le coffre"),
        p(
            "L'ouverture du coffre exige la présence de deux personnes : le chef d'agence et "
            "le caissier principal. Chacun détient une seule des deux combinaisons et "
            "compose la sienne hors de la vue de l'autre. Aucune personne ne peut ouvrir "
            "le coffre seule, ni connaître les deux combinaisons."
        ),
        h2("Remplacement d'un détenteur"),
        p(
            "En cas d'absence de l'un des détenteurs, la combinaison est confiée à son "
            "remplaçant désigné par écrit par la Direction des opérations, qui la lui remet "
            "sous pli scellé. Les combinaisons sont changées à chaque départ ou mutation "
            "d'un détenteur, et au moins une fois par an."
        ),
        h2("Temporisation"),
        p(
            "Le coffre est équipé d'un retard d'ouverture de quelques minutes, affiché à "
            "l'entrée de l'agence. Cette temporisation décourage les agresseurs, qui ne "
            "peuvent obtenir l'ouverture immédiate. Elle ne peut être désactivée par "
            "personne en agence."
        ),
        h2("Registre du coffre"),
        table(
            [
                ["Information notée", "Pourquoi"],
                ["Date et heure d'ouverture et de fermeture", "Reconstituer tout incident"],
                ["Noms et signatures des deux personnes présentes", "Prouver le double contrôle"],
                [
                    "Montants entrés et sortis, avec le billetage",
                    "Rapprocher avec les caisses (voir OP-PRO-02)",
                ],
                ["Observations", "Signaler une anomalie de fonctionnement"],
            ],
            (0.5, 0.5),
        ),
        h2("Contenu du coffre"),
        p(
            "Le coffre ne contient que les fonds de l'agence, les doubles des clés sous pli "
            "scellé et les valeurs confiées par les clients dans le cadre d'un contrat "
            "(titres déposés en garantie). Aucun objet personnel n'y est rangé."
        ),
        h2("Accès à la zone du coffre"),
        p(
            "La zone du coffre n'est accessible qu'au personnel habilité. Aucun client, "
            "prestataire ou visiteur n'y entre, même accompagné, sauf intervention de "
            "maintenance autorisée par la Direction des opérations."
        ),
        h2("Ouverture hors des horaires"),
        p(
            "Le coffre n'est jamais ouvert en dehors des heures de travail, sauf urgence "
            "décidée par la Direction des opérations. L'ouverture est alors signalée à "
            "l'agent de sécurité et consignée au registre."
        ),
        h2("Panne du coffre"),
        p(
            "Si le coffre ne s'ouvre pas, aucune tentative de forçage n'est faite. Le "
            "chef d'agence prévient la Direction des opérations, qui envoie le "
            "prestataire de maintenance ; les guichets fonctionnent avec les fonds "
            "disponibles."
        ),
    ]


def _p3() -> Page:
    return [
        h1("4. Ouverture et fermeture de l'agence"),
        h2("Le matin"),
        *bullets(
            [
                "Deux salariés au moins arrivent ensemble ; l'un observe les abords pendant "
                "que l'autre ouvre.",
                "En cas d'anomalie (porte forcée, inconnu qui attend), ils n'entrent pas, "
                "s'éloignent et préviennent le chef d'agence et la police.",
                "L'alarme est désarmée avec le code personnel, puis les locaux sont "
                "inspectés avant l'arrivée des autres salariés.",
            ]
        ),
        h2("Le soir"),
        *bullets(
            [
                "Le chef d'agence vérifie que plus aucun client ni visiteur n'est présent.",
                "Les fonds sont rangés au coffre après l'arrêté des caisses.",
                "Les fenêtres, les portes et le local technique sont fermés ; l'alarme est "
                "armée ; deux salariés au moins quittent l'agence ensemble.",
            ]
        ),
        h1("5. Transports de fonds"),
        p(
            "Les transports de fonds entre le siège et les agences sont confiés à un "
            "prestataire spécialisé. Les horaires et les itinéraires varient et ne sont "
            "communiqués qu'au chef d'agence et au caissier principal, le jour même. Aucun "
            "salarié ne transporte seul des fonds de l'institution."
        ),
        h2("Réception d'un transport"),
        table(
            [
                ["Étape", "Contrôle"],
                ["Arrivée du convoi", "Vérification de l'identité des convoyeurs"],
                ["Remise", "Sacs scellés, numéros des scellés comparés au bordereau"],
                ["Comptage", "Au coffre, par deux personnes, avant signature du bordereau"],
            ],
            (0.3, 0.7),
        ),
        h2("Visiteurs et prestataires"),
        p(
            "Les visiteurs sont accueillis dans les espaces publics. Un prestataire n'accède "
            "aux zones de caisse ou au local technique qu'accompagné, après vérification de "
            "son ordre d'intervention."
        ),
        h2("Codes de l'alarme"),
        p(
            "Chaque salarié autorisé dispose d'un code personnel, qui permet de savoir "
            "qui a armé ou désarmé l'alarme. Le code est désactivé le jour du départ du "
            "salarié."
        ),
        h2("Clés de l'agence"),
        p(
            "Les clés des portes extérieures sont détenues par le chef d'agence et son "
            "adjoint. Une clé perdue entraîne le changement de la serrure dans la "
            "journée."
        ),
    ]


def _p4() -> Page:
    return [
        h1("6. En cas de braquage"),
        p(
            "En cas de braquage, ne pas résister : obéir calmement aux agresseurs, ne pas "
            "faire de geste brusque, ne pas les regarder fixement. Déclencher l'alarme "
            "silencieuse seulement si c'est possible sans prendre de risque, c'est-à-dire "
            "sans être vu. Remettre les fonds demandés sans discuter : ils sont assurés."
        ),
        h2("Pendant l'agression"),
        *bullets(
            [
                "Observer discrètement : nombre d'agresseurs, taille, voix, vêtements, armes.",
                "Ne pas ouvrir le coffre plus vite que la temporisation ne le permet.",
                "Protéger les clients en leur demandant calmement de rester immobiles.",
            ]
        ),
        h2("Après le départ des agresseurs"),
        table(
            [
                ["Ordre", "Action"],
                [
                    "1",
                    "Fermer les portes de l'agence et ne laisser entrer que les secours et "
                    "la police",
                ],
                ["2", "Porter secours aux blessés et appeler les secours"],
                ["3", "Prévenir la police, le chef d'agence et la Direction des opérations"],
                ["4", "Ne toucher à rien : préserver les traces et les images"],
                ["5", "Demander aux témoins de rester ou de laisser leurs coordonnées"],
                ["6", "Chaque témoin note seul ce qu'il a vu, sans en discuter avec les autres"],
            ],
            (0.1, 0.9),
        ),
        h2("Soutien aux salariés"),
        p(
            "Un braquage est une épreuve. Les salariés concernés sont reçus par la Direction "
            "des ressources humaines dans les jours qui suivent et peuvent bénéficier d'un "
            "soutien psychologique pris en charge par l'institution. Ils ne reprennent leur "
            "poste au guichet qu'avec leur accord."
        ),
        callout(
            "À ne jamais faire",
            [
                "Poursuivre les agresseurs, tenter de les désarmer, ou parler de l'incident "
                "aux journalistes : seule la Direction générale communique.",
            ],
        ),
        h2("Déclaration et enquête"),
        p(
            "Le chef d'agence rédige un rapport détaillé dans les vingt-quatre heures. "
            "L'agence reste fermée tant que la police n'a pas terminé ses constatations. "
            "Le montant volé est établi par un arrêté de caisse contradictoire."
        ),
        h2("Reprise de l'activité"),
        p(
            "L'agence ne rouvre qu'après accord de la Direction des opérations, une fois "
            "les constatations terminées, les fonds recomptés et le personnel en état de "
            "reprendre."
        ),
    ]


def _p5() -> Page:
    return [
        h1("7. Autres situations"),
        table(
            [
                ["Situation", "Conduite à tenir"],
                [
                    "Colis ou sac abandonné",
                    "Ne pas y toucher, éloigner les personnes, prévenir la police",
                ],
                [
                    "Client agressif",
                    "Rester calme, ne pas répondre aux provocations, appeler "
                    "le chef d'agence et l'agent de sécurité",
                ],
                [
                    "Troubles dans le quartier",
                    "Fermer l'agence sur décision du chef d'agence, "
                    "informer la Direction des opérations",
                ],
                [
                    "Tentative d'intrusion de nuit",
                    "L'agent de sécurité alerte la police et le "
                    "chef d'agence, sans intervenir seul",
                ],
                ["Repérage suspect", "Noter la description et l'heure, prévenir le chef d'agence"],
            ],
            (0.3, 0.7),
        ),
        h1("8. Formation et exercices"),
        p(
            "Chaque salarié en agence suit une formation à la sécurité lors de son "
            "intégration, puis un rappel annuel. Un exercice de simulation d'agression est "
            "organisé une fois par an dans chaque agence, en dehors des heures d'ouverture."
        ),
        h2("Agents de sécurité"),
        p(
            "Les agents de sécurité contrôlent l'entrée, surveillent les abords et "
            "interviennent en cas d'incident, sans jamais mettre en danger les clients. "
            "Ils ne manipulent pas de fonds et ne quittent pas leur poste sans être "
            "remplacés."
        ),
        h2("Vérification des dispositifs"),
        p(
            "Le chef d'agence vérifie chaque semaine que les caméras enregistrent et "
            "chaque mois que l'alarme fonctionne. Toute panne est signalée le jour même à"
            " la Direction des opérations."
        ),
        h1("9. Questions fréquentes"),
        *faq(
            [
                (
                    "Un client demande où se trouve le coffre.",
                    "Ne répondez pas et signalez la question au chef d'agence.",
                ),
                (
                    "Puis-je arriver seul le matin si mon collègue est en retard ?",
                    "Non. Attendez à distance de l'agence, dans un lieu sûr.",
                ),
            ]
        ),
        h1("10. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Février 2022", "Création de la procédure"],
                ["1.2", SPEC.approval_date, "Temporisation du coffre et soutien aux salariés"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
