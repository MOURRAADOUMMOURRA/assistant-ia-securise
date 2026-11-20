"""Document n° 16 — Procédure d'ouverture de compte (OP-PRO-01, 5 pages).

Réponses attendues : pièces à fournir (page 2) et compte d'un mineur (page 4).
"""

from scripts.demo_corpus.facts import DOCUMENTS, fcfa
from scripts.demo_corpus.render import Page, bullets, callout, faq, h1, h2, p, table, title_block

SPEC = DOCUMENTS[16]


def build_pages() -> list[Page]:
    """Construit les 5 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Cette procédure décrit l'ouverture d'un compte chez Kouri Épargne & Crédit : "
            "pièces à demander, contrôles à réaliser, saisie dans le logiciel et remise des "
            "documents au client. Le compte est la porte d'entrée vers tous nos services : "
            "épargne, crédit, réception du salaire, transferts. Une ouverture bien faite "
            "protège le client comme l'institution."
        ),
        h1("2. Qui peut ouvrir un compte"),
        table(
            [
                ["Type de titulaire", "Particularités", "Section"],
                ["Personne majeure", "Titulaire seul, ou compte joint à deux", "Section 3"],
                ["Personne mineure", "Ouvert et géré par son représentant légal", "Section 5"],
                [
                    "Groupement ou association",
                    "Statuts, liste des membres, personnes habilitées à signer",
                    "Section 6",
                ],
                [
                    "Entreprise individuelle",
                    "Pièces du dirigeant et justificatif d'activité",
                    "Section 6",
                ],
            ],
            (0.3, 0.5, 0.2),
        ),
        h2("Principes"),
        *bullets(
            [
                "Le client est toujours reçu en personne : aucun compte n'est ouvert à "
                "distance ou par un intermédiaire.",
                "L'identité est vérifiée sur l'original des documents, jamais sur une copie.",
                "Les règles de connaissance du client (voir CONF-POL-01) s'appliquent dès "
                "l'ouverture.",
                "L'ouverture d'un compte est gratuite ; les tarifs des services figurent dans "
                "la grille des taux et frais en vigueur.",
            ]
        ),
        callout(
            "Refus d'ouverture",
            [
                "Un compte n'est pas ouvert si l'identité ne peut être établie, si le client "
                "refuse de répondre aux questions de connaissance client, ou s'il figure sur "
                "une liste de sanctions. Le refus est consigné et signalé à la conformité.",
            ],
        ),
        h2("Délai d'ouverture"),
        p(
            "Un dossier complet permet d'ouvrir le compte en une seule visite, en général"
            " en moins d'une heure. Si une pièce manque, le chargé de clientèle remet au "
            "client la liste écrite de ce qu'il doit apporter et conserve la fiche "
            "commencée pendant un mois."
        ),
    ]


def _p2() -> Page:
    return [
        h1("3. Pièces à fournir par une personne majeure"),
        p(
            "Pour ouvrir un compte, le client présente une pièce d'identité valide, 2 photos "
            "d'identité récentes, et un justificatif de domicile ou, à défaut, une "
            "attestation du chef de quartier. Ces pièces suffisent dans la grande majorité "
            "des cas ; le chargé de clientèle n'en exige pas d'autres sans motif."
        ),
        table(
            [
                ["Pièce", "Documents acceptés", "Contrôle"],
                [
                    "Identité",
                    "Carte nationale d'identité, passeport, carte de réfugié, carte consulaire",
                    "Validité, photo ressemblante, absence de rature",
                ],
                ["Photos", "Photos d'identité en couleur, de face", "Récentes et ressemblantes"],
                [
                    "Domicile",
                    "Facture d'eau ou d'électricité, contrat de bail, ou attestation de résidence",
                    "Moins de trois mois, nom du client",
                ],
            ],
            (0.15, 0.5, 0.35),
        ),
        h2("Le justificatif de domicile"),
        p(
            "Beaucoup de clients n'ont ni facture ni bail à leur nom. L'attestation de "
            "résidence délivrée par l'autorité du quartier est alors acceptée, si elle porte "
            "un cachet lisible, une date et la signature de l'autorité. En cas de doute, le "
            "chargé de clientèle peut demander à un agent de crédit de passer vérifier "
            "l'adresse lors d'une visite dans le quartier."
        ),
        h2("Informations demandées au client"),
        *bullets(
            [
                "Adresse précise et numéro de téléphone joignable.",
                "Profession ou activité, et lieu d'exercice.",
                "Origine habituelle des fonds qui seront déposés.",
                "Utilisation prévue du compte : épargne, crédit, salaire, activité.",
            ]
        ),
        h2("Compte joint"),
        p(
            "Un compte joint est ouvert au nom de deux personnes majeures qui fournissent "
            "chacune les pièces ci-dessus. Les titulaires précisent si chacun peut opérer "
            "seul ou si les deux signatures sont nécessaires ; ce choix figure dans la "
            "convention et ne peut être modifié qu'avec l'accord des deux."
        ),
        h2("Pièces d'identité en mauvais état"),
        p(
            "Une pièce déchirée, illisible ou dont la photo ne permet pas de reconnaître "
            "le client n'est pas acceptée, même si elle est encore valide. Le client est "
            "invité à la faire renouveler ; l'ouverture est reportée."
        ),
        h2("Client qui ne sait pas lire"),
        p(
            "Le chargé de clientèle lit à voix haute la convention de compte et les "
            "tarifs, dans une langue que le client comprend, en présence d'un témoin "
            "choisi par le client. La mention de cette lecture figure sur la convention."
        ),
    ]


def _p3() -> Page:
    return [
        h1("4. Étapes de l'ouverture"),
        table(
            [
                ["Étape", "Action", "Responsable"],
                [
                    "1. Accueil",
                    "Explication des produits et des tarifs, remise de la grille",
                    "Chargé de clientèle",
                ],
                [
                    "2. Vérification",
                    "Contrôle des originaux, copie des pièces, entretien de connaissance client",
                    "Chargé de clientèle",
                ],
                [
                    "3. Filtrage",
                    "Recherche du nom dans les listes de sanctions",
                    "Logiciel, automatiquement",
                ],
                ["4. Saisie", "Création de la fiche client et du compte", "Chargé de clientèle"],
                [
                    "5. Signature",
                    "Convention de compte et spécimen de signature ou d'empreinte",
                    "Client",
                ],
                ["6. Validation", "Contrôle de la fiche et des pièces", "Chef d'agence"],
                [
                    "7. Remise",
                    "Carte de membre, livret, copie de la convention",
                    "Chargé de clientèle",
                ],
            ],
            (0.17, 0.58, 0.25),
        ),
        h2("Spécimen de signature"),
        p(
            "Le client signe trois fois le carton de spécimen. S'il ne sait pas signer, son "
            "empreinte digitale est apposée en présence de deux témoins, salariés de "
            "l'agence, qui signent également. Le spécimen est numérisé et apparaît à l'écran "
            "du caissier à chaque retrait."
        ),
        h2("Dépôt initial"),
        p(
            f"Un dépôt initial de {fcfa(2_000)} est demandé ; il reste sur le compte et "
            "appartient au client. Il peut être versé dans les sept jours qui suivent "
            "l'ouverture. Le compte est actif dès la validation par le chef d'agence."
        ),
        h2("Contrôles du chef d'agence"),
        *bullets(
            [
                "Toutes les pièces obligatoires sont copiées et lisibles.",
                "La fiche est complète et cohérente avec les pièces.",
                "Le filtrage des listes de sanctions a été effectué et ne donne pas d'alerte.",
            ]
        ),
        h2("Saisie dans le logiciel"),
        p(
            "Les informations sont saisies exactement comme elles figurent sur la pièce "
            "d'identité : orthographe du nom, date et lieu de naissance, numéro de la "
            "pièce. Une erreur de saisie peut empêcher plus tard le client de retirer son"
            " argent ou de prouver son identité."
        ),
        h2("Remise des documents au client"),
        p(
            "Le client repart avec sa carte de membre, son livret, une copie de la "
            "convention signée et la grille des tarifs. Le chargé de clientèle lui "
            "explique comment déposer, retirer et consulter son solde, et lui présente "
            "les produits d'épargne."
        ),
        h2("Archivage du dossier"),
        p(
            "Le dossier papier est classé dans l'armoire fermée à clé de l'agence ; les "
            "copies numérisées sont rattachées à la fiche dans le logiciel le jour même."
        ),
    ]


def _p4() -> Page:
    return [
        h1("5. Compte d'un mineur"),
        p(
            "Le compte d'un mineur est ouvert par son parent ou son tuteur légal, qui "
            "présente sa propre pièce d'identité, l'acte de naissance de l'enfant et, pour un "
            "tuteur, le jugement qui le désigne. Le parent ou le tuteur est le seul "
            "signataire du compte jusqu'à ses 18 ans : l'enfant ne peut effectuer aucune "
            "opération seul."
        ),
        h2("À la majorité"),
        p(
            "À sa majorité, le jeune titulaire se présente avec sa pièce d'identité. Le "
            "compte est transformé en compte ordinaire à son seul nom, et le représentant "
            "légal perd ses pouvoirs. Le solde accumulé appartient au jeune titulaire."
        ),
        h2("Opérations autorisées"),
        table(
            [
                ["Opération", "Autorisée", "Condition"],
                ["Dépôt", "Oui", "Par toute personne, au nom de l'enfant"],
                ["Retrait", "Oui", "Par le représentant légal, dans l'intérêt de l'enfant"],
                ["Crédit", "Non", "Aucun crédit au nom d'un mineur"],
                ["Dépôt à terme", "Oui", "Signé par le représentant légal"],
            ],
            (0.25, 0.15, 0.6),
        ),
        h1("6. Groupements et entreprises"),
        p(
            "Pour un groupement, une association ou une coopérative, le chargé de "
            "clientèle demande les statuts, le procès-verbal de désignation des "
            "responsables, la liste des membres et les pièces d'identité des personnes "
            "habilitées à signer. Au moins deux signatures sont exigées pour tout retrait."
        ),
        p(
            "Pour une entreprise individuelle, les pièces du dirigeant sont complétées par "
            "un justificatif d'activité : registre de commerce, patente ou, pour une petite "
            "activité informelle, attestation de l'autorité du marché."
        ),
        h2("Fin de la représentation légale"),
        p(
            "Si le représentant légal décède ou perd son autorité parentale, le compte du"
            " mineur est bloqué jusqu'à la présentation de la décision désignant le "
            "nouveau représentant. Aucune opération n'est possible entre-temps, sauf les "
            "dépôts."
        ),
        h2("Procuration"),
        p(
            "Un titulaire majeur peut donner procuration à une personne de confiance. La "
            "procuration est signée à l'agence par les deux personnes, qui présentent "
            "leurs pièces d'identité ; elle précise les opérations autorisées et peut "
            "être révoquée à tout moment."
        ),
        h2("Groupement dont les responsables changent"),
        p(
            "Le groupement présente le procès-verbal de l'assemblée qui a désigné les "
            "nouveaux responsables. Les anciens spécimens de signature sont désactivés le"
            " jour même."
        ),
    ]


def _p5() -> Page:
    return [
        h1("7. Vie du compte"),
        h2("Mise à jour des informations"),
        p(
            "Le client signale tout changement d'adresse, de téléphone ou de situation. Le "
            "chargé de clientèle met la fiche à jour sur présentation du justificatif. Les "
            "fréquences de révision selon le niveau de risque sont fixées par CONF-POL-01."
        ),
        h2("Compte inactif et clôture"),
        p(
            "Un compte sans mouvement pendant douze mois devient inactif ; le client est "
            "contacté pour le réactiver ou le clôturer. La clôture est demandée par écrit "
            "par le titulaire ; le solde lui est remis après déduction des frais éventuels, "
            "et la carte de membre est restituée."
        ),
        h2("Décès du titulaire"),
        p(
            "Au décès du titulaire, le compte est bloqué dès que l'agence en est informée. Le "
            "solde n'est remis qu'aux héritiers désignés par un acte officiel, après "
            "remboursement des crédits éventuels non couverts par l'assurance."
        ),
        h2("Comptes en double"),
        p(
            "Avant toute ouverture, le logiciel recherche si le client a déjà une fiche. "
            "Un client ne peut avoir qu'une seule fiche ; un nouveau compte est rattaché "
            "à sa fiche existante."
        ),
        h2("Confidentialité"),
        p(
            "Le solde et les opérations d'un client ne sont communiqués qu'à lui-même ou "
            "à son mandataire, jamais à un membre de sa famille sans procuration."
        ),
        h1("8. Questions fréquentes"),
        *faq(
            [
                (
                    "Un étranger peut-il ouvrir un compte ?",
                    "Oui, avec un passeport ou une carte consulaire en cours de validité et un "
                    "justificatif de domicile au Tchad.",
                ),
                (
                    "Peut-on ouvrir un compte pour un parent âgé qui ne se déplace pas ?",
                    "Non : le titulaire doit être présent. Une procuration peut ensuite être "
                    "donnée à l'agence, en présence du titulaire.",
                ),
                (
                    "Un client peut-il avoir plusieurs comptes ?",
                    "Oui, un compte courant et un ou plusieurs comptes d'épargne, sous une même "
                    "fiche client.",
                ),
            ]
        ),
        h1("9. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["2.0", "Juin 2023", "Compte joint et spécimen numérisé"],
                ["2.3", SPEC.approval_date, "Justificatif de domicile simplifié"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
