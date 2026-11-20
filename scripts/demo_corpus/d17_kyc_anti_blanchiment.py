"""Document n° 17 — Connaissance client (KYC) et lutte anti-blanchiment (CONF-POL-01, 8 p.).

Réponses attendues : seuil de déclaration interne d'une opération en espèces (page 4)
et mise à jour du dossier d'un client à risque élevé (page 6).
"""

from scripts.demo_corpus.facts import DOCUMENTS, fcfa
from scripts.demo_corpus.render import Page, bullets, callout, faq, h1, h2, p, table, title_block

SPEC = DOCUMENTS[17]
CASH_THRESHOLD = 5_000_000


def build_pages() -> list[Page]:
    """Construit les 8 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6(), _p7(), _p8()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Cette politique définit comment Kouri Épargne & Crédit connaît ses clients et "
            "détecte les opérations qui pourraient servir à blanchir de l'argent ou à "
            "financer le terrorisme. Elle traduit en règles pratiques les obligations "
            "prévues par la réglementation applicable aux établissements de microfinance. "
            "Chaque salarié en contact avec les clients ou leurs opérations est concerné."
        ),
        h1("2. Qu'est-ce que le blanchiment ?"),
        p(
            "Blanchir de l'argent, c'est faire passer des fonds d'origine illicite (vol, "
            "corruption, trafic, fraude) pour des fonds légitimes, en les faisant transiter "
            "par des comptes, des crédits ou des achats. Une microfinance peut être utilisée "
            "à son insu : dépôts répétés en espèces, remboursements anticipés inexpliqués, "
            "comptes ouverts pour d'autres personnes."
        ),
        h2("Les trois piliers de la politique"),
        table(
            [
                ["Pilier", "Contenu", "Sections"],
                [
                    "Connaître le client",
                    "Identifier, vérifier, comprendre l'activité et l'origine des fonds",
                    "3 et 4",
                ],
                [
                    "Surveiller les opérations",
                    "Repérer les opérations inhabituelles ou importantes",
                    "5 et 6",
                ],
                [
                    "Déclarer",
                    "Transmettre les soupçons à la conformité, sans alerter le client",
                    "7",
                ],
            ],
            (0.27, 0.58, 0.15),
        ),
        callout(
            "Responsabilité personnelle",
            [
                "Un salarié qui aide sciemment une opération de blanchiment, ou qui avertit "
                "un client d'une déclaration le concernant, s'expose à des sanctions pénales, "
                "en plus des sanctions disciplinaires.",
            ],
        ),
        h2("Champ d'application"),
        p(
            "La politique s'applique à toutes les agences et à tous les produits : "
            "comptes, épargne, crédit, transferts. Elle s'impose aussi aux prestataires "
            "qui agissent pour le compte de l'institution."
        ),
    ]


def _p2() -> Page:
    return [
        h1("3. Identification et vérification"),
        p(
            "Aucune relation d'affaires ne commence sans identification complète du client. "
            "Les pièces exigées à l'ouverture du compte sont décrites dans la procédure "
            "d'ouverture de compte (voir OP-PRO-01). La présente politique y ajoute les "
            "questions qui permettent de comprendre le client."
        ),
        table(
            [
                ["Question", "Pourquoi la poser"],
                [
                    "Quelle est votre activité, et où l'exercez-vous ?",
                    "Vérifier que les montants déposés correspondent à l'activité",
                ],
                [
                    "D'où proviennent les fonds que vous déposerez ?",
                    "Repérer une origine floue ou incohérente",
                ],
                ["Comment utiliserez-vous le compte ?", "Établir un profil d'opérations attendu"],
                [
                    "Agissez-vous pour vous-même ou pour une autre personne ?",
                    "Identifier le bénéficiaire réel",
                ],
                [
                    "Exercez-vous une fonction publique importante ?",
                    "Repérer les personnes politiquement exposées",
                ],
            ],
            (0.5, 0.5),
        ),
        h2("Le bénéficiaire réel"),
        p(
            "Le bénéficiaire réel est la personne qui, en définitive, possède ou contrôle "
            "les fonds. Pour un groupement ou une entreprise, ce sont les personnes qui le "
            "dirigent ou en tirent profit. Le chargé de clientèle les identifie et note "
            "leur identité dans la fiche. Si un client semble agir pour un tiers qu'il "
            "refuse de nommer, la relation n'est pas engagée."
        ),
        h2("Personnes politiquement exposées"),
        p(
            "Les personnes qui exercent ou ont exercé une fonction publique importante "
            "(ministre, parlementaire, haut magistrat, officier supérieur, dirigeant "
            "d'entreprise publique), ainsi que leurs proches, sont automatiquement classées "
            "en risque élevé. L'ouverture de leur compte est autorisée par le Directeur "
            "général, après avis de la conformité."
        ),
        h2("Vérification des documents"),
        p(
            "Le chargé de clientèle compare la photo au client présent, vérifie la date "
            "de validité et recherche les signes de falsification : rature, police de "
            "caractères différente, photo collée. En cas de doute, il demande une seconde"
            " pièce et prévient le chef d'agence."
        ),
        h2("Refus de répondre"),
        p(
            "Un client qui refuse d'indiquer son activité ou l'origine de ses fonds ne "
            "peut pas ouvrir de compte. Si le refus intervient en cours de relation, la "
            "situation est signalée à la conformité."
        ),
        h2("Mandataires"),
        p(
            "Lorsqu'une personne agit pour le titulaire avec une procuration, son "
            "identité est vérifiée comme celle d'un client, et ses liens avec le "
            "titulaire sont notés dans la fiche."
        ),
    ]


def _p3() -> Page:
    return [
        h1("4. Classification des clients par niveau de risque"),
        p(
            "Chaque client reçoit à l'ouverture un niveau de risque, calculé par le "
            "logiciel à partir de critères objectifs et confirmé par le chargé de "
            "clientèle. Le niveau détermine la vigilance appliquée et la fréquence de "
            "révision du dossier."
        ),
        table(
            [
                ["Niveau", "Exemples de clients", "Vigilance"],
                [
                    "Faible",
                    "Salarié dont le salaire est domicilié, petit commerçant connu "
                    "du quartier, épargnant régulier",
                    "Simplifiée",
                ],
                [
                    "Moyen",
                    "Commerçant avec des volumes importants en espèces, client "
                    "résidant hors de la zone de l'agence",
                    "Normale",
                ],
                [
                    "Élevé",
                    "Personne politiquement exposée, activité à forte circulation "
                    "d'espèces, origine des fonds peu claire",
                    "Renforcée",
                ],
            ],
            (0.13, 0.62, 0.25),
        ),
        h2("Critères de classement"),
        *bullets(
            [
                "Nature de l'activité et importance des espèces dans celle-ci.",
                "Zone géographique de résidence et d'activité.",
                "Montants et fréquence des opérations attendues.",
                "Qualité de personne politiquement exposée.",
                "Comportement à l'ouverture : réticence, documents douteux, urgence.",
            ]
        ),
        h2("Vigilance renforcée"),
        p(
            "Pour un client à risque élevé, le chargé de clientèle obtient des justificatifs "
            "de l'origine des fonds (factures, actes de vente, contrats), le chef d'agence "
            "valide l'ouverture et la conformité reçoit une copie du dossier. Les opérations "
            "importantes du client sont examinées avant d'être exécutées."
        ),
        h2("Changement de niveau"),
        p(
            "Le niveau de risque est revu à chaque événement significatif : opération "
            "inhabituelle, changement d'activité, information défavorable. Un passage au "
            "niveau élevé est validé par la conformité."
        ),
        h2("Clients à vigilance simplifiée"),
        p(
            "Pour un salarié dont le salaire est domicilié et dont les opérations sont "
            "faibles et régulières, les vérifications se limitent à l'identification et "
            "aux révisions périodiques. Cette simplification cesse dès qu'une opération "
            "sort de l'ordinaire."
        ),
        h2("Rôle du logiciel"),
        p(
            "Le logiciel calcule un score à partir des critères de classement et propose "
            "un niveau. Le chargé de clientèle peut le relever, jamais l'abaisser sans "
            "l'accord de la conformité."
        ),
    ]


def _p4() -> Page:
    return [
        h1("5. Surveillance des opérations en espèces"),
        p(
            f"Toute opération en espèces d'un montant égal ou supérieur à "
            f"{fcfa(CASH_THRESHOLD)}, en dépôt comme en retrait, fait l'objet d'une "
            "déclaration interne au responsable de la conformité, le jour même, au moyen du "
            "formulaire F-CONF-01. La déclaration interne n'est pas une accusation : elle "
            "permet à la conformité d'examiner l'opération à la lumière du profil du client."
        ),
        h2("Opérations fractionnées"),
        p(
            "Plusieurs opérations plus petites, effectuées sur une courte période par le "
            "même client ou par des personnes liées, et dont le total atteint ce seuil, sont "
            "déclarées de la même façon. Le fractionnement volontaire pour rester sous le "
            "seuil est en lui-même un signal d'alerte."
        ),
        h2("Contenu de la déclaration interne"),
        table(
            [
                ["Rubrique", "Exemple"],
                ["Client et compte", "Nom, numéro de compte, niveau de risque"],
                ["Opération", "Nature, montant, date, guichet"],
                [
                    "Origine ou destination déclarée",
                    "Vente d'un lot de bétail, achat de marchandises",
                ],
                ["Justificatif présenté", "Facture, acte de vente, ou aucun"],
                ["Observation du caissier", "Comportement, cohérence avec l'activité connue"],
            ],
            (0.35, 0.65),
        ),
        h2("Conduite à tenir au guichet"),
        *bullets(
            [
                "Exécuter l'opération normalement si rien ne paraît anormal, puis déclarer.",
                "Demander poliment l'origine des fonds et un justificatif, comme pour tout client.",
                "En cas de doute sérieux, prévenir le chef d'agence avant d'exécuter.",
                "Ne jamais dire au client qu'une déclaration sera faite.",
            ]
        ),
        h2("Après la déclaration interne"),
        p(
            "La conformité accuse réception de la déclaration et l'examine dans les jours"
            " qui suivent. Elle peut demander au chef d'agence des informations "
            "complémentaires, toujours sans alerter le client."
        ),
        h2("Registre des opérations importantes"),
        p(
            "Les déclarations internes sont inscrites dans un registre tenu par la "
            "conformité : date, client, montant, suite donnée. Le registre est présenté "
            "aux autorités de contrôle sur demande."
        ),
        h2("Seuil et profil du client"),
        p(
            "Le seuil de déclaration est le même pour tous les clients. Mais une "
            "opération plus petite doit aussi être signalée si elle est incohérente avec "
            "le profil du client, par exemple un dépôt important sur le compte d'un "
            "salarié modeste."
        ),
    ]


def _p5() -> Page:
    return [
        h1("6. Signaux d'alerte"),
        p(
            "Les signaux ci-dessous ne prouvent rien à eux seuls, mais ils justifient un "
            "examen attentif. Le salarié qui en constate un le note et en parle à son chef "
            "d'agence ou directement à la conformité."
        ),
        table(
            [
                ["Situation", "Pourquoi c'est suspect"],
                [
                    "Dépôts importants sans rapport avec l'activité déclarée",
                    "Les fonds peuvent provenir d'une autre source",
                ],
                [
                    "Remboursement anticipé d'un crédit en espèces, sans explication",
                    "Le crédit peut servir à « laver » de l'argent",
                ],
                [
                    "Compte dormant qui reçoit soudain de gros montants",
                    "Compte prêté ou vendu à un tiers",
                ],
                [
                    "Client qui insiste pour éviter toute formalité",
                    "Volonté de ne pas laisser de trace",
                ],
                [
                    "Nombreux dépôts de tiers sur un même compte",
                    "Collecte de fonds pour une autre personne",
                ],
                [
                    "Transferts rapides vers des comptes sans lien apparent",
                    "Circuit de dispersion des fonds",
                ],
            ],
            (0.5, 0.5),
        ),
        h2("Crédit et blanchiment"),
        p(
            "Le crédit peut aussi être détourné : un client emprunte, puis rembourse "
            "aussitôt avec des fonds d'origine douteuse. L'agent de crédit vérifie que les "
            "remboursements proviennent de l'activité financée et signale tout "
            "remboursement anticipé important, surtout en espèces."
        ),
        h2("Financement du terrorisme"),
        p(
            "Le financement du terrorisme peut porter sur de petites sommes d'origine licite. "
            "Le filtrage des listes de sanctions, à l'ouverture et lors de chaque transfert, "
            "est donc essentiel. Toute correspondance, même partielle, avec une liste est "
            "transmise immédiatement à la conformité et l'opération est suspendue."
        ),
        h2("Transferts"),
        p(
            "Pour tout transfert, le nom du donneur d'ordre et celui du bénéficiaire sont"
            " filtrés dans les listes de sanctions. Un transfert vers une personne ou une"
            " zone signalée est suspendu et transmis à la conformité."
        ),
        h2("Que faire d'un signal d'alerte"),
        p(
            "Le salarié ne mène pas d'enquête lui-même et ne questionne pas le client de "
            "façon inhabituelle. Il note les faits, en informe la conformité et continue "
            "à servir le client normalement."
        ),
        h2("Exemples tirés de la pratique"),
        p(
            "Un commerçant de céréales dont les dépôts triplent hors saison, un compte "
            "d'étudiant qui reçoit des dépôts de nombreuses personnes, un remboursement "
            "anticipé en espèces juste après le décaissement : chacun de ces cas a "
            "justifié un examen."
        ),
        h2("Après un signalement"),
        p(
            "Le salarié n'a pas à connaître la suite donnée à son signalement. La "
            "conformité peut cependant lui demander des précisions sur ce qu'il a "
            "observé."
        ),
    ]


def _p6() -> Page:
    return [
        h1("7. Mise à jour des dossiers"),
        p(
            "Les informations sur le client vieillissent : activité, adresse, revenus. Le "
            "dossier est revu selon une fréquence qui dépend du niveau de risque. Le "
            "dossier d'un client à risque élevé est mis à jour chaque année, avec un "
            "entretien et de nouveaux justificatifs ; la mise à jour est validée par la "
            "conformité."
        ),
        table(
            [
                ["Niveau de risque", "Fréquence de révision", "Validation"],
                ["Faible", "Tous les cinq ans, ou à l'occasion d'un crédit", "Chargé de clientèle"],
                ["Moyen", "Tous les trois ans", "Chef d'agence"],
                ["Élevé", "Annuelle (voir ci-dessus)", "Responsable de la conformité"],
            ],
            (0.25, 0.45, 0.3),
        ),
        h2("Déroulement d'une mise à jour"),
        *bullets(
            [
                "Le logiciel signale chaque mois les dossiers à revoir.",
                "Le chargé de clientèle contacte le client et vérifie ses pièces.",
                "Les changements sont saisis et les copies des nouvelles pièces classées.",
                "Le niveau de risque est confirmé ou modifié.",
            ]
        ),
        h2("Client injoignable"),
        p(
            "Si le client ne peut être joint ou refuse la mise à jour, son compte est placé "
            "sous surveillance : les opérations au crédit restent possibles, mais les "
            "retraits importants sont soumis à l'accord du chef d'agence jusqu'à la mise à "
            "jour complète."
        ),
        h2("Documents d'identité expirés"),
        p(
            "Une pièce d'identité expirée est remplacée dès la prochaine visite du client. "
            "Aucun nouveau crédit n'est accordé tant que la pièce n'est pas valide."
        ),
        h2("Événements qui déclenchent une révision"),
        p(
            "En dehors des révisions périodiques, le dossier est revu lors d'une demande "
            "de crédit importante, d'une opération inhabituelle, d'un changement "
            "d'activité ou d'une information publique défavorable sur le client."
        ),
        h2("Traçabilité"),
        p(
            "Chaque révision est datée et signée dans le logiciel, avec les pièces "
            "nouvelles. Le contrôle interne vérifie chaque année un échantillon de "
            "dossiers revus."
        ),
        h2("Révision allégée"),
        p(
            "Pour les clients à faible risque, la révision peut se faire à l'occasion "
            "d'une visite au guichet : le chargé de clientèle confirme l'adresse, le "
            "téléphone et l'activité, puis valide la fiche."
        ),
    ]


def _p7() -> Page:
    return [
        h1("8. Déclaration de soupçon"),
        p(
            "Lorsque la conformité, après examen d'une déclaration interne ou d'un "
            "signalement, a des motifs de soupçonner que des fonds proviennent d'une "
            "activité illicite, elle effectue une déclaration de soupçon auprès de la "
            "cellule nationale de renseignement financier, selon les formes prévues par la "
            "réglementation."
        ),
        table(
            [
                ["Étape", "Responsable", "Délai"],
                ["Signalement interne", "Tout salarié", "Le jour même"],
                ["Examen du dossier", "Responsable de la conformité", "Sans délai"],
                [
                    "Décision de déclarer ou de classer",
                    "Responsable de la conformité",
                    "Dès que l'examen est terminé",
                ],
                [
                    "Déclaration à la cellule de renseignement financier",
                    "Responsable de la conformité",
                    "Selon la réglementation",
                ],
                ["Archivage", "Conformité", "Dossier séparé, accès restreint"],
            ],
            (0.45, 0.33, 0.22),
        ),
        h2("Confidentialité absolue"),
        p(
            "L'existence d'un signalement ou d'une déclaration ne doit jamais être révélée "
            "au client ni à des tiers. Les dossiers de déclaration sont conservés à part, "
            "sous la seule responsabilité de la conformité. Le salarié qui a signalé de "
            "bonne foi est protégé."
        ),
        h2("Rôle du responsable de la conformité"),
        p(
            "Le responsable de la conformité anime le dispositif, examine les signalements, "
            "décide des déclarations, tient les registres et présente chaque année un "
            "rapport au Conseil d'administration. Il dispose d'un accès à tous les dossiers "
            "et opérations nécessaires à sa mission."
        ),
        h2("Opération suspendue"),
        p(
            "Lorsque la conformité suspend une opération, le chef d'agence indique au "
            "client qu'un contrôle interne est en cours, sans autre précision. La "
            "suspension est levée dès que la conformité le décide."
        ),
        h2("Coopération avec les autorités"),
        p(
            "Les demandes des autorités compétentes sont traitées par la conformité, avec"
            " l'accord de la Direction générale. Les informations sont transmises dans "
            "les formes et délais prévus."
        ),
        h2("Indicateurs du dispositif"),
        p(
            "La conformité suit le nombre de déclarations internes, de déclarations de "
            "soupçon, de dossiers révisés dans les délais et de salariés formés. Ces "
            "indicateurs figurent dans son rapport annuel."
        ),
        h2("Protection du déclarant"),
        p(
            "Aucune action ne peut être engagée contre un salarié ou contre l'institution"
            " pour une déclaration faite de bonne foi, même si les soupçons ne sont "
            "finalement pas confirmés."
        ),
    ]


def _p8() -> Page:
    return [
        h1("9. Conservation et formation"),
        p(
            "Les documents d'identification et les pièces relatives aux opérations sont "
            "conservés pendant la durée prévue par la réglementation et par la politique de "
            "protection des données personnelles (voir CONF-POL-02). Ils sont présentés sur "
            "demande aux autorités habilitées."
        ),
        p(
            "Tout le personnel suit chaque année la formation anti-blanchiment prévue au "
            "plan de formation (voir RH-PLF-2026). Les nouveaux arrivants suivent un module "
            "d'initiation avant toute opération seule avec la clientèle."
        ),
        h2("Sanctions internes"),
        p(
            "Le non-respect de la politique (ouverture sans pièces, absence de "
            "déclaration interne, information donnée au client) est une faute "
            "disciplinaire, sanctionnée selon le règlement intérieur (voir RH-REG-01)."
        ),
        h2("Contrôle du dispositif"),
        p(
            "L'audit interne vérifie chaque année le fonctionnement du dispositif dans "
            "toutes les agences et présente ses conclusions au Conseil d'administration."
        ),
        h2("Points de contact"),
        p(
            "Pour toute question, le salarié s'adresse à son chef d'agence ou directement"
            " au responsable de la conformité, dont les coordonnées sont affichées dans "
            "chaque agence."
        ),
        h1("10. Questions fréquentes"),
        *faq(
            [
                (
                    "Un client habituel dépose une somme importante après la vente de son "
                    "bétail. Faut-il déclarer ?",
                    "Oui si le seuil est atteint : la déclaration interne est obligatoire, même "
                    "pour un client connu. Joignez si possible l'acte de vente.",
                ),
                (
                    "Puis-je refuser un dépôt ?",
                    "Seulement sur instruction du chef d'agence ou de la conformité, en cas de "
                    "soupçon sérieux ou de refus du client de justifier l'origine des fonds.",
                ),
                (
                    "Le client me demande pourquoi je pose ces questions.",
                    "Expliquez qu'elles sont posées à tous les clients, conformément à la "
                    "réglementation, et qu'elles protègent aussi leur argent.",
                ),
            ]
        ),
        h1("11. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["2.0", "Avril 2022", "Classification des clients par niveau de risque"],
                ["3.1", SPEC.approval_date, "Opérations fractionnées et filtrage des transferts"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
