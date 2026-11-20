"""Document n° 1 — Règlement intérieur (RH-REG-01, 8 pages).

Réponses attendues : horaires du vendredi (page 2) et échelle des sanctions (page 7).
"""

from scripts.demo_corpus.facts import DOCUMENTS
from scripts.demo_corpus.render import Page, bullets, callout, h1, h2, p, table, title_block

SPEC = DOCUMENTS[1]


def build_pages() -> list[Page]:
    """Construit les 8 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6(), _p7(), _p8()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("Préambule"),
        p(
            "Le présent règlement intérieur fixe les règles d'organisation du travail, "
            "d'hygiène, de sécurité et de discipline applicables au sein de Kouri Épargne & "
            "Crédit S.A. Il est établi conformément au Code du travail en vigueur en "
            "République du Tchad, après consultation des délégués du personnel, et déposé "
            "auprès de l'inspection du travail compétente."
        ),
        h2("Champ d'application"),
        p(
            "Il s'applique à toute personne qui travaille dans les locaux de l'institution, au "
            "siège comme en agence : salariés permanents ou temporaires, stagiaires, "
            "personnels mis à disposition. Les règles d'hygiène et de sécurité s'imposent "
            "aussi aux prestataires et aux visiteurs pendant leur présence dans nos locaux."
        ),
        h2("Opposabilité et affichage"),
        p(
            "Le règlement est affiché dans chaque agence, à un endroit accessible au "
            "personnel, et remis à tout nouvel embauché qui en accuse réception par écrit. "
            "Nul ne peut se prévaloir de son ignorance. Les notes de service prises pour son "
            "application ont la même valeur que le règlement lui-même."
        ),
        h1("Plan du règlement"),
        table(
            [
                ["Titre", "Objet"],
                [
                    "I. Durée et horaires de travail",
                    "Horaires, pointage, retards, heures supplémentaires, permanences",
                ],
                ["II. Absences et congés", "Justification des absences, abandon de poste"],
                [
                    "III. Hygiène, santé et sécurité",
                    "Prévention, tenue, secourisme, visites médicales, accidents",
                ],
                [
                    "IV. Discipline générale",
                    "Confidentialité, conflits d'intérêts, biens et documents de l'institution",
                ],
                ["V. Relations avec la clientèle", "Accueil, neutralité, manipulation des fonds"],
                ["VI. Sanctions disciplinaires", "Fautes, échelle des sanctions, retenues"],
                [
                    "VII. Droits de la défense",
                    "Procédure disciplinaire, représentation du personnel",
                ],
                ["VIII. Dispositions finales", "Entrée en vigueur et modifications"],
            ],
            (0.38, 0.62),
        ),
    ]


def _p2() -> Page:
    return [
        h1("Titre I — Durée et horaires de travail"),
        h2("Article 1 — Durée du travail"),
        p(
            "La durée hebdomadaire de travail effectif est de 37 h 30, répartie du lundi au "
            "vendredi. Le temps de pause n'est pas compté comme du travail effectif. Les "
            "horaires ci-dessous s'appliquent à l'ensemble du personnel du siège et des "
            "agences, sauf affectation particulière notifiée par écrit."
        ),
        h2("Article 2 — Horaires du personnel"),
        table(
            [
                ["Jours", "Horaires du personnel", "Pause"],
                ["Du lundi au jeudi", "De 7 h 30 à 16 h 30", "Une heure, par roulement"],
                ["Vendredi", "De 7 h 00 à 12 h 30", "Sans pause"],
                ["Samedi et dimanche", "Repos hebdomadaire", "Permanences (article 6)"],
            ],
            (0.3, 0.35, 0.35),
        ),
        p(
            "Les horaires d'ouverture des agences au public sont fixés par note de service. "
            "Ils peuvent être adaptés pendant certaines périodes de l'année ; la note de "
            "service applicable précise alors les horaires du public et du personnel."
        ),
        h2("Article 3 — Pointage"),
        p(
            "Chaque salarié enregistre son heure d'arrivée et de départ sur le registre ou le "
            "badgeur de son site. Pointer pour un collègue est interdit. Le chef d'agence ou "
            "le responsable de service vise le registre chaque fin de semaine."
        ),
        h2("Article 4 — Retards"),
        p(
            "Tout retard est signalé au responsable dès que possible, par téléphone ou par "
            "message. Les retards répétés et non justifiés constituent une faute (titre VI). "
            "Le temps perdu peut être récupéré avec l'accord du responsable."
        ),
        h2("Article 5 — Heures supplémentaires"),
        p(
            "Les heures supplémentaires ne sont effectuées qu'à la demande écrite du "
            "responsable. Elles sont rémunérées ou récupérées selon les majorations prévues "
            "par la réglementation, et enregistrées dans le registre prévu à cet effet."
        ),
        h2("Article 6 — Permanences"),
        p(
            "Lorsqu'une agence ouvre exceptionnellement en dehors des jours habituels, une "
            "équipe de permanence est désignée par roulement. Le planning est affiché au "
            "moins une semaine à l'avance ; les heures de permanence sont récupérées dans la "
            "semaine qui suit, ou payées comme heures supplémentaires."
        ),
        callout(
            "Ponctualité",
            [
                "L'agence ouvre à l'heure annoncée au public : le personnel est donc à son "
                "poste, caisse prête, avant l'ouverture des portes. Un guichet ouvert en "
                "retard est un client mal servi.",
            ],
        ),
    ]


def _p3() -> Page:
    return [
        h1("Titre II — Absences et congés"),
        h2("Article 7 — Principe"),
        p(
            "Toute absence doit être autorisée à l'avance ou, si elle est imprévisible, "
            "signalée au responsable le jour même, avant l'heure de prise de poste lorsque "
            "c'est possible. Une absence non signalée et non justifiée est une absence "
            "irrégulière, qui entraîne une retenue sur salaire et peut être sanctionnée."
        ),
        h2("Article 8 — Justification"),
        table(
            [
                ["Motif d'absence", "Justificatif à fournir", "Délai de remise"],
                ["Maladie", "Certificat médical", "Dans les deux jours qui suivent l'arrêt"],
                ["Événement familial", "Acte d'état civil ou attestation", "Au retour du salarié"],
                ["Convocation officielle", "Copie de la convocation", "Avant l'absence"],
                [
                    "Accident du travail",
                    "Déclaration et certificat initial",
                    "Le jour même (article 15)",
                ],
            ],
            (0.25, 0.4, 0.35),
        ),
        h2("Article 9 — Congés"),
        p(
            "Les congés annuels, les congés pour événements familiaux et les autorisations "
            "d'absence sont régis par la procédure de demande de congés (voir RH-PRO-02), qui "
            "fixe les durées, les délais de dépôt et le circuit de validation. Aucun congé ne "
            "peut être pris sans validation écrite préalable, sauf urgence familiale dûment "
            "justifiée a posteriori."
        ),
        h2("Article 10 — Périodes chargées"),
        p(
            "Pendant les fins de mois, les périodes de paie des clients salariés et la "
            "rentrée scolaire, les congés peuvent être limités pour garantir la continuité du "
            "service. Le planning des présences est alors publié au moins deux semaines à "
            "l'avance par le chef d'agence."
        ),
        h2("Article 11 — Abandon de poste"),
        p(
            "Le salarié qui quitte son poste sans autorisation pendant les heures de travail, "
            "ou qui ne reprend pas le travail à la fin d'un congé sans justification, est en "
            "situation d'abandon de poste. Après une mise en demeure restée sans réponse "
            "pendant trois jours ouvrables, la procédure disciplinaire du titre VII est "
            "engagée."
        ),
        h2("Article 12 — Obligations civiques et religieuses"),
        p(
            "Les absences pour remplir une obligation civique (convocation d'un tribunal, "
            "élection en tant qu'assesseur) sont autorisées sur justificatif. Les "
            "aménagements d'horaires pour les pratiques religieuses sont organisés par le "
            "responsable, dans la mesure compatible avec la continuité du service."
        ),
        h2("Article 12 bis — Retenues pour absence"),
        p(
            "Une absence irrégulière donne lieu à une retenue sur salaire proportionnelle à "
            "la durée de l'absence. Le salarié est informé par écrit avant la retenue et "
            "peut présenter un justificatif dans les deux jours ouvrables ; la retenue est "
            "annulée si le justificatif est accepté."
        ),
    ]


def _p4() -> Page:
    return [
        h1("Titre III — Hygiène, santé et sécurité"),
        h2("Article 13 — Prévention"),
        p(
            "Chacun veille à sa propre sécurité et à celle des autres. Les consignes "
            "d'incendie et d'évacuation (voir SEC-CON-01) et les règles de sécurité des "
            "agences (voir SEC-PRO-02) sont obligatoires. Les issues de secours, les "
            "extincteurs et les tableaux électriques doivent rester dégagés en permanence."
        ),
        h2("Article 14 — Interdictions"),
        *bullets(
            [
                "Fumer dans les locaux, y compris dans les toilettes et les réserves.",
                "Introduire ou consommer de l'alcool ou des produits stupéfiants, ou se "
                "présenter au travail sous leur emprise.",
                "Introduire une arme dans les locaux, à l'exception des agents de sécurité "
                "autorisés dans le cadre de leur mission.",
                "Neutraliser un dispositif de sécurité : caméra, serrure, alarme, détecteur.",
            ]
        ),
        h2("Article 15 — Accidents du travail"),
        p(
            "Tout accident survenu au travail ou sur le trajet est déclaré le jour même au "
            "responsable, qui informe la Direction des ressources humaines. Un registre des "
            "accidents est tenu dans chaque site, et la déclaration aux organismes sociaux "
            "est faite dans les délais réglementaires."
        ),
        h2("Article 16 — Secourisme"),
        p(
            "Chaque agence dispose d'une trousse de premiers secours, vérifiée chaque mois "
            "par le chef d'agence, et d'au moins un salarié formé aux gestes de premiers "
            "secours. Son nom est affiché près de la trousse. En cas de malaise d'un client "
            "ou d'un collègue, il est appelé en priorité, avant les secours extérieurs si "
            "la situation n'est pas grave."
        ),
        h2("Article 17 — Suivi médical"),
        p(
            "Chaque salarié passe une visite médicale d'embauche, puis une visite périodique "
            "organisée par l'institution. La visite est obligatoire et se déroule pendant le "
            "temps de travail. Le médecin peut proposer un aménagement de poste."
        ),
        h2("Article 18 — Propreté des locaux et tenue"),
        p(
            "Chacun maintient son poste de travail propre et rangé ; aucun repas n'est pris "
            "aux guichets. Le personnel en contact avec la clientèle porte une tenue "
            "correcte, la tenue traditionnelle étant admise, et le badge nominatif fourni "
            "par l'institution, restitué au départ du salarié."
        ),
        h2("Article 18 bis — Droit d'alerte"),
        p(
            "Tout salarié qui a un motif raisonnable de penser qu'une situation présente un "
            "danger grave pour sa vie ou sa santé en avertit immédiatement son responsable. "
            "Il peut se retirer de cette situation sans encourir de sanction, à condition de "
            "ne pas créer un nouveau danger pour autrui."
        ),
    ]


def _p5() -> Page:
    return [
        h1("Titre IV — Discipline générale"),
        h2("Article 19 — Confidentialité"),
        p(
            "Le personnel est tenu au secret professionnel sur toutes les informations "
            "relatives aux clients, à leurs comptes et à leurs crédits, ainsi qu'aux affaires "
            "internes de l'institution. Cette obligation demeure après la fin du contrat. "
            "Les règles d'usage des outils informatiques et de protection des données sont "
            "précisées dans la charte informatique (voir SI-CHA-01) et dans la politique de "
            "protection des données personnelles (voir CONF-POL-02)."
        ),
        h2("Article 20 — Conflits d'intérêts"),
        p(
            "Tout salarié déclare par écrit à son responsable toute situation où son intérêt "
            "personnel, familial ou commercial pourrait influencer une décision : dossier de "
            "crédit d'un proche, relation d'affaires avec un fournisseur, activité "
            "parallèle. Le dossier concerné est alors confié à un autre collègue."
        ),
        h2("Article 21 — Cadeaux et avantages"),
        p(
            "Aucun cadeau, aucune commission et aucun service, quelle qu'en soit la valeur, "
            "ne peuvent être acceptés d'un client, d'un demandeur de crédit ou d'un "
            "fournisseur. Un cadeau reçu malgré tout est remis au responsable, qui le restitue "
            "ou le remet à une œuvre sociale, et l'incident est consigné."
        ),
        h2("Article 22 — Biens de l'institution"),
        p(
            "Le matériel, les véhicules, les fournitures et les fonds confiés au personnel "
            "sont utilisés uniquement pour les besoins du service. Leur usage personnel, leur "
            "sortie des locaux sans autorisation ou leur détérioration volontaire constituent "
            "des fautes. Les véhicules de service ne transportent aucune personne étrangère "
            "au service."
        ),
        h2("Article 23 — Documents et registres"),
        p(
            "Les dossiers des clients, les registres et les pièces comptables ne quittent "
            "jamais les locaux, sauf transfert organisé entre sites. Toute correction d'un "
            "document se fait par une mention datée et signée, sans rature ni effacement. "
            "Détruire ou modifier un document pour masquer une erreur est une faute grave."
        ),
        h2("Article 24 — Téléphone et réseaux sociaux"),
        p(
            "L'usage du téléphone personnel est limité au strict nécessaire pendant les "
            "heures d'accueil du public. Il est interdit de publier sur les réseaux sociaux "
            "des photos des locaux, des documents internes ou toute information sur un "
            "client, même sans le nommer."
        ),
        h2("Article 24 bis — Activités extérieures"),
        p(
            "Une activité professionnelle exercée en dehors de l'institution est déclarée à "
            "la Direction des ressources humaines. Elle est interdite si elle concurrence "
            "l'institution (prêt d'argent, tontine organisée à titre lucratif, change) ou si "
            "elle empêche le salarié de respecter ses horaires."
        ),
    ]


def _p6() -> Page:
    return [
        h1("Titre V — Relations avec la clientèle"),
        h2("Article 25 — Accueil"),
        p(
            "Chaque client est accueilli avec courtoisie, dans la langue de son choix "
            "lorsque c'est possible (français, arabe tchadien ou langue locale), et servi "
            "dans l'ordre d'arrivée, sauf priorité accordée aux personnes âgées, aux femmes "
            "enceintes et aux personnes en situation de handicap."
        ),
        h2("Article 26 — Neutralité et égalité de traitement"),
        p(
            "Le personnel s'abstient de toute discrimination fondée sur l'origine, la "
            "religion, le sexe, l'appartenance politique ou la situation sociale. Il ne fait "
            "état d'aucune préférence politique ou religieuse dans l'exercice de ses "
            "fonctions."
        ),
        h2("Article 27 — Opérations interdites avec les clients"),
        *bullets(
            [
                "Prêter de l'argent à un client, lui en emprunter, ou se porter garant pour "
                "lui à titre personnel.",
                "Conserver des fonds, des pièces d'identité ou des carnets appartenant à un "
                "client en dehors des procédures prévues.",
                "Effectuer une opération sur le compte d'un client sans sa demande signée.",
                "Recevoir un client en dehors des locaux pour une opération de caisse.",
            ]
        ),
        h2("Article 28 — Manipulation des fonds"),
        p(
            "Seuls les caissiers et les personnes habilitées manipulent les fonds, selon les "
            "procédures de caisse (voir OP-PRO-02). Tout écart de caisse est déclaré "
            "immédiatement, sans attendre la fin de la journée. Les fonds ne sont jamais "
            "transportés par un salarié seul en dehors du circuit prévu."
        ),
        h2("Article 29 — Réclamations"),
        p(
            "Toute réclamation d'un client, même formulée oralement, est enregistrée et "
            "traitée selon la procédure de traitement des réclamations (voir QUA-PRO-01). Un "
            "salarié mis en cause par une réclamation ne la traite pas lui-même."
        ),
        h2("Article 30 — Harcèlement et violence"),
        p(
            "Le harcèlement moral ou sexuel, les menaces, les insultes et toute forme de "
            "violence, envers un collègue comme envers un client, sont interdits. La victime "
            "ou le témoin peut saisir son responsable, la Direction des ressources humaines "
            "ou un délégué du personnel. Aucune sanction ne peut frapper la personne qui a "
            "signalé de bonne foi."
        ),
        h2("Article 30 bis — Documents remis aux clients"),
        p(
            "Tout document remis à un client (reçu, contrat, tableau d'amortissement) est "
            "complet, lisible et signé. Le personnel explique son contenu oralement si le "
            "client le souhaite, dans une langue qu'il comprend."
        ),
    ]


def _p7() -> Page:
    return [
        h1("Titre VI — Sanctions disciplinaires"),
        h2("Article 31 — Principes"),
        p(
            "Constitue une faute tout manquement au présent règlement, aux notes de service "
            "ou aux procédures internes. La sanction est proportionnée à la gravité de la "
            "faute, compte tenu des circonstances et des antécédents du salarié. Une même "
            "faute ne peut être sanctionnée deux fois."
        ),
        h2("Article 32 — Échelle des sanctions"),
        p(
            "Les sanctions applicables sont, par ordre de gravité : l'avertissement écrit, "
            "la mise à pied de 1 à 3 jours sans salaire, et le licenciement."
        ),
        table(
            [
                ["Sanction", "Exemples de fautes", "Autorité compétente"],
                [
                    "Avertissement écrit",
                    "Retards répétés, tenue négligée, usage abusif du téléphone",
                    "Responsable hiérarchique, après avis de la DRH",
                ],
                [
                    "Mise à pied",
                    "Absence irrégulière, refus d'appliquer une procédure, "
                    "récidive après avertissement",
                    "Direction des ressources humaines",
                ],
                [
                    "Licenciement",
                    "Détournement de fonds, violation du secret professionnel, "
                    "violence, faute grave",
                    "Directeur général",
                ],
            ],
            (0.22, 0.48, 0.30),
        ),
        p(
            "Les sanctions sont appliquées dans l'ordre de l'échelle, sauf faute grave qui "
            "peut justifier directement un licenciement. Une mise à pied conservatoire peut "
            "être prononcée en attendant la décision, lorsque la présence du salarié "
            "compromettrait l'enquête ou la sécurité des fonds."
        ),
        h2("Article 33 — Fautes graves"),
        *bullets(
            [
                "Tout détournement, même partiel ou temporaire, de fonds ou de biens.",
                "La falsification d'un document, d'une signature ou d'une écriture comptable.",
                "La divulgation d'informations confidentielles sur un client.",
                "L'octroi ou le décaissement d'un crédit en violation délibérée des procédures.",
            ]
        ),
        h2("Article 34 — Responsabilité pécuniaire"),
        p(
            "Un manquant de caisse ou un préjudice causé par une négligence peut être mis à "
            "la charge du salarié, dans les limites prévues par la réglementation, après "
            "procès-verbal contradictoire. Une retenue sur salaire n'est jamais une sanction "
            "en soi : elle répare un préjudice constaté."
        ),
        h2("Article 35 — Effacement"),
        p(
            "Un avertissement est effacé du dossier après deux années sans nouvelle sanction. "
            "Une mise à pied est effacée après trois années dans les mêmes conditions."
        ),
        callout(
            "Rappel",
            [
                "Aucune amende ni sanction pécuniaire ne peut être infligée en dehors des "
                "cas prévus par le présent titre.",
            ],
        ),
    ]


def _p8() -> Page:
    return [
        h1("Titre VII — Droits de la défense"),
        h2("Article 36 — Procédure"),
        table(
            [
                ["Étape", "Contenu"],
                [
                    "Convocation",
                    "Lettre remise contre décharge, indiquant l'objet, la date et "
                    "le lieu de l'entretien, au moins trois jours ouvrables à l'avance",
                ],
                [
                    "Entretien",
                    "Le salarié présente ses explications ; il peut se faire "
                    "assister d'un délégué du personnel ou d'un collègue de son choix",
                ],
                [
                    "Décision",
                    "Notifiée par écrit et motivée, au plus tôt le lendemain de "
                    "l'entretien et au plus tard un mois après",
                ],
                [
                    "Recours",
                    "Recours écrit auprès du Directeur général sous quinze jours, sans "
                    "effet suspensif",
                ],
            ],
            (0.2, 0.8),
        ),
        h2("Article 37 — Représentation du personnel"),
        p(
            "Les délégués du personnel présentent les réclamations individuelles et "
            "collectives relatives aux conditions de travail. Ils sont reçus par la "
            "Direction générale au moins une fois par trimestre, et disposent du temps "
            "nécessaire à leur mandat dans les limites prévues par la réglementation."
        ),
        h2("Article 37 bis — Égalité professionnelle"),
        p(
            "Les femmes et les hommes bénéficient de l'égalité de traitement pour le "
            "recrutement, la rémunération, la formation et la promotion. Toute inégalité "
            "constatée est signalée à la Direction des ressources humaines, qui en rend "
            "compte aux délégués du personnel."
        ),
        h1("Titre VIII — Dispositions finales"),
        h2("Article 38 — Entrée en vigueur"),
        p(
            f"Le présent règlement entre en vigueur le {SPEC.effective_date}. Il annule et "
            "remplace le règlement précédent ainsi que toutes les notes de service "
            "contraires."
        ),
        h2("Article 39 — Modifications"),
        p(
            "Toute modification suit la même procédure que l'adoption du règlement : avis "
            "des délégués du personnel, dépôt auprès de l'inspection du travail et affichage. "
            "Les notes de service d'application sont diffusées par la Direction des "
            "ressources humaines."
        ),
        h2("Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Mai 2019", "Adoption du premier règlement intérieur"],
                ["2.0", "Janvier 2023", "Ajout des règles sur les réseaux sociaux"],
                [
                    "2.1",
                    SPEC.approval_date,
                    "Précisions sur les cadeaux, le harcèlement et les permanences",
                ],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
