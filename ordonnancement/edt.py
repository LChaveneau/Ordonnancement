#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Contient les classes Activite et EDT.
"""
import matplotlib.pyplot as plt
from typing import Any, List, Union, Generator, Optional
from dataclasses import dataclass
from rich.table import Table
from .probleme import Nom, Tache, Prerequis, Duree
from .calendrier import Date, Calendrier
from pendulum import datetime


@dataclass
class Activite:
    """Tâche plannifiée."""

    tache: Tache
    debut: Duree
    fin: Duree

    def __post_init__(self):
        """Vérifie que la durée est respectée."""
        if self.fin < self.debut:
            raise ValueError(
                f"Les durées de l'activité correspondant à la tache {self.tache} ne respecte pas l'ordre."
            )
        if self.fin - self.debut < self.tache.duree:
            raise ValueError(
                f"L'activité correspondant à la tache {self.tache} ne respecte pas la durée."
            )


class EDT:
    """Emploi du temps.

            Exemple:
        >>> edt = EDT(activites=[
        Activite(tache=Tache(nom='A', duree=Duree(annees=3, semaines=2), prerequis=[], correspondance='Decryptage du probleme'), debu t=Duree(), fin=Duree(annees=3, semaines=2)),
        Activite(tache=Tache(nom='B', duree=Duree(semaines=2, jours=4), prerequis =[Prerequis(nom='A', typ='fin', latence=Duree(jours=2, heures=3))], correspondance='Developpement du projet'), debut=Duree(annees=3, semaines=2, jours=2, heures=3), fin=Duree(annees= 3, semaines=4, jours=6, heures=3)),
        Activite(tache=Tache(nom='C', duree=Duree(heures=2, minutes=23), prerequis =[Prerequis(nom='B', typ='debut', latence=Duree(jours=2, heures=3))], correspondance="Envoyer la requête à l'agence"), debut=Duree(annees=3, semaines=2, jours=4, heures=6), fin=Duree(annees=3, semaines=2, jours=4, heures=8, minutes=23))])

        >>> print(list(edt.activites))
    [Activite(tache=Tache(nom='A', duree=Duree(annees=3, semaines=2), prerequis=[], correspondance='Decryptage du probleme'), debut=Duree(Aucune durée), fin=Duree(annees=3, semaines=2)),
    Activite(tache=Tache(nom='B', duree=Duree(semaines=2, jours=4), prerequis=[Prerequis(nom='A', typ='fin', latence=Duree(jours=2, heures=3))], correspondance='Developpement du projet'), debut=Duree(annees=3, semaines=2, jours=2, heures=3), fin=Duree(annees=3, semaines=4, jours=6, heures=3)), Activite(tache=Tache(nom='C', duree=Duree(heures=2, minutes=23), prerequis=[Prerequis(nom='B', typ='debut', latence=Duree(jour
    s=2, heures=3))], correspondance="Envoyer la requête à l'agence"), debut=Duree(annees=3, semaines=2, jours=4, heures=6), fin=Duree(annees=3, semaines=2, jours=4, heures=8, minutes=23))]

        >>> edt["A"]
    Activite(tache=Tache(nom='A', duree=Duree(annees=3, semaines=2), prerequis=[], correspondance='Decryptage du probleme'), debut=Duree(Aucune durée), fin=Duree(annees=3, semaines=2))

        >>> edt_bis=EDT(activites=[])

        >>> edt_bis.ajoute(edt["A"])

        >>> print(edt_bis)
    EDT(activites=[Activite(tache=Tache(nom='A', duree=Duree(annees=3, semaines=2), prerequis=[], correspondance='Decryptage du probleme'), debut=Duree(Aucune durée), fin=Duree(annees=3, semaines=2))])

        >>> edt_bis.est_valide()
    True

        >>> edt_bis.ajoute(edt["B"])
        >>> edt_bis.ajoute(edt["C"])
        >>> edt_bis==edt
    True
        >>> edt.affiche()
                        Solution du problème : emploi du temps
    ┌───────┬──────────────────────────────────┬──────────────────────────────────┐
    │ Tâche │ Début                            │ Fin                              │
    ├───────┼──────────────────────────────────┼──────────────────────────────────┤
    │ A     │ Débute au temps 0                │ 3 ans 2 semaines                 │
    │ B     │ 3 ans 2 semaines 2 jours 3       │ 3 ans 4 semaines 6 jours 3       │
    │       │ heures                           │ heures                           │
    │ C     │ 3 ans 2 semaines 4 jours 6       │ 3 ans 2 semaines 4 jours 8       │
    │       │ heures                           │ heures 23 minutes                │
    └───────┴──────────────────────────────────┴──────────────────────────────────┘
    >>> edt.affiche(entier=True)
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
    └───────┴──────────────────────┴───────────────────────┴──────────────────────┘
        >>> edt_bis.ajoute(edt["A"])
    ValueError: La tâche A est déjà présente dans l'emploi du temps.

        >>> edt.ajoute(Activite(tache=Tache("E", duree=Duree(annees=4),prerequis=[]), debut=Duree(annees=5), fin=Duree(annees=6)))
    ValueError: L'activité correspondant à la tache Tache(nom='E', duree=Duree(annees=4), prerequis=[], correspondance=' ') ne respecte pas la durée.
        >>> edt.est_valide()
    False
        >>> edt_bis.est_valide()
    False"""

    def __init__(self, activites: List[Activite]):
        """Instancie à partir de la liste d'activites."""
        self._activites: List[Activite] = []
        for activite in activites:
            self.ajoute(activite)

    def __eq__(self, autre: Any) -> bool:
        """Pour ne pas tester l'identité de python."""
        if type(autre) != type(self):
            return False
        return self._activites == autre._activites

    def __repr__(self) -> str:
        """Représente l'emploi du temps."""
        return f"EDT(activites={self._activites})"

    @property
    def activites(self) -> Generator[Activite, None, None]:
        """Itére sur les activités."""
        yield from self._activites

    def __getitem__(self, nom: Nom) -> Activite:
        """Accède aux activités par leur nom de tâche."""
        for activite in self._activites:
            if activite.tache.nom == nom:
                return activite

        raise ValueError("Pas d'activité avec ce nom de tâche.")

    def ajoute(self, activite: Activite) -> "EDT":
        """Rajoute une nouvelle activité."""
        if any(activite.tache.nom == autre.tache.nom for autre in self.activites):
            raise ValueError(
                f"La tâche {activite.tache.nom} est déjà présente "
                "dans l'emploi du temps."
            )
        self._activites.append(activite)

    def est_valide(self) -> bool:
        """Vérifie si l'emploi du temps respecte les contraintes."""
        for activite in self.activites:
            for prerequis in activite.tache.prerequis:
                if activite.debut < self[prerequis.nom].fin:
                    return False
        return True

    def _genere_table(self, entier: bool, brute: bool) -> Table:
        """Retourne une table rich."""
        if entier:
            resultat = Table(title="Solution du problème : emploi du temps")
            resultat.add_column("Tâche")
            resultat.add_column("Nature")
            resultat.add_column("Début")
            resultat.add_column("Fin")
            for activite in self._activites:
                resultat.add_row(
                    activite.tache.nom,
                    activite.tache.correspondance,
                    str(activite.debut._choisi_brute(brute)),
                    activite.fin._choisi_brute(brute),
                )
        else:
            resultat = Table(title="Solution du problème : emploi du temps")
            resultat.add_column("Tâche")
            resultat.add_column("Début")
            resultat.add_column("Fin")
            for activite in self._activites:
                resultat.add_row(
                    activite.tache.nom,
                    activite.debut._choisi_brute(brute),
                    activite.fin._choisi_brute(brute),
                )

        return resultat

    def affiche(self, entier: Optional[bool] = False, brute: Optional[bool] = False):
        """Affiche l'emploi du temps.

        [optionnel] entier est un argument donnant la table avec ou sans les correspondances.

        [optionnel] brute est un argument qui re-travaille ou non les durées.

        """
        from rich import print

        print(self._genere_table(entier=entier, brute=brute))

    def genere_graphique(self) -> plt.Figure:
        """Renvoie une figure matplotlib."""
        figure, repere = plt.subplots()
        repere.set_ylabel("Tâches")
        repere.set_xlabel("Instants")
        repere.set_title("Solution du problème d'ordonnancement")
        x_ticks = list()
        x_labels = list()
        for indice, activite in enumerate(self.activites):
            repere.plot(
                [
                    activite.debut._convertit_duration().in_seconds(),
                    activite.fin._convertit_duration().in_seconds(),
                ],
                [-indice, -indice],
                linewidth=4,
            )
            x_ticks.append(activite.debut._convertit_duration().in_seconds())
            x_ticks.append(activite.fin._convertit_duration().in_seconds())
            x_labels.append(activite.debut._retourne_temps_calculee())
            x_labels.append(activite.fin._retourne_temps_calculee())
        repere.set_yticks([-indice for indice, _ in enumerate(self.activites)])
        repere.set_yticklabels([activite.tache.nom for activite in self.activites])
        repere.set_xticks(x_ticks)
        ax = repere.set_xticklabels(x_labels, rotation="vertical")
