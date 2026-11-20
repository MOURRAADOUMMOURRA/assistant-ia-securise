"""Document n° 9 — Note de service : horaires du Ramadan (NS-2026-03, 3 pages).

Réponses attendues : horaires des agences pendant le Ramadan (page 1) et ouverture
de l'agence du Grand Marché le samedi (page 2).
"""

from scripts.demo_corpus.facts import DOCUMENTS
from scripts.demo_corpus.render import Page, bullets, callout, h1, h2, p, table, title_block

SPEC = DOCUMENTS[9]


def build_pages() -> list[Page]:
    """Construit les 3 pages de la note."""
    return [_p1(), _p2(), _p3()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        p(
            "**Destinataires** : tout le personnel du siège et des agences. **Objet** : "
            "horaires d'ouverture et de travail pendant le mois de Ramadan."
        ),
        h1("1. Période concernée"),
        p(
            "Les horaires ci-dessous s'appliquent pendant tout le mois de Ramadan de l'année "
            "en cours, à partir du premier jour du jeûne annoncé par les autorités "
            "religieuses, et jusqu'à la veille de la fête de l'Aïd el-Fitr. Les dates exactes "
            "dépendant de l'observation de la lune, la Direction des ressources humaines "
            "confirme le premier et le dernier jour par message au personnel."
        ),
        h1("2. Horaires d'ouverture des agences au public"),
        table(
            [
                ["Jours", "Horaires d'ouverture au public"],
                ["Du lundi au jeudi", "De 7 h 30 à 13 h 00"],
                ["Vendredi", "De 7 h 30 à 11 h 30"],
                ["Samedi et dimanche", "Fermé, sauf disposition particulière (section 4)"],
            ],
            (0.35, 0.65),
        ),
        h1("3. Horaires du personnel"),
        p(
            "Le personnel prend son poste quinze minutes avant l'ouverture au public et le "
            "quitte après la clôture des caisses et le rangement des fonds au coffre, en "
            "principe trente minutes après la fermeture. Ces horaires remplacent "
            "temporairement ceux de l'article 2 du règlement intérieur (voir RH-REG-01)."
        ),
        p(
            "Les salariés qui ne jeûnent pas suivent les mêmes horaires, afin que les "
            "équipes restent complètes pendant les heures d'ouverture. Aucune pause repas "
            "n'est prise dans les espaces ouverts au public pendant cette période."
        ),
        h2("Opérations de fin de journée"),
        p(
            "Les dernières opérations de caisse sont acceptées jusqu'à l'heure de fermeture. "
            "L'arrêté des caisses, le rangement des fonds et la synchronisation des "
            "tablettes se font aussitôt après, afin que le personnel quitte l'agence avant "
            "les heures de forte circulation."
        ),
    ]


def _p2() -> Page:
    return [
        h1("4. Agence du Grand Marché : ouverture le samedi"),
        p(
            "L'activité commerciale du Grand Marché est particulièrement forte pendant le "
            "Ramadan et à l'approche de la fête. Pour répondre aux besoins des commerçants, "
            "l'agence du Grand Marché ouvre aussi le samedi, de 8 h à 11 h, pendant toute la "
            "période. Les autres agences restent fermées le samedi."
        ),
        h2("Opérations proposées le samedi"),
        table(
            [
                ["Opération", "Disponible le samedi"],
                ["Dépôts et retraits sur compte", "Oui"],
                ["Remboursement des échéances de crédit", "Oui"],
                ["Ouverture de compte", "Non : orienter le client vers un jour de semaine"],
                ["Dépôt d'une demande de crédit", "Non"],
                ["Retrait d'un dépôt à terme", "Non"],
            ],
            (0.55, 0.45),
        ),
        h2("Organisation de l'équipe du samedi"),
        *bullets(
            [
                "L'équipe comprend au moins le chef d'agence ou son adjoint, deux caissiers "
                "et un agent de sécurité.",
                "Le planning est établi par roulement et affiché le lundi précédent.",
                "Les heures travaillées le samedi sont récupérées dans la semaine qui suit, "
                "selon le planning du chef d'agence.",
                "Les fonds sont livrés le vendredi selon le circuit habituel ; aucun "
                "transport de fonds n'a lieu le samedi.",
                "Le chef d'agence transmet le lundi à la Direction des opérations le nombre "
                "d'opérations réalisées le samedi, pour décider de la reconduction de "
                "l'ouverture les années suivantes.",
            ]
        ),
        h2("Fonds disponibles le samedi"),
        p(
            "L'encaisse prévue pour le samedi est calculée le vendredi par le chef d'agence, "
            "à partir des retraits observés les samedis précédents. Si les fonds deviennent "
            "insuffisants, les retraits importants sont reportés au lundi et les clients en "
            "sont informés poliment, sans jamais faire appel à un transport de fonds."
        ),
        h2("Information des commerçants"),
        p(
            "Les agents de crédit de l'agence informent les commerçants du marché de cette "
            "ouverture lors de leurs visites, et une affiche est posée à l'entrée de "
            "l'agence et au marché, avec l'accord des responsables du marché. Les clients "
            "des autres agences peuvent y effectuer leurs dépôts et retraits."
        ),
        callout(
            "Sécurité",
            [
                "La fermeture de la caisse du samedi suit exactement la procédure habituelle "
                "(voir OP-PRO-02). L'agence ne reçoit plus aucun client après l'heure de "
                "fermeture, même déjà présent devant la porte.",
            ],
        ),
    ]


def _p3() -> Page:
    return [
        h1("5. Autres dispositions"),
        h2("Information des clients"),
        p(
            "Les nouveaux horaires sont affichés à l'entrée de chaque agence au moins trois "
            "jours avant le début du Ramadan, en français et en arabe. Les agents de crédit "
            "informent leurs clients lors des visites et rappellent que les dates "
            "d'échéance ne changent pas."
        ),
        h2("Rendez-vous et visites de terrain"),
        p(
            "Les visites de clients sont programmées le matin. Les comités de crédit "
            "conservent leur calendrier, en commençant plus tôt. Les formations prévues "
            "pendant la période sont reportées, sauf les formations obligatoires."
        ),
        h2("Transports de fonds"),
        p(
            "Les approvisionnements et les remises de fonds entre le siège et les agences "
            "sont avancés en début de matinée. Les horaires précis sont communiqués aux "
            "seules personnes concernées, comme le prévoient les règles de sécurité des "
            "agences (voir SEC-PRO-02)."
        ),
        h2("Personnel en mission ou en formation"),
        p(
            "Les missions hors de N'Djamena sont limitées aux déplacements indispensables et "
            "organisées de façon à éviter les trajets aux heures les plus chaudes. Les "
            "salariés en mission suivent les horaires de l'agence qui les accueille."
        ),
        h2("Fête de l'Aïd el-Fitr"),
        p(
            "Les jours fériés de la fête sont ceux fixés par les autorités. Les horaires "
            "habituels reprennent le premier jour ouvrable qui suit la fête. Les demandes de "
            "congé autour de la fête sont traitées selon la procédure habituelle (voir "
            "RH-PRO-02), en garantissant la présence minimale dans chaque agence."
        ),
        h2("Santé du personnel"),
        p(
            "Un salarié qui ressent un malaise pendant le jeûne le signale à son responsable, "
            "qui l'autorise à se reposer ou à rentrer chez lui. Les travaux physiques "
            "(rangement des archives, inventaires) sont reportés après la période."
        ),
        h2("Contact"),
        p(
            "Toute question sur l'application de cette note est adressée à la Direction des "
            "ressources humaines. Les chefs d'agence veillent à son affichage et à sa "
            "diffusion à l'ensemble de leur équipe."
        ),
        callout(
            "Signature",
            [
                f"Note approuvée par la Direction générale le {SPEC.approval_date}. Elle "
                "cesse de s'appliquer automatiquement à la fin de la période de Ramadan.",
            ],
        ),
    ]
