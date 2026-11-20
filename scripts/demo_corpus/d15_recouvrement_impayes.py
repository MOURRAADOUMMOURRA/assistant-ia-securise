"""Document n° 15 — Recouvrement des impayés (CR-PRO-04, 6 pages).

Réponses attendues : première visite de l'agent (page 2) et passage au contentieux
(page 4).
"""

from scripts.demo_corpus.facts import DOCUMENTS, fcfa
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

SPEC = DOCUMENTS[15]
CONTENTIOUS_DAYS = 90
FIRST_VISIT_DAY = 7

# Exemple de régularisation (page 3).
MISSED = 2
INSTALLMENT = 45_000
EXTRA_PER_MONTH = 15_000


def build_pages() -> list[Page]:
    """Construit les 6 pages du document."""
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6()]


def _p1() -> Page:
    return [
        *title_block(SPEC),
        h1("1. Objet"),
        p(
            "Cette procédure décrit les actions à mener lorsqu'un client ne paie pas une "
            "échéance de crédit à la date prévue. Son objectif est double : récupérer les "
            "sommes dues, et aider le client de bonne foi à surmonter une difficulté "
            "passagère avant qu'elle ne devienne insurmontable. Un retard traité tôt se "
            "règle presque toujours à l'amiable."
        ),
        h1("2. Principes"),
        *bullets(
            [
                "**Réactivité** : chaque jour de retard compte ; le suivi commence le "
                "lendemain de l'échéance.",
                "**Respect** : aucune menace, aucune humiliation publique, aucune visite de "
                "nuit, aucune pression sur la famille du client.",
                "**Confidentialité** : la situation du client n'est jamais évoquée devant des "
                "tiers, sauf avec ses cautions dans le cadre prévu.",
                "**Légalité** : aucun bien n'est saisi sans décision de justice, sauf "
                "mobilisation des garanties signées par le client.",
                "**Traçabilité** : chaque action est notée dans la fiche de suivi du client.",
            ]
        ),
        h1("3. Définitions"),
        table(
            [
                ["Terme", "Définition"],
                [
                    "Échéance impayée",
                    "Échéance non payée en totalité à la date prévue au tableau d'amortissement",
                ],
                [
                    "Jours de retard",
                    "Nombre de jours écoulés depuis la plus ancienne échéance impayée",
                ],
                [
                    "Portefeuille à risque",
                    "Capital restant dû des crédits qui ont au moins "
                    "une échéance impayée depuis un nombre de jours donné",
                ],
                [
                    "Contentieux",
                    "Phase où le recouvrement passe par les garanties et, si "
                    "besoin, par la justice",
                ],
                [
                    "Plan de régularisation",
                    "Accord écrit par lequel le client rattrape son retard en plusieurs versements",
                ],
            ],
            (0.25, 0.75),
        ),
    ]


def _p2() -> Page:
    return [
        h1("4. Phase amiable : les premiers jours"),
        p(
            "La rapidité de la première réaction détermine le plus souvent l'issue du "
            "retard. Le calendrier ci-dessous est un minimum : l'agent peut agir plus tôt "
            "s'il connaît une difficulté du client."
        ),
        table(
            [
                ["Moment", "Action", "Responsable"],
                [
                    "1er jour de retard",
                    "Appel téléphonique pour connaître la cause",
                    "Agent de crédit",
                ],
                ["3e jour", "Message de rappel courtois", "Agent de crédit"],
                [
                    "Jour de la visite",
                    "Visite au domicile ou sur le lieu d'activité",
                    "Agent de crédit",
                ],
                [
                    "15e jour",
                    "Lettre de relance remise en main propre",
                    "Agent de crédit, signée par le chef d'agence",
                ],
            ],
            (0.22, 0.5, 0.28),
        ),
        h2("La première visite"),
        p(
            "Au 7e jour de retard, l'agent de crédit rend visite au client, sur son lieu "
            "d'activité ou à son domicile, aux heures habituelles de travail. La visite sert "
            "à comprendre la cause du retard, à constater l'état de l'activité et à "
            "convenir d'une date de paiement. L'agent remplit la fiche de visite, que le "
            "client signe."
        ),
        h2("Comprendre la cause"),
        table(
            [
                ["Cause fréquente", "Réponse adaptée"],
                ["Baisse passagère des ventes", "Date de paiement rapprochée, suivi hebdomadaire"],
                [
                    "Maladie ou décès dans la famille",
                    "Délai court, et étude d'un rééchelonnement si la difficulté dure",
                ],
                [
                    "Détournement des fonds vers une autre dépense",
                    "Rappel ferme de l'engagement, information des cautions",
                ],
                ["Mauvaise foi", "Passage accéléré aux étapes suivantes"],
            ],
            (0.4, 0.6),
        ),
        h2("Prévention"),
        p(
            "Trois jours avant chaque échéance, un message de rappel est envoyé aux clients "
            "qui ont déjà eu un retard. Prévenir coûte moins cher que recouvrer."
        ),
        h2("Fiche de suivi"),
        p(
            "Chaque action (appel, message, visite, promesse de paiement) est notée le jour "
            "même dans la fiche de suivi du client, avec la date et le nom de l'agent. Le chef "
            "d'agence relit chaque semaine les fiches des crédits en retard."
        ),
        callout(
            "Bonne pratique",
            [
                "Un engagement de paiement est toujours daté et chiffré : « je paierai "
                "bientôt » n'est pas un engagement.",
            ],
        ),
    ]


def _p3() -> Page:
    catch_up_months = MISSED * INSTALLMENT // EXTRA_PER_MONTH
    return [
        h1("5. Phase amiable : relances renforcées"),
        table(
            [
                ["Moment", "Action", "Responsable"],
                ["30e jour", "Convocation du client à l'agence", "Chef d'agence"],
                ["30e jour", "Information écrite des cautions", "Chef d'agence"],
                ["45e jour", "Visite conjointe agent et chef d'agence", "Chef d'agence"],
                [
                    "60e jour",
                    "Mise en demeure par lettre recommandée ou remise contre décharge",
                    "Direction du crédit",
                ],
            ],
            (0.15, 0.6, 0.25),
        ),
        h2("Plan de régularisation"),
        p(
            "Lorsque le client est de bonne foi et que son activité continue, l'agent "
            "propose un plan de régularisation : le client paie ses échéances normales, plus "
            "un complément chaque mois jusqu'à rattrapage du retard."
        ),
        *calculation(
            [
                ("Échéances impayées", str(MISSED)),
                ("Montant d'une échéance", fcfa(INSTALLMENT)),
                ("Arriéré = ligne 1 × ligne 2", fcfa(MISSED * INSTALLMENT)),
                ("Complément mensuel accepté par le client", fcfa(EXTRA_PER_MONTH)),
                ("Durée du rattrapage = ligne 3 ÷ ligne 4", f"{catch_up_months} mois"),
            ],
            "Étape du calcul",
        ),
        p(
            "Le plan est signé par le client et visé par le chef d'agence. Si le retard "
            "résulte d'un événement durable (maladie grave, sinistre), un rééchelonnement "
            "peut être proposé selon CR-PRO-01."
        ),
        h2("Rôle des cautions"),
        p(
            "Les cautions sont informées par écrit dès le 30e jour. Elles peuvent aider le "
            "client à régulariser. Elles ne sont appelées à payer qu'après la mise en "
            "demeure restée sans effet."
        ),
        h2("Convocation à l'agence"),
        p(
            "Le chef d'agence reçoit le client en entretien privé, rappelle les engagements "
            "du contrat et écoute ses explications. L'entretien se conclut par un "
            "engagement écrit ou par l'annonce des étapes suivantes."
        ),
        h2("La mise en demeure"),
        p(
            "La mise en demeure rappelle le montant dû, les échéances impayées et le délai "
            "accordé pour payer, en général quinze jours. Elle indique qu'à défaut, les "
            "garanties seront mobilisées. Une copie est classée au dossier avec la preuve de "
            "remise. Elle est rédigée en termes simples et, si nécessaire, expliquée "
            "oralement au client dans sa langue."
        ),
    ]


def _p4() -> Page:
    return [
        h1("6. Phase contentieuse"),
        p(
            f"Le dossier passe au contentieux après {CONTENTIOUS_DAYS} jours de retard, ou "
            "plus tôt si le client a disparu, a vendu les biens gagés ou refuse toute "
            "solution. Le passage est décidé par la Direction du crédit, sur proposition du "
            "chef d'agence ; le dossier est alors confié au chargé du contentieux du siège."
        ),
        h2("Mobilisation des garanties"),
        table(
            [
                ["Garantie", "Mode de mobilisation"],
                ["Épargne bloquée", "Imputée sur la dette, après information écrite du client"],
                [
                    "Caution personnelle",
                    "Mise en demeure de la caution de payer, avec copie de l'acte signé",
                ],
                [
                    "Gage sur matériel ou stock",
                    "Récupération amiable ; à défaut, procédure judiciaire",
                ],
                ["Hypothèque ou titre foncier", "Procédure judiciaire de réalisation"],
            ],
            (0.3, 0.7),
        ),
        h2("Procédure judiciaire"),
        p(
            "Le recours à la justice n'est engagé que si le montant en jeu justifie les frais "
            "et si les garanties ou le patrimoine du débiteur permettent d'espérer un "
            "recouvrement. La décision est prise par la Direction générale. Les frais de "
            "procédure sont mis à la charge du débiteur lorsque la décision de justice le "
            "prévoit."
        ),
        h2("Négociation pendant le contentieux"),
        p(
            "Un accord amiable reste possible à tout moment. Une remise partielle des "
            "intérêts de retard peut être accordée par la Direction du crédit contre un "
            "paiement immédiat du capital ; toute remise sur le capital relève du comité du "
            "siège."
        ),
        h2("Suivi des dossiers au contentieux"),
        p(
            "Le chargé du contentieux tient un tableau de bord des dossiers : montant dû, "
            "garanties mobilisées, étape de la procédure, prochaine action. Il le présente "
            "chaque mois à la Direction du crédit."
        ),
        h2("Transfert du dossier"),
        p(
            "Le chef d'agence transmet au chargé du contentieux le dossier complet : contrat, "
            "actes de garantie, fiches de suivi, mise en demeure et preuve de remise. L'agent "
            "de crédit reste disponible pour accompagner le chargé chez le client. Le crédit "
            "reste inscrit dans le portefeuille de l'agence jusqu'à son règlement ou son "
            "passage en perte."
        ),
        callout(
            "Interdit",
            [
                "Saisir soi-même un bien, retenir une pièce d'identité, menacer, ou contacter "
                "l'employeur ou les voisins du client sans base légale.",
            ],
        ),
    ]


def _p5() -> Page:
    return [
        h1("7. Classement et provisions"),
        p(
            "Les crédits en retard sont classés selon l'ancienneté de leur plus vieille "
            "échéance impayée. Ce classement détermine les provisions comptables que "
            "l'institution doit constituer, selon les règles prudentielles applicables."
        ),
        table(
            [
                ["Ancienneté du retard", "Classement", "Suivi"],
                ["1 à 30 jours", "Sous surveillance", "Agent de crédit"],
                ["31 à 90 jours", "Douteux", "Chef d'agence"],
                ["91 à 180 jours", "Compromis", "Chargé du contentieux"],
                ["Plus de 180 jours", "Proposé en perte", "Comité du siège"],
            ],
            (0.3, 0.3, 0.4),
        ),
        p(
            "Le classement est automatique dans le logiciel : chaque matin, les jours de "
            "retard sont recalculés et la liste des crédits changeant de catégorie est "
            "envoyée au chef d'agence."
        ),
        h2("Passage en perte"),
        p(
            "Un crédit peut être passé en perte lorsque toutes les actions raisonnables ont "
            "échoué. La décision est prise par le comité du siège et présentée au Conseil "
            "d'administration. Le passage en perte est une écriture comptable : la dette "
            "reste due et le recouvrement continue si une occasion se présente."
        ),
        h2("Indicateurs suivis"),
        *bullets(
            [
                "Portefeuille à risque à 30 jours, par agent, par agence et pour "
                "l'institution, chaque mois.",
                "Taux de régularisation des retards dans les 30 jours.",
                "Montants récupérés au contentieux et coût des procédures.",
            ]
        ),
        h2("Rapport mensuel"),
        p(
            "La Direction du crédit présente chaque mois à la Direction générale la liste "
            "des crédits de plus de 30 jours de retard, avec les actions engagées."
        ),
        h2("Analyse des causes"),
        p(
            "Chaque trimestre, la Direction du crédit analyse les causes des retards les plus "
            "fréquents : secteur d'activité, saison, agent, type de garantie. Les "
            "enseignements sont utilisés pour adapter la politique de crédit et la "
            "formation des agents."
        ),
        h2("Récupération après passage en perte"),
        p(
            "Toute somme récupérée sur un crédit passé en perte est enregistrée comme une "
            "recette exceptionnelle. Le client qui règle intégralement sa dette peut, après "
            "un délai d'observation, présenter une nouvelle demande de crédit."
        ),
    ]


def _p6() -> Page:
    return [
        h1("8. Cas particuliers"),
        table(
            [
                ["Situation", "Règle"],
                [
                    "Décès du client",
                    "Déclaration à l'assurance ; suspension des relances auprès de la famille",
                ],
                [
                    "Sinistre collectif (inondation, incendie de marché)",
                    "Suspension temporaire des relances décidée par la Direction générale",
                ],
                [
                    "Client parti sans adresse",
                    "Recherche par les cautions et le voisinage, puis contentieux",
                ],
                ["Membre d'un groupement", "Solidarité du groupe d'abord (voir CR-PRO-03)"],
            ],
            (0.38, 0.62),
        ),
        h2("Client salarié"),
        p(
            "Pour un client salarié dont le salaire est domicilié chez Kouri, l'échéance est "
            "prélevée dès le versement du salaire, selon l'autorisation signée au contrat. "
            "Un changement de domiciliation sans accord est traité comme un retard."
        ),
        h2("Réclamation du client"),
        p(
            "Un client qui conteste le montant réclamé ou le comportement d'un agent peut "
            "présenter une réclamation (voir QUA-PRO-01). Les relances continuent pendant "
            "l'examen, sauf sur la partie contestée."
        ),
        h1("9. Questions fréquentes"),
        *faq(
            [
                (
                    "Le client peut-il payer une partie seulement de l'échéance ?",
                    "Oui. Tout paiement partiel est accepté et réduit le retard ; le reste "
                    "suit la procédure.",
                ),
                (
                    "Les intérêts de retard sont-ils obligatoires ?",
                    "Ils sont prévus au contrat et à la grille des taux et frais en vigueur ; "
                    "une remise ne peut être accordée que selon la section 6.",
                ),
                (
                    "L'agent peut-il encaisser un remboursement en espèces sur le terrain ?",
                    "Oui, contre un reçu numéroté, et il le verse le jour même à la caisse.",
                ),
                (
                    "Un client en retard peut-il obtenir un nouveau crédit ?",
                    "Non, tant que le retard n'est pas régularisé ; un retard important est "
                    "pris en compte dans l'analyse des demandes suivantes.",
                ),
            ]
        ),
        h1("10. Historique des versions"),
        table(
            [
                ["Version", "Date", "Modification"],
                ["1.0", "Septembre 2021", "Création de la procédure"],
                ["2.0", SPEC.approval_date, "Calendrier renforcé et plan de régularisation"],
            ],
            (0.14, 0.24, 0.62),
        ),
    ]
