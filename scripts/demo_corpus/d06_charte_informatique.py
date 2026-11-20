"""Document n° 6 — Charte informatique et sécurité des données (SI-CHA-01, 7 pages).

Réponses attendues : changement du mot de passe (page 3) et perte d'une tablette de
collecte (page 6).
"""

from scripts.demo_corpus.facts import DOCUMENTS
from scripts.demo_corpus.render import Page, bullets, callout, h1, h2, p, table, title_block

SPEC = DOCUMENTS[6]


def build_pages() -> list[Page]:
    """Construit les 7 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6(), _p7()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "La présente charte fixe les règles d'utilisation des outils informatiques de "
            "Kouri Épargne & Crédit et les mesures qui protègent les données de nos clients. "
            "Une microfinance repose sur la confiance : une fuite de données ou une fraude "
            "informatique peut ruiner des années de travail. Chaque utilisateur est donc un "
            "maillon de la sécurité."
        ),
        h1("2. Champ d'application"),
        p(
            "La charte s'applique à toute personne qui utilise un équipement ou un logiciel "
            "de l'institution : salariés, stagiaires, prestataires. Elle couvre les "
            "ordinateurs, les tablettes de collecte des agents de crédit, les téléphones de "
            "service, le réseau, la messagerie et le logiciel de gestion des comptes."
        ),
        h1("3. Trois objectifs de sécurité"),
        table(
            [
                ["Objectif", "Ce qu'il signifie", "Exemple de menace"],
                [
                    "Confidentialité",
                    "Seules les personnes autorisées accèdent aux données",
                    "Un tiers consulte le solde d'un client",
                ],
                [
                    "Intégrité",
                    "Les données ne sont modifiées que par des opérations autorisées",
                    "Une écriture est modifiée pour masquer un détournement",
                ],
                [
                    "Disponibilité",
                    "Les systèmes fonctionnent quand on en a besoin",
                    "Une panne bloque les opérations de caisse",
                ],
            ],
            (0.2, 0.42, 0.38),
        ),
        h2("Rôles"),
        p(
            "Le service informatique administre les systèmes, crée les comptes et traite les "
            "incidents. Les chefs d'agence veillent à l'application de la charte dans leur "
            "agence. Le contrôle interne vérifie périodiquement son respect et rend compte à "
            "la Direction générale."
        ),
        callout(
            "Engagement",
            [
                "Chaque utilisateur signe la présente charte avant de recevoir ses accès. "
                "Le non-respect de la charte expose à des sanctions disciplinaires (voir "
                "RH-REG-01), sans préjudice de poursuites pénales.",
            ],
        ),
    ]


def _p2() -> Page:
    return [
        h1("4. Comptes et droits d'accès"),
        *bullets(
            [
                "Chaque utilisateur dispose d'un compte nominatif. Les comptes partagés sont "
                "interdits, y compris au guichet.",
                "Les droits sont limités à ce dont le poste a besoin : un caissier ne crée "
                "pas de crédit, un agent de crédit ne valide pas d'opération de caisse.",
                "Toute modification de droits est demandée par écrit par le responsable et "
                "réalisée par le service informatique.",
                "Les comptes sont désactivés le jour même du départ d'un salarié, et "
                "suspendus pendant ses congés de plus de deux semaines.",
            ]
        ),
        h2("Profils d'accès au logiciel de gestion"),
        table(
            [
                ["Profil", "Peut faire", "Ne peut pas faire"],
                [
                    "Caissier",
                    "Dépôts, retraits, consultation des soldes",
                    "Créer un crédit, modifier un client",
                ],
                [
                    "Agent de crédit",
                    "Saisir une demande, consulter son portefeuille",
                    "Valider un décaissement, saisir une opération de caisse",
                ],
                [
                    "Chef d'agence",
                    "Valider les opérations de son agence, consulter les rapports",
                    "Modifier les paramètres du logiciel",
                ],
                [
                    "Contrôle interne",
                    "Consulter toutes les opérations",
                    "Saisir ou modifier une opération",
                ],
                [
                    "Administrateur",
                    "Gérer les comptes et les paramètres",
                    "Saisir des opérations clients",
                ],
            ],
            (0.2, 0.42, 0.38),
        ),
        p(
            "Le service informatique revoit les droits de tous les comptes chaque trimestre "
            "avec les chefs d'agence. Les droits inutiles sont retirés et la revue est "
            "consignée dans un registre."
        ),
        h2("Mutation d'un salarié"),
        p(
            "Lorsqu'un salarié change de poste ou d'agence, ses anciens droits sont retirés le "
            "jour de la mutation et les nouveaux sont ouverts sur demande du nouveau "
            "responsable. Un salarié ne cumule jamais les droits de deux postes."
        ),
        h2("Comptes techniques"),
        p(
            "Les comptes techniques utilisés par les logiciels entre eux ne servent jamais à "
            "se connecter pour travailler. Leurs mots de passe sont conservés sous scellé "
            "par le service informatique et changés à chaque départ d'un administrateur."
        ),
        h2("Accès des prestataires"),
        p(
            "Un prestataire (maintenance, éditeur du logiciel) reçoit un compte temporaire, "
            "limité à la durée de son intervention et accompagné par un membre du service "
            "informatique. Les interventions à distance sont autorisées au cas par cas et "
            "tracées dans un registre."
        ),
    ]


def _p3() -> Page:
    return [
        h1("5. Mots de passe"),
        p(
            "Le mot de passe protège le compte de l'utilisateur et engage sa responsabilité : "
            "toute opération faite avec son compte est présumée faite par lui. Il est "
            "strictement personnel et ne doit jamais être communiqué, même à un responsable "
            "ou au service informatique."
        ),
        table(
            [
                ["Règle", "Exigence"],
                ["Longueur", "12 caractères minimum"],
                ["Composition", "Lettres majuscules et minuscules, chiffres et signes"],
                [
                    "Renouvellement",
                    "Changé tous les 90 jours ; les 5 derniers mots de passe "
                    "ne peuvent pas être réutilisés",
                ],
                [
                    "Verrouillage",
                    "Compte bloqué après 5 essais erronés, débloqué par le "
                    "service informatique après vérification d'identité",
                ],
                ["Comptes administrateurs", "Double authentification obligatoire"],
            ],
            (0.28, 0.72),
        ),
        h2("Choisir un bon mot de passe"),
        p(
            "Une phrase de passe est plus facile à retenir et plus difficile à deviner qu'un "
            "mot isolé. Exemple de construction : prendre une phrase personnelle, garder les "
            "initiales, ajouter des chiffres et un signe. Les mots de passe à proscrire sont "
            "la date de naissance, le nom d'un enfant, le nom de l'agence ou une suite "
            "évidente comme « 123456 »."
        ),
        h2("Poste de travail"),
        *bullets(
            [
                "Verrouiller la session dès que l'on quitte son poste, même un instant.",
                "Ne jamais noter son mot de passe sur un papier, un bureau ou un écran.",
                "Signaler immédiatement tout mot de passe qui aurait pu être vu ou deviné, "
                "et le changer.",
            ]
        ),
        h2("Mot de passe oublié"),
        p(
            "Le salarié se présente au service informatique, ou l'appelle depuis le "
            "téléphone fixe de son agence en présence de son chef d'agence, qui confirme son "
            "identité. Un mot de passe provisoire lui est communiqué ; il doit le changer dès "
            "sa première connexion."
        ),
        h2("Poste d'un collègue"),
        p(
            "Il est interdit de travailler sur la session ouverte d'un collègue, même pour "
            "le dépanner pendant une absence courte. Chacun ferme sa session et se reconnecte "
            "avec ses propres identifiants : la traçabilité des opérations en dépend."
        ),
        h2("Codes physiques"),
        p(
            "Les codes de l'alarme, de la porte du local technique et du coffre suivent "
            "leurs propres règles de sécurité (voir SEC-PRO-02). Ils ne sont jamais "
            "enregistrés sur un ordinateur ni envoyés par message."
        ),
    ]


def _p4() -> Page:
    return [
        h1("6. Messagerie et Internet"),
        p(
            "La messagerie et l'accès à Internet sont fournis pour un usage professionnel. "
            "Un usage personnel ponctuel est toléré s'il ne gêne pas le service et ne met "
            "pas en danger la sécurité du réseau."
        ),
        h2("Reconnaître un message frauduleux"),
        *bullets(
            [
                "Il crée l'urgence : « votre compte sera bloqué dans une heure ».",
                "Il demande un mot de passe, un code ou un virement inhabituel.",
                "L'adresse de l'expéditeur ressemble à une adresse connue, à une lettre près.",
                "Il contient une pièce jointe ou un lien inattendu.",
            ]
        ),
        p(
            "En cas de doute, ne cliquez sur rien, ne répondez pas, et transférez le "
            "message au service informatique. Une demande de virement reçue par message est "
            "toujours confirmée par téléphone, à un numéro connu."
        ),
        h1("7. Logiciels et supports amovibles"),
        table(
            [
                ["Élément", "Règle"],
                ["Installation de logiciels", "Réservée au service informatique"],
                ["Clés USB personnelles", "Interdites sur les postes de l'institution"],
                [
                    "Clés USB de service",
                    "Chiffrées, fournies et inventoriées par le service informatique",
                ],
                [
                    "Applications de messagerie grand public",
                    "Interdites pour échanger des données de clients",
                ],
                ["Stockage en ligne personnel", "Interdit pour tout document de l'institution"],
            ],
            (0.35, 0.65),
        ),
        h2("Réseau et Wi-Fi"),
        p(
            "Seuls les appareils de l'institution se connectent au réseau interne. Le Wi-Fi "
            "réservé aux visiteurs, lorsqu'il existe, est séparé du réseau interne et ne "
            "donne accès à aucun serveur. Il est interdit de brancher un appareil personnel "
            "sur une prise réseau de l'agence."
        ),
        h2("Ordinateurs portables"),
        p(
            "Les ordinateurs portables sont chiffrés et ne quittent les locaux qu'avec "
            "l'accord du responsable. Ils ne sont jamais laissés visibles dans un véhicule. "
            "En déplacement, ils restent sous la surveillance de leur utilisateur."
        ),
        h2("Mises à jour"),
        p(
            "Les mises à jour de sécurité sont installées par le service informatique, de "
            "préférence en dehors des heures d'ouverture. L'utilisateur ne les reporte pas "
            "et laisse son poste allumé le soir lorsqu'une mise à jour est annoncée. Un poste "
            "qui n'a pas reçu les mises à jour depuis un mois est isolé du réseau."
        ),
    ]


def _p5() -> Page:
    return [
        h1("8. Classification et protection des données"),
        table(
            [
                ["Niveau", "Exemples", "Règles"],
                ["Public", "Grille des taux affichée, brochures", "Diffusion libre"],
                ["Interne", "Notes de service, procédures", "Personnel uniquement"],
                [
                    "Confidentiel",
                    "Données d'un client, dossier de crédit, salaires",
                    "Accès selon le profil ; jamais transmis à l'extérieur sans base légale",
                ],
                [
                    "Strictement confidentiel",
                    "Mots de passe, clés du coffre, paramètres de sécurité",
                    "Accès nominatif, registre des accès",
                ],
            ],
            (0.22, 0.4, 0.38),
        ),
        p(
            "Le traitement des données personnelles des clients et du personnel suit la "
            "politique de protection des données personnelles (voir CONF-POL-02), qui fixe "
            "notamment les durées de conservation et les droits des personnes."
        ),
        h2("Sauvegardes"),
        *bullets(
            [
                "La base du logiciel de gestion est sauvegardée chaque soir, après la "
                "clôture des caisses.",
                "Une copie chiffrée est conservée hors du siège, dans un lieu sûr.",
                "Une restauration d'essai est réalisée chaque trimestre et consignée.",
            ]
        ),
        h2("Impression et papier"),
        p(
            "Les documents confidentiels sont imprimés uniquement lorsque c'est nécessaire, "
            "récupérés aussitôt et détruits au broyeur lorsqu'ils ne servent plus. Aucun "
            "document client n'est jeté entier dans une poubelle."
        ),
        h2("Dossiers partagés"),
        p(
            "Les fichiers de travail sont enregistrés dans les dossiers partagés du service, "
            "sauvegardés chaque soir, et non sur le bureau du poste. Chaque dossier partagé a "
            "un responsable qui en contrôle l'accès ; un fichier de clients n'est jamais "
            "placé dans un dossier ouvert à tous."
        ),
        h2("Écrans et visiteurs"),
        p(
            "Les écrans des guichets sont orientés de façon à ne pas être visibles par les "
            "clients qui attendent. Aucun visiteur n'est laissé seul dans un bureau où un "
            "poste est ouvert."
        ),
        h2("Transmission de données à l'extérieur"),
        p(
            "Aucune donnée de client n'est transmise à un tiers sans base légale ou accord "
            "écrit de la Direction générale. Les transmissions réglementaires sont faites par "
            "les canaux sécurisés prévus, par la seule personne désignée. Une demande "
            "d'information émanant d'une autorité est toujours transmise à la Direction "
            "générale avant toute réponse."
        ),
    ]


def _p6() -> Page:
    return [
        h1("9. Tablettes de collecte et téléphones de service"),
        p(
            "Les agents de crédit utilisent des tablettes pour saisir les demandes et "
            "enregistrer les remboursements sur le terrain. Ces appareils contiennent des "
            "données de clients : leur protection est une priorité."
        ),
        table(
            [
                ["Mesure", "Détail"],
                ["Chiffrement", "Activé sur toutes les tablettes avant leur remise"],
                ["Code de déverrouillage", "6 chiffres au moins, différent de tout autre code"],
                ["Synchronisation", "Chaque soir, au retour à l'agence"],
                ["Applications", "Seules les applications installées par le service informatique"],
                ["Prêt de l'appareil", "Interdit, y compris à un collègue"],
            ],
            (0.3, 0.7),
        ),
        h2("Perte ou vol d'une tablette"),
        p(
            "En cas de perte ou de vol d'une tablette de collecte, l'agent prévient le "
            "service informatique sous 2 h pour un blocage à distance, par téléphone, puis "
            "confirme par écrit. Le service efface les données de l'appareil à distance dès "
            "sa prochaine connexion. En cas de vol, l'agent dépose plainte et remet une "
            "copie du récépissé à son chef d'agence."
        ),
        callout(
            "Pourquoi agir vite",
            [
                "Un appareil perdu peut être utilisé pour consulter des données ou saisir de "
                "fausses opérations. Le blocage rapide limite ce risque ; un retard de "
                "déclaration est une faute.",
            ],
        ),
        h2("Téléphones de service"),
        p(
            "Les téléphones de service sont protégés par un code et ne contiennent que les "
            "applications installées par le service informatique. Les échanges avec les "
            "clients s'y limitent aux rappels d'échéance et aux rendez-vous ; aucune donnée "
            "financière détaillée n'est envoyée par message."
        ),
        h2("Usage sur le terrain"),
        p(
            "Sur le terrain, l'agent saisit les informations devant le client, sans laisser "
            "l'écran visible par des tiers. Il ne photographie les documents d'un client "
            "qu'avec l'application prévue, jamais avec l'appareil photo du téléphone, pour "
            "que les images restent chiffrées."
        ),
        h2("Restitution du matériel"),
        p(
            "À son départ ou à sa mutation, le salarié restitue tablette, téléphone, "
            "chargeurs et clés USB de service. Le service informatique efface les appareils "
            "avant toute réattribution et met à jour l'inventaire. Un appareil non restitué "
            "est bloqué à distance et sa valeur peut être retenue sur le solde de tout compte."
        ),
    ]


def _p7() -> Page:
    return [
        h1("10. Incidents de sécurité"),
        p(
            "Tout utilisateur qui constate un incident, ou qui en soupçonne un, le signale "
            "sans délai au service informatique et à son responsable. Un signalement fait de "
            "bonne foi n'est jamais reproché, même s'il se révèle sans objet."
        ),
        table(
            [
                ["Type d'incident", "Exemples", "Premier réflexe"],
                [
                    "Virus ou logiciel malveillant",
                    "Fichiers illisibles, messages de rançon",
                    "Débrancher le câble réseau, ne pas éteindre",
                ],
                [
                    "Accès suspect",
                    "Opération inconnue sur son compte",
                    "Changer son mot de passe, prévenir",
                ],
                [
                    "Fraude par message",
                    "Demande de virement ou de code",
                    "Ne pas répondre, transférer",
                ],
                [
                    "Fuite de données",
                    "Document client envoyé à la mauvaise personne",
                    "Prévenir immédiatement",
                ],
            ],
            (0.27, 0.4, 0.33),
        ),
        h2("Contrôles"),
        p(
            "Le service informatique peut contrôler l'usage des outils pour des raisons de "
            "sécurité, dans le respect de la vie privée : journaux de connexion, analyse "
            "antivirus, revue des droits. Les contrôles nominatifs sont réalisés en présence "
            "de l'intéressé ou d'un délégué du personnel."
        ),
        h2("Après l'incident"),
        p(
            "Le service informatique analyse chaque incident, en mesure les conséquences et "
            "propose des mesures pour éviter qu'il se reproduise. Les incidents graves sont "
            "présentés à la Direction générale, et ceux qui touchent des données "
            "personnelles sont traités selon CONF-POL-02."
        ),
        h2("Sanctions"),
        p(
            "Le non-respect de la présente charte, notamment le partage d'un mot de passe ou "
            "la sortie de données de clients, est une faute disciplinaire (voir RH-REG-01). "
            "Les accès de l'utilisateur peuvent être suspendus à titre conservatoire."
        ),
        h2("Engagement de l'utilisateur"),
        p(
            "En signant la charte, l'utilisateur reconnaît en avoir reçu un exemplaire et "
            "s'engage à la respecter pendant toute la durée de son activité. La charte est "
            "rappelée lors de la formation annuelle à la sécurité informatique."
        ),
        h2("Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["2.0", "Juin 2023", "Ajout des tablettes de collecte"],
                [
                    "3.0",
                    SPEC.approval_date,
                    "Mots de passe de 12 caractères et double authentification",
                ],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
