"""Document n° 4 — Politique de rémunération et avantages (RH-POL-04, 6 pages).

Réponses attendues : date de paiement des salaires (page 2) et taux du prêt au
personnel (page 4). Volontairement, aucune prime de fin d'année n'est mentionnée
(question sans réponse N1 du jeu d'évaluation).
"""

from scripts.demo_corpus.facts import DOCUMENTS, decimal_fr, fcfa, fmt_int
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

SPEC = DOCUMENTS[4]
STAFF_LOAN_RATE = 0.06
STAFF_LOAN_SALARY_MONTHS = 6
EXAMPLE_GROSS_SALARY = 250_000
EXAMPLE_NET_SALARY = 212_000
EXAMPLE_LOAN = 900_000
EXAMPLE_MONTHS = 24


def build_pages() -> list[Page]:
    """Construit les 6 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Cette politique définit les règles de rémunération du personnel de Kouri "
            "Épargne & Crédit : structure du salaire, primes et indemnités, avantages "
            "sociaux, prêts au personnel et évolution salariale. Elle vise une rémunération "
            "juste, lisible et comparable à celle du secteur de la microfinance au Tchad, "
            "dans le respect de l'équilibre financier de l'institution."
        ),
        h2("Champ d'application"),
        p(
            "La politique s'applique à tous les salariés liés à l'institution par un contrat "
            "de travail, au siège et en agence. Les stagiaires reçoivent une gratification "
            "fixée par leur convention de stage ; la rémunération des directeurs est fixée "
            "par le Conseil d'administration dans le respect des mêmes principes."
        ),
        h1("2. Principes"),
        *bullets(
            [
                "**Équité** : à poste et ancienneté égaux, salaire de base égal, sans "
                "distinction de sexe ou d'origine.",
                "**Lisibilité** : chaque élément de rémunération figure sur une ligne "
                "distincte du bulletin de paie.",
                "**Mérite** : la part variable récompense la qualité du travail mesurée par "
                "des indicateurs connus à l'avance.",
                "**Confidentialité** : le salaire de chacun n'est connu que de lui, de la "
                "Direction des ressources humaines et de la Direction générale.",
            ]
        ),
        h1("3. Composantes de la rémunération"),
        table(
            [
                ["Élément", "Nature", "Section"],
                ["Salaire de base", "Fixe, selon la catégorie et l'échelon", "Section 4"],
                ["Prime d'ancienneté", "Fixe, selon les années de service", "Section 6"],
                ["Indemnités", "Transport, caisse, responsabilité", "Section 6"],
                ["Prime de performance", "Variable, trimestrielle", "Section 6"],
                ["Avantages sociaux", "Prêts, avances, couverture santé", "Sections 7 et 8"],
            ],
            (0.3, 0.5, 0.2),
        ),
    ]


def _p2() -> Page:
    return [
        h1("4. Salaire de base"),
        p(
            "Chaque poste est classé dans une catégorie de la grille salariale. Le salaire "
            "de base progresse par échelon, selon l'ancienneté dans la catégorie et les "
            "résultats de l'évaluation annuelle (section 9)."
        ),
        table(
            [
                ["Catégorie", "Exemples de postes", "Salaire de base mensuel brut"],
                [
                    "A",
                    "Gardien, chauffeur, agent d'entretien",
                    f"De {fcfa(90_000)} à {fcfa(140_000)}",
                ],
                ["B", "Caissier, assistant administratif", f"De {fcfa(150_000)} à {fcfa(230_000)}"],
                ["C", "Agent de crédit, comptable", f"De {fcfa(220_000)} à {fcfa(340_000)}"],
                [
                    "D",
                    "Chef d'agence, responsable de service",
                    f"De {fcfa(380_000)} à {fcfa(600_000)}",
                ],
                ["E", "Directeur", "Fixé par le Conseil d'administration"],
            ],
            (0.14, 0.46, 0.4),
        ),
        h1("5. Paiement des salaires"),
        p(
            "Les salaires sont versés le 25 de chaque mois, par virement sur le compte du "
            "salarié ouvert chez Kouri. Lorsque cette date tombe un samedi, un dimanche ou un "
            "jour férié, le virement est effectué le dernier jour ouvrable qui précède. Le "
            "bulletin de paie est remis le même jour, sous enveloppe fermée ou par voie "
            "électronique."
        ),
        h2("Contenu du bulletin de paie"),
        *bullets(
            [
                "Salaire de base, primes et indemnités, chacun sur une ligne.",
                "Cotisations sociales et impôt retenus, avec leur base de calcul.",
                "Remboursements de prêt ou d'avance retenus sur le salaire.",
                "Solde de congés acquis et pris à la fin du mois.",
            ]
        ),
        h2("Entrée ou départ en cours de mois"),
        p(
            "Le salaire du mois d'embauche ou de départ est calculé au prorata des jours de "
            "travail effectif. Le solde de tout compte est payé au plus tard à la paie qui "
            "suit le départ, après restitution du matériel et des clés confiés au salarié."
        ),
        h2("Retenues sur salaire"),
        p(
            "Seules les retenues prévues par la loi ou acceptées par écrit par le salarié "
            "peuvent être opérées : cotisations, impôt, remboursement d'un prêt ou d'une "
            "avance, absence irrégulière, manquant de caisse constaté contradictoirement. "
            "Leur total est limité par la quotité saisissable fixée par la réglementation."
        ),
        callout(
            "Erreur sur le bulletin",
            [
                "Le salarié signale toute erreur à la Direction des ressources humaines dans "
                "le mois. Un trop-perçu est récupéré en plusieurs fois si son montant dépasse "
                "le dixième du salaire net.",
            ],
        ),
    ]


def _p3() -> Page:
    return [
        h1("6. Primes et indemnités"),
        table(
            [
                ["Élément", "Bénéficiaires", "Montant ou règle"],
                [
                    "Prime d'ancienneté",
                    "Tous les salariés après 2 ans de service",
                    "2 % du salaire de base par année de service, plafonnée à 25 %",
                ],
                ["Indemnité de transport", "Tous les salariés", f"{fcfa(15_000)} par mois"],
                [
                    "Indemnité de caisse",
                    "Caissiers titulaires",
                    f"{fcfa(20_000)} par mois, pour couvrir le risque d'erreur",
                ],
                [
                    "Indemnité de responsabilité",
                    "Chefs d'agence et responsables de service",
                    "10 % du salaire de base",
                ],
                [
                    "Prime de performance",
                    "Agents de crédit et chefs d'agence",
                    "Trimestrielle, selon la grille de la section 6.1",
                ],
            ],
            (0.26, 0.32, 0.42),
        ),
        h2("6.1 Prime de performance des agents de crédit"),
        p(
            "La prime récompense un portefeuille à la fois développé et sain. Elle est "
            "calculée chaque trimestre à partir de trois indicateurs, et n'est versée que si "
            "le portefeuille à risque de l'agent reste sous le seuil fixé chaque année par "
            "la Direction du crédit."
        ),
        table(
            [
                ["Indicateur", "Poids", "Mesure"],
                ["Qualité du portefeuille", "50 %", "Part des crédits remboursés sans retard"],
                ["Nouveaux clients financés", "30 %", "Nombre de premiers crédits décaissés"],
                [
                    "Qualité des dossiers",
                    "20 %",
                    "Résultat des contrôles du chef d'agence et de l'audit interne",
                ],
            ],
            (0.34, 0.12, 0.54),
        ),
        p(
            "Un dossier accordé en violation de la politique de crédit annule la prime du "
            "trimestre concerné, sans préjudice des sanctions prévues au règlement intérieur."
        ),
        h2("6.2 Prime de performance des chefs d'agence"),
        p(
            "La prime du chef d'agence repose sur les résultats de toute son agence : "
            "qualité du portefeuille, croissance de l'épargne collectée, absence d'écart de "
            "caisse non expliqué et résultat des missions d'audit. Elle est versée chaque "
            "trimestre après validation par la Direction des opérations."
        ),
        h2("6.3 Versement des primes"),
        p(
            "Les primes trimestrielles sont versées avec le salaire du mois qui suit la fin "
            "du trimestre. Un salarié absent plus de la moitié du trimestre, sauf congé de "
            "maternité ou accident du travail, ne perçoit pas la prime de ce trimestre."
        ),
        callout(
            "Transparence",
            [
                "Chaque salarié concerné reçoit, avec sa prime, le détail du calcul : valeur "
                "de chaque indicateur, poids appliqué et montant obtenu. Il peut demander "
                "une vérification à la Direction des ressources humaines.",
            ],
        ),
    ]


def _p4() -> Page:
    ceiling = STAFF_LOAN_SALARY_MONTHS * EXAMPLE_GROSS_SALARY
    monthly_rate = STAFF_LOAN_RATE / 12
    installment = round(EXAMPLE_LOAN * monthly_rate / (1 - (1 + monthly_rate) ** -EXAMPLE_MONTHS))
    third = EXAMPLE_NET_SALARY // 3
    return [
        h1("7. Prêts et avances au personnel"),
        h2("7.1 Prêt au personnel"),
        p(
            "Tout salarié confirmé dans son poste peut obtenir un prêt pour un projet "
            "personnel (logement, équipement, études, événement familial). Le taux du prêt au "
            "personnel est de 6 % par an, dans la limite de 6 mois de salaire brut. La "
            "mensualité ne dépasse pas le tiers du salaire net, et la durée est de 36 mois au "
            "plus. Le prêt est accordé par le comité de crédit, sans que l'intéressé ni son "
            "responsable direct n'y siègent."
        ),
        h2("Exemple : prêt de 900 000 FCFA sur 24 mois"),
        *calculation(
            [
                ("Salaire de base mensuel brut", fcfa(EXAMPLE_GROSS_SALARY)),
                (f"Plafond du prêt = {STAFF_LOAN_SALARY_MONTHS} × ligne 1", fcfa(ceiling)),
                ("Montant demandé (inférieur au plafond)", fcfa(EXAMPLE_LOAN)),
                (
                    f"Taux mensuel = {decimal_fr(STAFF_LOAN_RATE, 2)} ÷ 12",
                    decimal_fr(monthly_rate, 4),
                ),
                (
                    f"Mensualité = montant × t ÷ (1 − (1 + t) puissance −{EXAMPLE_MONTHS})",
                    fcfa(installment),
                ),
                ("Salaire net mensuel", fcfa(EXAMPLE_NET_SALARY)),
                ("Tiers du salaire net = ligne 6 ÷ 3", fcfa(third)),
                ("Contrôle : ligne 5 inférieure à ligne 7", "Prêt possible"),
            ],
            "Étape du calcul",
        ),
        h2("7.2 Avance sur salaire"),
        p(
            "Une avance sur salaire peut être accordée une fois par mois, pour un montant "
            "maximal égal à la moitié du salaire net. Elle est retenue en totalité sur le "
            f"salaire suivant et ne porte pas d'intérêts. Exemple : pour un salaire net de "
            f"{fmt_int(EXAMPLE_NET_SALARY)} FCFA, l'avance maximale est de "
            f"{fcfa(EXAMPLE_NET_SALARY // 2)}."
        ),
        h2("7.3 Remboursement et garanties"),
        p(
            "Les mensualités du prêt et l'avance sont retenues directement sur le salaire, "
            "avec l'autorisation écrite signée par le salarié à la mise en place. Le prêt "
            "est couvert par l'assurance décès-invalidité dans les mêmes conditions que les "
            "crédits aux clients."
        ),
        h2("7.4 Instruction et priorités"),
        p(
            "Les demandes de prêt sont instruites par la Direction des ressources humaines, "
            "qui vérifie le plafond et la capacité de remboursement, puis transmises au "
            "comité de crédit. Lorsque l'enveloppe annuelle des prêts au personnel est "
            "insuffisante, priorité est donnée aux projets de logement et aux dépenses de "
            "santé. Un nouveau prêt n'est accordé qu'après le remboursement complet du "
            "précédent, sauf urgence médicale."
        ),
    ]


def _p5() -> Page:
    return [
        h1("8. Couverture santé et protection sociale"),
        p(
            "Le personnel est affilié au régime de sécurité sociale prévu par la "
            "réglementation. En complément, l'institution souscrit une assurance santé de "
            "groupe qui couvre le salarié, son conjoint et ses enfants à charge."
        ),
        table(
            [
                ["Prestation", "Prise en charge par l'assurance de groupe"],
                ["Consultations et médicaments prescrits", "80 % des frais réels"],
                ["Hospitalisation", "90 % des frais réels, dans les établissements agréés"],
                ["Maternité", "100 % du forfait accouchement"],
                ["Lunettes", "Une paire tous les deux ans, dans la limite du barème"],
            ],
            (0.45, 0.55),
        ),
        h2("Assurance décès et invalidité du salarié"),
        p(
            "Une assurance de groupe verse aux ayants droit d'un salarié décédé un capital "
            "égal à douze mois de salaire brut, et au salarié reconnu invalide une rente "
            "complémentaire. La cotisation est entièrement prise en charge par l'institution."
        ),
        h1("9. Évaluation et évolution salariale"),
        p(
            "Chaque salarié a un entretien annuel d'évaluation avec son responsable. "
            "L'entretien porte sur les objectifs de l'année écoulée, les compétences, les "
            "besoins de formation et les souhaits d'évolution. Le compte rendu est signé par "
            "les deux parties ; le salarié peut y ajouter ses observations."
        ),
        table(
            [
                ["Résultat de l'évaluation", "Effet sur le salaire de base"],
                ["Excellent", "Passage de deux échelons"],
                ["Satisfaisant", "Passage d'un échelon"],
                ["À améliorer", "Maintien de l'échelon, plan de progrès sur six mois"],
                ["Insuffisant", "Maintien de l'échelon, entretien avec la DRH"],
            ],
            (0.4, 0.6),
        ),
        h2("Promotion"),
        p(
            "Le passage à une catégorie supérieure suppose un poste vacant et la réussite de "
            "la procédure de recrutement interne (voir RH-PRO-03). Le salarié promu est "
            "classé à l'échelon de la nouvelle catégorie immédiatement supérieur à son "
            "salaire actuel."
        ),
        h2("Révision générale de la grille"),
        p(
            "La grille salariale est révisée par le Conseil d'administration en fonction de "
            "l'évolution du coût de la vie et des résultats de l'institution. La révision "
            "s'applique à tous les salariés à la même date, indépendamment des passages "
            "d'échelon individuels."
        ),
    ]


def _p6() -> Page:
    return [
        h1("10. Heures supplémentaires et déplacements"),
        p(
            "Les heures supplémentaires autorisées par écrit sont payées avec les majorations "
            "prévues par la réglementation, ou récupérées en temps à la demande du salarié. "
            "Les frais de déplacement professionnel sont remboursés selon la procédure des "
            "frais de mission (voir FIN-PRO-05)."
        ),
        h2("Départ à la retraite"),
        p(
            "Le salarié qui part à la retraite perçoit l'indemnité de départ prévue par la "
            "réglementation, calculée sur son ancienneté. La Direction des ressources "
            "humaines l'accompagne dans la constitution de son dossier de pension au moins "
            "six mois avant la date de départ."
        ),
        h1("11. Questions fréquentes"),
        *faq(
            [
                (
                    "Puis-je avoir un prêt au personnel et une avance en même temps ?",
                    "Oui, si le total des retenues sur le salaire ne dépasse pas la moitié du "
                    "salaire net.",
                ),
                (
                    "Que devient mon prêt si je quitte l'institution ?",
                    "Le capital restant dû devient exigible ; il est retenu sur le solde de tout "
                    "compte, puis le reliquat est remboursé selon un échéancier convenu.",
                ),
                (
                    "Ma prime de performance est-elle garantie ?",
                    "Non. Elle dépend des résultats du trimestre et de la qualité du portefeuille.",
                ),
                (
                    "Le salaire est-il versé en espèces ?",
                    "Non. Il est toujours versé par virement sur un compte Kouri.",
                ),
                (
                    "Mon ancienneté est-elle conservée après un congé sans solde ?",
                    "Oui, mais la durée du congé sans solde n'est pas comptée dans le calcul "
                    "de la prime d'ancienneté.",
                ),
            ]
        ),
        h2("Confidentialité des données de paie"),
        p(
            "Les bulletins de paie et les dossiers de prêt du personnel sont des données "
            "confidentielles : seuls la Direction des ressources humaines, la Direction "
            "générale et les auditeurs y ont accès. Un salarié qui divulgue la rémunération "
            "d'un collègue commet une faute."
        ),
        h1("12. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Janvier 2021", "Création de la politique"],
                ["2.0", SPEC.approval_date, "Nouvelle grille salariale et prime de performance"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
