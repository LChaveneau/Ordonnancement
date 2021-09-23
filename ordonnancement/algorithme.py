#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Contient la fonction de résolution du problème d'ordonnancement.
"""
from .probleme import Probleme, Tache, Prerequis, Duree
from .edt import Activite, EDT
from .calendrier import Date, Calendrier, Datation
import networkx as nx
from pendulum import duration, datetime
from typing import Union, Optional


def genere_graphe(probleme: Probleme) -> nx.DiGraph:
    """Crée le graphe associé au problème."""
    resultat = nx.DiGraph()
    for tache in probleme.taches:
        for prerequis in tache.prerequis:
            if prerequis:
                resultat.add_edge(
                    prerequis.nom,
                    tache.nom,
                    temps=tache.duree,
                    attente=prerequis.latence,
                    typ=prerequis.typ,
                )
    return resultat


def _calcule_demarrage(tache: Tache, edt: EDT) -> Duree:
    """Calcule sur quels prerequis une tâche doit commencer.
    Retourne un type Duree"""

    fins_prerequis = list()
    for prerequis in tache.prerequis:
        if prerequis:
            if prerequis.typ == "fin":
                fins_prerequis.append(edt[prerequis.nom].fin.add(prerequis.latence))
            if prerequis.typ == "debut":
                fins_prerequis.append(edt[prerequis.nom].debut.add(prerequis.latence))
    if fins_prerequis:
        return max(fins_prerequis)
    return Duree()


def _calcule_demarrage2(
    tache: Tache, calendrier: Calendrier, date_commencement: Date
) -> Date:
    """Calcule sur quelle prerequis une tâche doit commencer.
    Retourne type Date"""
    fins_prerequis = list()
    for prerequis in tache.prerequis:
        if prerequis:
            if prerequis.typ == "fin":
                fins_prerequis.append(
                    calendrier[prerequis.nom].date_fin.add(prerequis.latence)
                )
            if prerequis.typ == "debut":
                fins_prerequis.append(
                    calendrier[prerequis.nom].date_debut.add(prerequis.latence)
                )
    if fins_prerequis:
        return max(fins_prerequis)
    return date_commencement


def _calcule_journalier(duree: Duree, duree_max_journalier: Union[int, float]) -> Duree:
    """Calcule le temps d'éxécution d'une tâche si nous rajoutons une durée maximale journaliére d'éxécution de tâche."""
    minutes = duree._convertit_duration().in_minutes()
    secondes = duree._convertit_duration().seconds
    ##Rajoute les durées d'exécution de la tache en secondes.
    minutes_total = int(round((minutes / 60 / duree_max_journalier) * 24 * 60))
    ##Calcule les temps pour qu'il ne reste pas de surplus de temps.
    minutes_restantes = minutes_total % 60
    heures_total = minutes_total // 60
    heures_restantes = heures_total % 24
    journee_total = heures_total // 24
    heures_restantes = heures_total % 24
    annees_restantes = journee_total // 365
    journee_restante_annee = journee_total % 365
    mois_restants = int(journee_restante_annee // 30.4167)
    journee_restante_mois = int(round(journee_restante_annee % 30.4167))
    semaines_restantes = journee_restante_mois // 7
    jours_restants = journee_restante_mois % 7
    return Duree(
        secondes=secondes,
        jours=jours_restants,
        heures=heures_restantes,
        semaines=semaines_restantes,
        minutes=minutes_restantes,
        mois=mois_restants,
        annees=annees_restantes,
    )


def _calcule_repos(duree: Duree, nb_jours_repos: Union[int, float]) -> Duree:
    """Calcule la fin d'éxécution d'une tâche quand nous sommes en présence de jours de repos en semaine."""
    heures = duree._convertit_duration().hours
    minutes = duree._convertit_duration().minutes
    secondes = duree._convertit_duration().seconds
    jours = duree._convertit_duration().in_days()
    ## Calcule le temps nécessaire d'éxécution de la tache.
    semaines_totales = jours // (7 - nb_jours_repos)
    ##Calcule les temps pour qu'il ne reste pas de surplus de temps.
    jours_restants = jours % (7 - nb_jours_repos)
    annees_restantes = int(semaines_totales // 52.14)
    semaines_restantes_annee = int(round(semaines_totales % 52.14))
    mois_restants = int(semaines_restantes_annee // 4.3482)
    semaines_restantes = int(round(semaines_restantes_annee % 4.3482))
    return Duree(
        secondes=secondes,
        jours=jours_restants,
        heures=heures,
        semaines=semaines_restantes,
        minutes=minutes,
        mois=mois_restants,
        annees=annees_restantes,
    )


def _choix(
    duree: Duree,
    duree_max_journalier: Optional[Union[float, int]],
    nb_jours_repos: Optional[int],
):
    """Retourne la fin d'éxécution d'une tâche selon les conditions."""
    if duree_max_journalier is None and nb_jours_repos is None:
        return duree
    if duree_max_journalier is not None and nb_jours_repos is None:
        return _calcule_journalier(duree, duree_max_journalier)
    if duree_max_journalier is None and nb_jours_repos is not None:
        return _calcule_repos(duree, nb_jours_repos)
    else:
        return _calcule_repos(
            _calcule_journalier(duree, duree_max_journalier), nb_jours_repos
        )


def _choix2(
    demarrage: Duree,
    duree_tache: Duree,
    heures_execution: Optional[str],
    jours_repos: Optional[str],
):
    """Retourne la date de demarrage et la date de fin selon les conditions."""
    ## Pas de conditions renseignées
    if heures_execution is None and jours_repos is None:
        arrivee_valide = demarrage.add(duree_tache)
        return demarrage, arrivee_valide
    ## Seule la condition sur la durée journaliére d'éxécution est renseignée
    if heures_execution is not None and jours_repos is None:
        duree_max_journalier = _calcule_duree_max_journalier(heures_execution)
        arrivee = demarrage.add(_calcule_journalier(duree_tache, duree_max_journalier))
        demarrage_valide = _convertit_valide_heure(demarrage, heures_execution)
        arrivee_valide = _convertit_valide_heure(arrivee, heures_execution)
        return demarrage_valide, arrivee_valide
    ## Seule la condition les journées de repos hebdomadaires est renseignée
    if heures_execution is None and jours_repos is not None:
        nb_jours_repos = len(jours_repos.split())
        arrivee = demarrage.add(_calcule_repos(duree_tache, nb_jours_repos))
        demarrage_valide = _convertit_valide_repos(demarrage, jours_repos)
        arrivee_valide = _convertit_valide_repos(arrivee, jours_repos)
        return demarrage_valide, arrivee_valide
    ## Les deux conditions sont renseignées
    else:
        nb_jours_repos = len(jours_repos.split())
        duree_max_journalier = _calcule_duree_max_journalier(heures_execution)
        arrivee = demarrage.add(
            _calcule_repos(
                _calcule_journalier(duree_tache, duree_max_journalier), nb_jours_repos
            )
        )
        demarrage_valide = _convertit_valide_repos(
            _convertit_valide_heure(demarrage, heures_execution), jours_repos
        )
        arrivee_valide = _convertit_valide_repos(
            _convertit_valide_heure(arrivee, heures_execution), jours_repos
        )
        return demarrage_valide, arrivee_valide


def resous_EDT(
    probleme: Probleme,
    duree_max_journalier: Optional[Union[float, int]] = None,
    nb_jours_repos: Optional[Union[float, int]] = None,
) -> EDT:
    """Renvoie un calendrier optimal.

        [optionnel] duree_max_journalier
        Désigne le nombre d'heure journalié pour l'éxécution des tâches, la valeur par défaut est 24.
        Exemple :   - 8
                    - 23
        Attention ! Nous perdons de la précision avec cet argument

        [optionnel] nb_jours_repos
        Désigne le nombre de jours de repos hebdomadaire.
        Exemple :   - 2
                    - 6
        Attention ! Nous perdons de la précision avec cet argument

        Exemple:

        >>> mon_probleme.affiche_probleme()
                       Problème d'ordonnancement
    ┌───────┬─────────────────────┬────────────────────────────────┐
    │ Tâche │ Durée               │ Prérequis                      │
    ├───────┼─────────────────────┼────────────────────────────────┤
    │ A     │ 3 ans 2 semaines    │                                │
    │ B     │ 2 semaines 4 jours  │ fin de A + 2 jours 3 heures    │
    │ C     │ 2 heures 23 minutes │ debut de B + 2 jours 3 heures  │
    │ D     │ 3 ans               │ fin de A et fin de C + 10 mois │
    │ E     │ 1 seconde           │ fin de D                       │
    └───────┴─────────────────────┴────────────────────────────────┘
        >>> resolution=resous_EDT(mon_probleme)
        >>> resolution.affiche(entier=True)
                        Solution du problème : emploi du temps
    ┌───────┬──────────────────────┬───────────────────────┬──────────────────────┐
    │ Tâche │ Nature               │ Début                 │ Fin                  │
    ├───────┼──────────────────────┼───────────────────────┼──────────────────────┤
    │ A     │ Decryptage du        │ Débute au temps 0     │ 3 ans 2 semaines     │
    │       │ probleme             │                       │                      │
    │ B     │ Developpement du     │ 3 ans 2 semaines 2    │ 3 ans 4 semaines 6   │
    │       │ projet               │ jours 3 heures        │ jours 3 heures       │
    │ C     │ Envoyer la requête à │ 3 ans 2 semaines 4    │ 3 ans 2 semaines 4   │
    │       │ l'agence             │ jours 6 heures        │ jours 8 heures 23    │
    │       │                      │                       │ minutes              │
    │ D     │ Developpement de la  │ 3 ans 10 mois 2       │ 6 ans 10 mois 2      │
    │       │ plateforme publique  │ semaines 4 jours 8    │ semaines 4 jours 8   │
    │       │                      │ heures 23 minutes     │ heures 23 minutes    │
    │ E     │ Ouverture du projet  │ 6 ans 10 mois 2       │ 6 ans 10 mois 2      │
    │       │                      │ semaines 4 jours 8    │ semaines 4 jours 8   │
    │       │                      │ heures 23 minutes     │ heures 23 minutes 1  │
    │       │                      │                       │ seconde              │
    └───────┴──────────────────────┴───────────────────────┴──────────────────────┘
        >>> resolution=resous_EDT(mon_probleme, duree_max_journalier=12, nb_jours_repos=2)
        >>> resolution.affiche()
                        Solution du problème : emploi du temps
    ┌───────┬──────────────────────────────────┬──────────────────────────────────┐
    │ Tâche │ Début                            │ Fin                              │
    ├───────┼──────────────────────────────────┼──────────────────────────────────┤
    │ A     │ Débute au temps 0                │ 8 ans 5 mois 4 semaines 3 jours  │
    │ B     │ 8 ans 5 mois 4 semaines 5 jours  │ 8 ans 6 mois 7 semaines 6 jours  │
    │       │ 3 heures                         │ 3 heures                         │
    │ C     │ 8 ans 5 mois 5 semaines 6 heures │ 8 ans 5 mois 5 semaines 20       │
    │       │                                  │ heures 18 minutes                │
    │ D     │ 8 ans 15 mois 5 semaines 20      │ 16 ans 19 mois 9 semaines 20     │
    │       │ heures 18 minutes                │ heures 18 minutes                │
    │ E     │ 16 ans 19 mois 9 semaines 20     │ 16 ans 19 mois 9 semaines 20     │
    │       │ heures 18 minutes                │ heures 18 minutes 1 seconde      │
    └───────┴──────────────────────────────────┴──────────────────────────────────┘
    """

    graphe = genere_graphe(probleme)

    ##Conditions nécessaires au bon déroulement de l'algorithme
    if duree_max_journalier is not None:
        if duree_max_journalier <= 0 or duree_max_journalier >= 24:
            raise ValueError(
                "La durée maximum d'éxécution des tâches journalier doit-être strictement positive ou inférieure à 24."
            )
    if nb_jours_repos is not None:
        if nb_jours_repos <= 0 or nb_jours_repos > 6:
            raise ValueError(
                "Le nombre hebdomadaire de jours de repos doit être compris entre 1 et 6."
            )
    if not nx.is_directed_acyclic_graph(G=graphe):
        raise ValueError("Le problème n'a pas de solution.")
    ##################Algorithme##############################
    bon_ordre = [probleme[nom] for nom in nx.topological_sort(G=graphe)]
    resultat = EDT(activites=[])
    for tache_courante in bon_ordre:
        demarrage = _calcule_demarrage(tache=tache_courante, edt=resultat)
        arrivee = demarrage.add(
            _choix(tache_courante.duree, duree_max_journalier, nb_jours_repos)
        )
        resultat.ajoute(
            Activite(
                tache=tache_courante,
                debut=demarrage,
                fin=arrivee,
            )
        )
    return resultat


def resous_Calendrier(
    probleme: Probleme,
    date_commencement: Union[Date, str],
    heures_execution: Optional[str] = None,
    jours_repos: Optional[str] = None,
) -> Calendrier:
    """Renvoie un calendrier optimal.

        [optionnel] heures_execution
        Désigne la plage horaire d'éxécution des tâches, la valeur par défaut est 00h-00h.
        Exemple : 12.5-18.5
        Attention ! Nous perdons de la précision avec cet argument

        date_commencement
        Indique la date où commence l'éxécution des tâches
        Exemple :   - 12/10/1998
                    - 12/10/1998/12:34:01
                    - Date(jours=23, mois=10, annees= 1998, secondes=01)

        [optionnel] jours_repos
        Indique les jours où l'éxécution des tâches est arrétée.
        Exemple :   - Mardi Mercredi
                    - Lundi Vendredi
        Attention ! Nous perdons de la précision avec cet argument

        >>> mon_probleme.affiche_probleme()
                       Problème d'ordonnancement
    ┌───────┬─────────────────────┬────────────────────────────────┐
    │ Tâche │ Durée               │ Prérequis                      │
    ├───────┼─────────────────────┼────────────────────────────────┤
    │ A     │ 3 ans 2 semaines    │                                │
    │ B     │ 2 semaines 4 jours  │ fin de A + 2 jours 3 heures    │
    │ C     │ 2 heures 23 minutes │ debut de B + 2 jours 3 heures  │
    │ D     │ 3 ans               │ fin de A et fin de C + 10 mois │
    │ E     │ 1 seconde           │ fin de D                       │
    └───────┴─────────────────────┴────────────────────────────────┘
        >>> resolution=resous_Calendrier(mon_probleme, date_commencement="23/12/1998")
        >>> resolution.affiche()
                   Solution du problème : calendrier
    ┌───────┬──────────────────────────┬──────────────────────────┐
    │ Tâche │ Début                    │ Fin                      │
    ├───────┼──────────────────────────┼──────────────────────────┤
    │ A     │ 23 décembre 1998 à 00h00 │ 6 janvier 2002 à 00h00   │
    │ B     │ 8 janvier 2002 à 03h00   │ 26 janvier 2002 à 03h00  │
    │ C     │ 10 janvier 2002 à 06h00  │ 10 janvier 2002 à 08h23  │
    │ D     │ 10 novembre 2002 à 08h23 │ 10 novembre 2005 à 08h23 │
    │ E     │ 10 novembre 2005 à 08h23 │ 10 novembre 2005 à 08h23 │
    └───────┴──────────────────────────┴──────────────────────────┘
    >>> resolution=resous_Calendrier(mon_probleme, date_commencement="23/12/1998", jours_repos="Mardi mercredi", heures_execution="10-18")
    >>> resolution.affiche()
                    Solution du problème : calendrier
    ┌───────┬───────────────────────────┬───────────────────────────┐
    │ Tâche │ Début                     │ Fin                       │
    ├───────┼───────────────────────────┼───────────────────────────┤
    │ A     │ 24 décembre 1998 à 10h00  │ 22 septembre 2011 à 10h00 │
    │ B     │ 24 septembre 2011 à 13h00 │ 5 décembre 2011 à 13h00   │
    │ C     │ 26 septembre 2011 à 16h00 │ 29 septembre 2011 à 11h04 │
    │ D     │ 29 juillet 2012 à 11h04   │ 7 mars 2025 à 11h04       │
    │ E     │ 7 mars 2025 à 11h04       │ 7 mars 2025 à 11h04       │
    └───────┴───────────────────────────┴───────────────────────────┘
    """

    graphe = genere_graphe(probleme)
    if type(date_commencement) == str:
        date_commencement = _convertit_en_date(date_commencement)

    ##Conditions nécessaires au bon déroulement de l'algorithme
    if not nx.is_directed_acyclic_graph(G=graphe):
        raise ValueError("Le problème n'a pas de solution.")

    if jours_repos is not None:
        liste_verification = list()
        if len(jours_repos.split()) > 6:
            raise ValueError(
                "Vous ne pouvez prendre toutes les journées de la semaines en repos."
            )
        for temps in jours_repos.split():
            if temps in liste_verification:
                raise ValueError("Une journée est présente plusieurs fois.")
            else:
                liste_verification.append(temps)
    if heures_execution is not None:
        if (
            _calcule_duree_max_journalier(heures_execution) < 0
            or _calcule_duree_max_journalier(heures_execution) > 23.9
        ):
            raise ValueError(
                "La condition sur les heures journalières d'éxécution sont invalide"
            )
    ######################Algorithme###########################
    bon_ordre = [probleme[nom] for nom in nx.topological_sort(G=graphe)]
    resultat = Calendrier(dates=[])
    for tache_courante in bon_ordre:
        demarrage = _calcule_demarrage2(
            tache=tache_courante,
            calendrier=resultat,
            date_commencement=date_commencement,
        )
        demarrage_valide, arrivee_valide = _choix2(
            demarrage=demarrage,
            duree_tache=tache_courante.duree,
            heures_execution=heures_execution,
            jours_repos=jours_repos,
        )
        resultat.ajoute(
            Datation(
                tache=tache_courante,
                date_debut=demarrage_valide,
                date_fin=arrivee_valide,
            )
        )
    return resultat


def _convertit_en_date(message: str) -> Date:
    """Convertit un caractére valide en date."""
    return Date.par_str(message)


def _calcule_duree_max_journalier(heures_execution: str) -> Union[int, float]:
    """Calcule le temps de travail journalier."""
    inf, sup = heures_execution.split("-")
    if float(inf) > float(sup):
        return float(sup) + (24 - float(inf))
    elif float(sup) > float(inf):
        return float(sup) - float(inf)


def _convertit_valide_heure(date: Date, heures_execution: str) -> Date:
    """Convertit une date qui ne serait pas dans les heures d'éxécution de tâches."""
    inf, sup = heures_execution.split("-")
    inf = float(inf)
    sup = float(sup)
    limite = _calcule_duree_max_journalier(heures_execution)
    if date.heures * 60 + date.minutes < inf * 60:
        vrai_date = Date(
            jours=date.jours,
            annees=date.annees,
            mois=date.mois,
            heures=int((inf * 60) // 60),
            minutes=int(round(inf * 60) % 60),
            secondes=date.secondes,
        )
    elif date.heures * 60 + date.minutes > sup * 60:
        date = date.add(Duree(jours=1))
        vrai_date = Date(
            jours=date.jours,
            annees=date.annees,
            mois=date.mois,
            heures=int((inf * 60) // 60),
            minutes=int(round(inf * 60) % 60),
            secondes=date.secondes,
        )
    else:
        vrai_date = date
    return vrai_date


def _convertit_valide_repos(date: Date, jours_repos: str) -> Date:
    """Convertit une date qui serait dans les jours de repos."""
    liste_jour = list()
    for jours in jours_repos.split():
        liste_jour.append(jours.lower())
    ## Boucle qui décale la date à un jours non repos.
    while date._convertit_datetime().format("dddd", locale="fr") in liste_jour:
        date = date.add(Duree(jours=1))
    return date
