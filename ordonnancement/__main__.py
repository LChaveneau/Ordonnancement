#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Démonstration du module.
"""

from .probleme import Duree, Tache, Probleme
from .algorithme import resous_EDT, resous_Calendrier
from .edt import Activite, EDT
from .calendrier import Date, Datation, Calendrier

mon_probleme = Probleme.par_str(
    """
A / 3 ans + 2 semaines / / Decryptage du probleme
B / 2 semaine + 4 jours / A fin (2 jours + 3 heures) / Developpement du projet
C / 2 heures + 23 minutes / B debut (2 jours + 3 heures) / Envoyer la requête à l'agence
D / 3 ans / A fin | C fin (10 mois) / Developpement de la plateforme publique
E / 1 seconde / D fin / Ouverture du projet
"""
)

mon_probleme.affiche_probleme()
mon_probleme.affiche_correspondance()

## Solution sans conditions
print("Les solutions présentes ci-dessous n'ont pas de conditions")
solution_EDT = resous_EDT(mon_probleme)
solution.affiche()
solution_Calendrier = resous_Calendrier(mon_probleme)
solution.affiche()

print(
    "Les solutions présentes ci-dessous ont les conditions :\nLes tâches ne sont pas éxécutables le samedi et dimanche.\nL'éxécution de tâches ne se fait qu'entre 9h et 18h"
)
## Solution avec conditions
solution_EDT = resous_EDT(mon_probleme, nb_jours_repos=2, duree_max_journalier=9)
solution.affiche()
solution_Calendrier = resous_Calendrier(
    mon_probleme, jours_repos="Samedi Dimanche", heures_execution="9-18"
)
solution.affiche()
