"""Source unique des faits du corpus de démonstration.

Tous les chiffres partagés (réponses du jeu d'évaluation, taux et frais des
grilles) sont définis ici. Les documents et le vérificateur lisent ce module :
un chiffre ne peut donc jamais diverger entre le texte d'un PDF et ce que le
vérificateur attend.

L'institution, ses documents et ses chiffres sont entièrement fictifs.
"""

from dataclasses import dataclass

NBSP = " "

# --- Mise en forme française des nombres -------------------------------------


def fmt_int(value: int) -> str:
    """Entier avec espaces insécables entre les milliers : 500000 → « 500 000 »."""
    return f"{value:,}".replace(",", NBSP)


def fcfa(value: int) -> str:
    """Montant en francs CFA : 500000 → « 500 000 FCFA »."""
    return f"{fmt_int(value)}{NBSP}FCFA"


def decimal_fr(value: float, digits: int = 2) -> str:
    """Nombre décimal à la française, sans zéros inutiles : 0.0175 → « 0,0175 »."""
    text = f"{value:.{digits}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text.replace(".", ",")


def pct(value: float) -> str:
    """Pourcentage à la française : 21 → « 21 % », 1.5 → « 1,5 % »."""
    return f"{decimal_fr(value, 2)}{NBSP}%"


# --- Institution ---------------------------------------------------------------

INSTITUTION_NAME = "Kouri Épargne & Crédit S.A."
INSTITUTION_SHORT = "Kouri Épargne & Crédit"
INSTITUTION_CATEGORY = "établissement de microfinance de 2e catégorie"
HEAD_OFFICE_CITY = "N'Djamena"
FOOTER_TEXT = "Document fictif – démonstration ZakiCortex"

AGENCIES: tuple[str, ...] = (
    "Agence Centre (siège)",
    "Agence Grand Marché",
    "Agence Chagoua",
    "Agence Farcha",
    "Agence Moundou",
    "Agence Abéché",
)
"""Les 6 agences : 4 à N'Djamena (dont le Grand Marché), 1 à Moundou, 1 à Abéché."""


# --- Catalogue des 25 documents ------------------------------------------------


@dataclass(frozen=True)
class DocumentSpec:
    """Fiche d'identité d'un document du corpus."""

    number: int
    slug: str
    reference: str
    title: str
    pages: int
    version: str
    effective_date: str
    drafted_by: str
    approved_by: str
    approval_date: str

    @property
    def filename(self) -> str:
        """Nom du fichier PDF, ex. « d10_octroi_credit.pdf »."""
        return f"d{self.number:02d}_{self.slug}.pdf"


_DG = "Direction générale"
_CA = "Conseil d'administration"
_DRH = "Direction des ressources humaines"
_DC = "Direction du crédit"
_DO = "Direction des opérations"
_DCONF = "Direction de la conformité"

DOCUMENTS: dict[int, DocumentSpec] = {
    spec.number: spec
    for spec in (
        DocumentSpec(
            1,
            "reglement_interieur",
            "RH-REG-01",
            "Règlement intérieur",
            8,
            "2.1",
            "1er février 2025",
            _DRH,
            _CA,
            "20 janvier 2025",
        ),
        DocumentSpec(
            2,
            "demande_conges",
            "RH-PRO-02",
            "Procédure de demande de congés",
            5,
            "1.3",
            "1er mars 2025",
            _DRH,
            _DG,
            "17 février 2025",
        ),
        DocumentSpec(
            3,
            "recrutement_integration",
            "RH-PRO-03",
            "Recrutement et intégration",
            6,
            "1.2",
            "1er avril 2025",
            _DRH,
            _DG,
            "24 mars 2025",
        ),
        DocumentSpec(
            4,
            "remuneration_avantages",
            "RH-POL-04",
            "Politique de rémunération et avantages",
            6,
            "2.0",
            "1er janvier 2026",
            _DRH,
            _CA,
            "12 décembre 2025",
        ),
        DocumentSpec(
            5,
            "frais_mission",
            "FIN-PRO-05",
            "Frais de mission",
            5,
            "1.4",
            "1er juin 2025",
            "Direction financière",
            _DG,
            "26 mai 2025",
        ),
        DocumentSpec(
            6,
            "charte_informatique",
            "SI-CHA-01",
            "Charte informatique et sécurité des données",
            7,
            "3.0",
            "1er septembre 2025",
            "Service informatique",
            _DG,
            "25 août 2025",
        ),
        DocumentSpec(
            7,
            "plan_formation_2026",
            "RH-PLF-2026",
            "Plan de formation 2026",
            5,
            "1.0",
            "5 janvier 2026",
            _DRH,
            _DG,
            "18 décembre 2025",
        ),
        DocumentSpec(
            8,
            "consignes_incendie",
            "SEC-CON-01",
            "Consignes incendie et évacuation",
            4,
            "1.1",
            "1er juillet 2025",
            "Responsable sécurité",
            _DG,
            "23 juin 2025",
        ),
        DocumentSpec(
            9,
            "note_horaires_ramadan",
            "NS-2026-03",
            "Note de service : horaires du Ramadan",
            3,
            "1.0",
            "18 février 2026",
            _DRH,
            _DG,
            "9 février 2026",
        ),
        DocumentSpec(
            10,
            "octroi_credit",
            "CR-PRO-01",
            "Politique et procédure d'octroi de crédit",
            10,
            "3.0",
            "2 janvier 2026",
            _DC,
            _CA,
            "12 décembre 2025",
        ),
        DocumentSpec(
            11,
            "comite_credit_plafonds",
            "CR-PRO-02",
            "Comité de crédit et plafonds d'autorisation",
            5,
            "2.2",
            "2 janvier 2026",
            _DC,
            _CA,
            "12 décembre 2025",
        ),
        DocumentSpec(
            12,
            "credit_solidaire",
            "CR-PRO-03",
            "Crédit solidaire aux groupements",
            5,
            "1.5",
            "1er octobre 2025",
            _DC,
            _DG,
            "22 septembre 2025",
        ),
        DocumentSpec(
            13,
            "grille_taux_frais_2025",
            "TAR-2025",
            "Grille des taux et frais 2025",
            4,
            "1.0",
            "1er janvier 2025",
            "Direction financière",
            _CA,
            "16 décembre 2024",
        ),
        DocumentSpec(
            14,
            "grille_taux_frais_2026",
            "TAR-2026",
            "Grille des taux et frais 2026",
            4,
            "1.0",
            "1er janvier 2026",
            "Direction financière",
            _CA,
            "16 décembre 2025",
        ),
        DocumentSpec(
            15,
            "recouvrement_impayes",
            "CR-PRO-04",
            "Recouvrement des impayés",
            6,
            "2.0",
            "1er novembre 2025",
            _DC,
            _DG,
            "27 octobre 2025",
        ),
        DocumentSpec(
            16,
            "ouverture_compte",
            "OP-PRO-01",
            "Procédure d'ouverture de compte",
            5,
            "2.3",
            "1er mai 2025",
            _DO,
            _DG,
            "28 avril 2025",
        ),
        DocumentSpec(
            17,
            "kyc_anti_blanchiment",
            "CONF-POL-01",
            "Connaissance client (KYC) et lutte anti-blanchiment",
            8,
            "3.1",
            "1er juillet 2025",
            _DCONF,
            _CA,
            "19 juin 2025",
        ),
        DocumentSpec(
            18,
            "catalogue_epargne",
            "EP-CAT-01",
            "Catalogue des produits d'épargne",
            5,
            "2.0",
            "1er janvier 2026",
            _DO,
            _DG,
            "15 décembre 2025",
        ),
        DocumentSpec(
            19,
            "procedures_caisse",
            "OP-PRO-02",
            "Procédures de caisse en agence",
            6,
            "2.1",
            "1er août 2025",
            _DO,
            _DG,
            "21 juillet 2025",
        ),
        DocumentSpec(
            20,
            "securite_agences",
            "SEC-PRO-02",
            "Sécurité des agences",
            5,
            "1.2",
            "1er août 2025",
            "Responsable sécurité",
            _DG,
            "21 juillet 2025",
        ),
        DocumentSpec(
            21,
            "reclamations_clients",
            "QUA-PRO-01",
            "Traitement des réclamations clients",
            4,
            "1.1",
            "1er septembre 2025",
            "Service qualité",
            _DG,
            "25 août 2025",
        ),
        DocumentSpec(
            22,
            "organigramme_roles",
            "ORG-01",
            "Organigramme et rôles des services",
            4,
            "4.0",
            "1er janvier 2026",
            _DG,
            _CA,
            "12 décembre 2025",
        ),
        DocumentSpec(
            23,
            "rapport_annuel_2025",
            "RA-2025",
            "Rapport annuel 2025",
            10,
            "1.0",
            "15 avril 2026",
            "Direction financière",
            _CA,
            "8 avril 2026",
        ),
        DocumentSpec(
            24,
            "plan_continuite",
            "PCA-01",
            "Plan de continuité d'activité",
            6,
            "1.3",
            "1er octobre 2025",
            _DO,
            _DG,
            "29 septembre 2025",
        ),
        DocumentSpec(
            25,
            "protection_donnees",
            "CONF-POL-02",
            "Protection des données personnelles",
            5,
            "1.2",
            "1er septembre 2025",
            _DCONF,
            _DG,
            "25 août 2025",
        ),
    )
}


# --- Octroi de crédit (document n° 10) ----------------------------------------

FIRST_LOAN_CAP_FCFA = 500_000
"""Montant maximal d'un premier crédit."""

MAX_INSTALLMENT_RATIO_PCT = 40
"""Part maximale du revenu net mensuel consacrée aux mensualités."""


# --- Grilles des taux et frais (documents n° 13 et 14) ------------------------


@dataclass(frozen=True)
class CreditRate:
    """Ligne de la grille des taux : produit, durée maximale et taux annuel."""

    product: str
    max_duration: str
    annual_rate_pct: float


@dataclass(frozen=True)
class ServiceFee:
    """Ligne de la grille des frais de compte : service et tarif en FCFA (0 = gratuit)."""

    service: str
    fee_fcfa: int


@dataclass(frozen=True)
class TariffGrid:
    """Grille des taux et frais d'une année. Rubriques identiques d'une année à l'autre."""

    year: int
    document: int
    replaces_reference: str
    credit_rates: tuple[CreditRate, ...]
    dossier_fee_pct: float
    dossier_fee_min_fcfa: int
    insurance_pct: float
    late_penalty_pct: float
    rescheduling_fee_fcfa: int
    account_fee_monthly_fcfa: int
    services: tuple[ServiceFee, ...]

    @property
    def agr_rate_pct(self) -> float:
        """Taux annuel du crédit AGR (première ligne de la grille)."""
        return self.credit_rates[0].annual_rate_pct


AGR = "Crédit pour activité génératrice de revenus (AGR)"
_PRODUCTS = (
    (AGR, "18 mois"),
    ("Crédit solidaire aux groupements (voir CR-PRO-03)", "12 mois"),
    ("Crédit équipement (matériel professionnel)", "24 mois"),
    ("Crédit agricole de campagne", "10 mois"),
    ("Crédit scolaire (rentrée des classes)", "9 mois"),
)
_SERVICES = (
    "Relevé de compte à la demande",
    "Attestation de solde ou de non-engagement",
    "Duplicata de carte de membre",
    "Virement interne entre deux comptes Kouri",
    "Clôture de compte à la demande du client",
)


def _grid(
    year: int,
    document: int,
    replaces: str,
    rates: tuple[float, ...],
    fees: tuple[float, int, float, float, int, int],
    services: tuple[int, ...],
) -> TariffGrid:
    """Assemble une grille à partir des rubriques communes et des chiffres de l'année."""
    dossier_pct, dossier_min, insurance, penalty, rescheduling, account = fees
    return TariffGrid(
        year=year,
        document=document,
        replaces_reference=replaces,
        credit_rates=tuple(
            CreditRate(product, duration, rate)
            for (product, duration), rate in zip(_PRODUCTS, rates, strict=True)
        ),
        dossier_fee_pct=dossier_pct,
        dossier_fee_min_fcfa=dossier_min,
        insurance_pct=insurance,
        late_penalty_pct=penalty,
        rescheduling_fee_fcfa=rescheduling,
        account_fee_monthly_fcfa=account,
        services=tuple(
            ServiceFee(name, fee) for name, fee in zip(_SERVICES, services, strict=True)
        ),
    )


GRIDS: dict[int, TariffGrid] = {
    2025: _grid(
        2025,
        13,
        "TAR-2024",
        rates=(24, 22, 20, 23, 19),
        fees=(2, 2_500, 0.9, 1.25, 7_500, 1_000),
        services=(500, 1_500, 2_000, 300, 2_500),
    ),
    2026: _grid(
        2026,
        14,
        "TAR-2025",
        rates=(21, 19, 18, 20, 17),
        fees=(1.5, 3_000, 0.75, 1, 5_000, 1_500),
        services=(500, 2_000, 2_500, 200, 3_000),
    ),
}

EXAMPLE_LOAN_FCFA = 300_000
"""Montant de l'exemple chiffré des grilles."""

EXAMPLE_LOAN_MONTHS = 12


# --- Réponses attendues (jeu d'évaluation et réserve) --------------------------


@dataclass(frozen=True)
class AnswerKey:
    """Réponse attendue : document, page, et extrait exact qui doit y figurer une seule fois."""

    document: int
    label: str
    page: int
    needle: str
    question: str


_G25 = GRIDS[2025]
_G26 = GRIDS[2026]

ANSWER_KEYS: tuple[AnswerKey, ...] = (
    AnswerKey(1, "Q1", 2, "7 h 00 à 12 h 30", "Horaires du personnel le vendredi ?"),
    AnswerKey(1, "Q2", 7, "mise à pied de 1 à 3 jours", "Sanctions disciplinaires ?"),
    AnswerKey(
        2, "Q1", 3, "15 jours calendaires", "Délai de dépôt pour un congé de plus de 5 jours ?"
    ),
    AnswerKey(2, "Q2", 2, "4 jours ouvrables", "Congé pour mariage du salarié ?"),
    AnswerKey(
        3, "Q1", 4, "3 mois, renouvelable une fois", "Période d'essai d'un agent de crédit ?"
    ),
    AnswerKey(
        3,
        "Q2",
        5,
        "après signature de la charte de confidentialité",
        "Quand reçoit-on ses identifiants du logiciel ?",
    ),
    AnswerKey(4, "Q1", 2, "le 25 de chaque mois", "Date de paiement des salaires ?"),
    AnswerKey(4, "Q2", 4, "6 % par an", "Taux d'un prêt au personnel ?"),
    AnswerKey(5, "Q1", 3, "15 000 FCFA par jour", "Indemnité pour une mission hors de N'Djamena ?"),
    AnswerKey(5, "Q2", 4, "7 jours ouvrables", "Délai pour remettre les justificatifs ?"),
    AnswerKey(6, "Q1", 3, "tous les 90 jours", "Fréquence de changement du mot de passe ?"),
    AnswerKey(6, "Q2", 6, "sous 2 h", "Perte d'une tablette de collecte ?"),
    AnswerKey(7, "Q1", 2, "30 heures", "Heures de formation par salarié ?"),
    AnswerKey(7, "Q2", 4, "mars 2026", "Formation anti-blanchiment obligatoire ?"),
    AnswerKey(8, "Q1", 2, "parking devant le siège", "Point de rassemblement du siège ?"),
    AnswerKey(
        8, "Q2", 3, "chef d'agence dirige l'évacuation", "Qui dirige l'évacuation en agence ?"
    ),
    AnswerKey(9, "Q1", 1, "7 h 30 à 13 h 00", "Horaires des agences pendant le Ramadan ?"),
    AnswerKey(9, "Q2", 2, "de 8 h à 11 h", "L'agence du Grand Marché ouvre-t-elle le samedi ?"),
    AnswerKey(10, "Q1", 4, fcfa(FIRST_LOAN_CAP_FCFA), "Montant maximal d'un premier crédit ?"),
    AnswerKey(
        10,
        "Q2",
        6,
        f"{pct(MAX_INSTALLMENT_RATIO_PCT)} du revenu net mensuel",
        "Mensualité maximale ?",
    ),
    AnswerKey(
        11, "Q1", 2, "jusqu'à 1 000 000 FCFA", "Plafond qu'un chef d'agence peut approuver seul ?"
    ),
    AnswerKey(
        11, "Q2", 4, "au-delà de 10 000 000 FCFA", "Qui approuve au-delà de 10 000 000 FCFA ?"
    ),
    AnswerKey(12, "Q1", 2, "5 à 15 membres", "Taille d'un groupement ?"),
    AnswerKey(
        12, "Q2", 3, "les autres membres remboursent à sa place", "Un membre ne rembourse pas ?"
    ),
    AnswerKey(
        13,
        "Q1",
        2,
        f"{pct(_G25.dossier_fee_pct)} du montant du crédit",
        "Frais de dossier en 2025 ?",
    ),
    AnswerKey(
        13, "Q2", 3, f"{fcfa(_G25.account_fee_monthly_fcfa)} par mois", "Tenue de compte en 2025 ?"
    ),
    AnswerKey(
        13,
        "piège",
        2,
        f"{pct(_G25.agr_rate_pct)} par an",
        "Taux AGR de l'ancienne grille (piège 2025/2026)",
    ),
    AnswerKey(
        14,
        "Q1",
        2,
        f"{pct(_G26.agr_rate_pct)} par an",
        "Taux du crédit pour activité génératrice de revenus (AGR) ?",
    ),
    AnswerKey(14, "Q2", 3, f"{fcfa(_G26.account_fee_monthly_fcfa)} par mois", "Tenue de compte ?"),
    AnswerKey(15, "Q1", 4, "90 jours de retard", "Passage au contentieux ?"),
    AnswerKey(15, "Q2", 2, "7e jour de retard", "Première visite de l'agent ?"),
    AnswerKey(16, "Q1", 2, "attestation du chef de quartier", "Pièces à fournir ?"),
    AnswerKey(16, "Q2", 4, "jusqu'à ses 18 ans", "Compte d'un mineur ?"),
    AnswerKey(
        17,
        "Q1",
        4,
        "égal ou supérieur à 5 000 000 FCFA",
        "Seuil de déclaration interne d'une opération en espèces ?",
    ),
    AnswerKey(
        17,
        "Q2",
        6,
        "mis à jour chaque année",
        "Mise à jour du dossier d'un client à risque élevé ?",
    ),
    AnswerKey(18, "Q1", 3, "4,5 % par an", "Taux d'un dépôt à terme de 12 mois ?"),
    AnswerKey(18, "Q2", 4, "réduits de moitié", "Retrait avant l'échéance ?"),
    AnswerKey(19, "Q1", 2, "plafonnée à 5 000 000 FCFA", "Plafond d'encaisse d'un guichet ?"),
    AnswerKey(19, "Q2", 4, "procès-verbal le jour même", "Écart de caisse en fin de journée ?"),
    AnswerKey(
        20,
        "Q1",
        2,
        "chef d'agence et le caissier principal",
        "Combien de personnes pour ouvrir le coffre ?",
    ),
    AnswerKey(20, "Q2", 4, "alarme silencieuse", "Conduite en cas de braquage ?"),
    AnswerKey(21, "Q1", 2, "48 h ouvrées", "Délai d'accusé de réception ?"),
    AnswerKey(21, "Q2", 3, "15 jours ouvrables", "Délai de réponse définitive ?"),
    AnswerKey(22, "Q1", 1, "4 à N'Djamena, 1 à Moundou et 1 à Abéché", "Nombre d'agences ?"),
    AnswerKey(
        22,
        "Q2",
        3,
        "rattaché directement au Directeur général",
        "Rattachement du responsable conformité ?",
    ),
    AnswerKey(23, "Q1", 2, "18 400", "Clients actifs fin 2025 ?"),
    AnswerKey(23, "Q2", 6, "6,8 %", "Portefeuille à risque à 30 jours (PAR 30) fin 2025 ?"),
    AnswerKey(24, "Q1", 3, "autonomie de 8 heures", "Autonomie du groupe électrogène ?"),
    AnswerKey(
        24,
        "Q2",
        4,
        "100 000 FCFA par jour",
        "Logiciel en panne : combien un client peut-il retirer ?",
    ),
    AnswerKey(
        25,
        "Q1",
        3,
        "10 ans après la clôture du compte",
        "Conservation des données d'un ancien client ?",
    ),
    AnswerKey(25, "Q2", 2, "référent données personnelles", "Référent données personnelles ?"),
)
