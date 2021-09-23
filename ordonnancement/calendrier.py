#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Contient les classes Date, Datation et Calendrier.
"""
import matplotlib.pyplot as plt
from typing import Any, List, Union, Generator, Dict, Optional
from dataclasses import dataclass
from rich.table import Table
from .probleme import Nom, Tache, Prerequis, Duree
from pendulum import datetime


@dataclass
class Date:
    """Une date
        >>> date=Date(jours=23,mois=12,annees=1998)

        >>> date.add(Duree(secondes=3))
    Date(jours=23, mois=12, annees=1998, heures=0, minutes=0, secondes=3)

        >>> date - Duree(secondes=3)
    Date(jours=22, mois=12, annees=1998, heures=23, minutes=59, secondes=57)

        >>> date_bis=Date.par_str("23/12/1998")

        >>> date_bis==date
    True

        >>> date_bis=Date.par_str("23/12/1998/12:00")

        >>> date_bis
    Date(jours=23, mois=12, annees=1998, heures=12, minutes=0, secondes=0)"""

    def __init__(self, jours, mois, annees, heures=0, minutes=0, secondes=0):
        """Construction de la classe Date et stockage sous forme de dict des durées."""
        ##Creation de l'objet
        self.jours = jours
        self.mois = mois
        self.annees = annees
        self.heures = heures
        self.minutes = minutes
        self.secondes = secondes

        ##Dict sur les temps
        self._temps = dict()
        self._temps["jours"] = self.jours
        self._temps["mois"] = self.mois
        self._temps["annees"] = self.annees
        self._temps["heures"] = self.heures
        self._temps["minutes"] = self.minutes
        self._temps["secondes"] = self.secondes

        self._est_valide()

    def _est_valide(self):
        """Détecte la validité de la date."""
        for clefs in self._temps.keys():
            if self._temps[clefs] < 0:
                raise ValueError("Vous devez indiquer une date valide.")
        self._erreur()

    def _erreur(self):
        """Détecte les erreurs relatives à la mauvaise construction d'une date"""
        ## Erreurs évidentes
        if self.jours > 31 or self.jours == 0:
            raise ValueError("Le jour doit être compris entre 1 et 31.")
        if self.mois > 12 or self.mois == 0:
            raise ValueError("Le mois doit être compris entre 1 et 12.")
        if self.heures > 23:
            raise ValueError("L'heure doit être comprise entre 0 et 23.")
        if self.minutes > 59:
            raise ValueError("Les minutes doivent être valides.")
        if self.secondes > 59:
            raise ValueError("Les secondes doivent être valides.")

        ## Erreurs plus complexes
        try:
            self._convertit_datetime()
        except ValueError as VE:
            if str(VE) == "day is out of range for month":
                raise ValueError(
                    "Le numéro de la journée est indisponible pour le mois sélectionné."
                )
            else:
                raise VE

    def _convertit_datetime(self) -> datetime:
        """Renvoi le temps sous forme d'un objet datetime"""
        return datetime(
            day=self.jours,
            second=self.secondes,
            minute=self.minutes,
            hour=self.heures,
            month=self.mois,
            year=self.annees,
        )

    @classmethod
    def _convertit_date(cls, datetime: datetime) -> "Date":
        """Convertit un objet datetime en objet Date"""
        return cls._convertion(datetime)

    def _convertion(datetime: datetime) -> "Date":
        return Date(
            secondes=datetime.second,
            jours=datetime.day,
            minutes=datetime.minute,
            heures=datetime.hour,
            mois=datetime.month,
            annees=datetime.year,
        )

    def _retourne_date(self) -> str:
        """Retourne la date sous forme de message jour/mois/annee."""
        return self._convertit_datetime().format("D MMMM YYYY", locale="fr")

    def _retourne_date_heure(self) -> str:
        """Retourne la date sous forme de message jour/mois/annee heure minute."""
        return self._convertit_datetime().format("D MMMM YYYY à HH\hmm", locale="fr")

    def _retourne_date_heure_secondes(self) -> str:
        """Retourne la date sous forme de message jour/mois/annee heure minute secondes."""
        return self._convertit_datetime().format(
            "D MMMM YYYY à HH\hmm et ss \s\e\c\on\d\e\s", locale="fr"
        )

    def add(self, autre: Duree) -> "Date":
        """Additionne la durée d'un objet Duree à une date."""
        date_a_traiter = self._convertit_datetime()
        duree_a_traiter = autre._convertit_duration()
        date_final = date_a_traiter + duree_a_traiter
        return self._convertit_date(date_final)

    def temps(self) -> Dict:
        """Renvoi un dict du jour, mois et année d'une date"""
        temps = dict()
        temps["jours"] = self.jours
        temps["mois"] = self.mois
        temps["annees"] = self.annees
        return temps

    def temps_total(self) -> Dict:
        """Renvoi un dict de la date en entière."""
        temps_total = dict()
        for valeur in self.temps(), self.heure():
            temps_total.update(valeur)
        return temps_total

    def heure(self) -> Dict:
        """Renvoi un dict de l'heure de la date."""
        heure = dict()
        heure["heures"] = self.heures
        heure["minutes"] = self.minutes
        heure["secondes"] = self.secondes
        return heure

    def __eq__(self, autre: Any) -> bool:
        """Egalite."""
        if type(autre) != type(self):
            raise ValueError(
                "Vous ne pouvez comparer l'égalité entre des types d'objets différents"
            )
        return self._convertit_datetime() == autre._convertit_datetime()

    def __ne__(self, autre: Any) -> bool:
        """inégalite."""
        if type(autre) != type(self):
            raise ValueError(
                "Vous ne pouvez comparer l'inégalité entre des types d'objets différents"
            )
        return self._convertit_datetime() != autre._convertit_datetime()

    def __ge__(self, autre: Any) -> bool:
        """Supériorité"""
        if type(autre) != type(self):
            raise ValueError(
                "Vous ne pouvez comparer la supériorité entre des types d'objets différents"
            )
        return self._convertit_datetime() >= autre._convertit_datetime()

    def __gt__(self, autre: Any) -> bool:
        """Supériorité stricte"""
        if type(autre) != type(self):
            raise ValueError(
                "Vous ne pouvez comparer la supériorité stricte entre des types d'objets différents"
            )
        return self._convertit_datetime() > autre._convertit_datetime()

    def __le__(self, autre: Any) -> bool:
        """Infériorité"""
        if type(autre) != type(self):
            raise ValueError(
                "Vous ne pouvez comparer l'infériorité entre des types d'objets différents"
            )
        return self._convertit_datetime() <= autre._convertit_datetime()

    def __lt__(self, autre: Any) -> bool:
        """Infériorité stricte"""
        if type(autre) != type(self):
            raise ValueError(
                "Vous ne pouvez comparer l'infériorité stricte entre des types d'objets différents"
            )
        return self._convertit_datetime() < autre._convertit_datetime()

    def __add__(self, autre: Duree) -> "Date":
        """Additionne une durée à une date."""
        return self.add(autre)

    def __sub__(self, autre: Duree) -> "Date":
        """Soustrait une durée à une date."""
        date_a_traiter = self._convertit_datetime()
        duree_a_traiter = autre._convertit_duration()
        date_final = date_a_traiter - duree_a_traiter
        return self._convertit_date(date_final)

    def __repr__(self) -> str:
        """Renvoie la liste de construction."""
        i = 0
        message = ""
        if self.secondes == 0 and self.heures == 0 and self.minutes == 0:
            for temps in self.temps():
                i = i + 1
                if i < len(self.temps()):
                    message += f"{temps}={self.temps()[temps]}, "
                else:
                    message += f"{temps}={self.temps()[temps]}"
            return f"Date({message})"
        else:
            for temps in self.temps_total():
                i = i + 1
                if i < len(self.temps_total()):
                    message += f"{temps}={self.temps_total()[temps]}, "
                else:
                    message += f"{temps}={self.temps_total()[temps]}"
            return f"Date({message})"

    def __getitem__(self, nom: Nom) -> int:
        """Accès aux valeurs des temporalités."""
        return self._temps[nom]

    @classmethod
    def par_str(cls, message: str) -> "Date":
        """Constructeur alternatif pour la classe Date.

        Ce constructeur alternatif se construit comme suit:
        "JJ/MM/AAAA/HH:MM:SS"

        JJ : Jours
        MM : Mois
        AAAA : Annes
        [optionnel] HH : Heures
        [optionnel] MM : Minutes
        [optionnel] SS : Secondes
        """
        if len(message.split("/")) == 4:
            jour, mois, annees, heure = message.split("/")
            if len(heure.split(":")) == 3:
                heures, minutes, secondes = heure.split(":")
            elif len(heure.split(":")) == 2:
                heures, minutes = heure.split(":")
                secondes = "0"
            elif len(heure.split(":")) == 1:
                heures = heure.split(":")
                minutes, secondes = "0", "0"
            else:
                raise ValueError("Vous avez mal rempli l'heure de la date")
        elif len(message.split("/")) == 3:
            jour, mois, annees = message.split("/")
            heures, minutes, secondes = "0", "0", "0"
        else:
            raise ValueError("Vous avez mal rempli les valeurs de la date.")
        jours_valide = cls._encode(jour)
        mois_valide = cls._encode(mois)
        annees_valide = cls._encode(annees)
        heures_valide = cls._encode(heures)
        minutes_valide = cls._encode(minutes)
        secondes_valide = cls._encode(secondes)
        return Date(
            jours=jours_valide,
            mois=mois_valide,
            annees=annees_valide,
            heures=heures_valide,
            minutes=minutes_valide,
            secondes=secondes_valide,
        )

    @staticmethod
    def _encode(valeur) -> "Date":
        """Aide au constructeur alternatif."""
        try:
            valeur_valide = int(valeur)
        except ValueError:
            raise ValueError(f"La valeur {valeur} n'est pas numérique")
        return valeur_valide


@dataclass
class Datation:
    tache: Tache
    date_debut: Date
    date_fin: Date

    def __post_init__(self):
        """Vérifie que la durée est respectée."""
        if self.date_fin < self.date_debut:
            raise ValueError(
                f"Les durées de l'activité correspondant à la tache {self.tache} ne respecte pas l'ordre."
            )
        if self.date_fin - self.tache.duree < self.date_debut:
            raise ValueError(
                f"L'activité correspondant à la tache {self.tache} ne respecte pas la durée."
            )


class Calendrier:
    """Calendrier
        Exemple :

        >>> calendrier=Calendrier(dates=[
        Datation(tache=Tache(nom='A', duree=Duree(annees=3, semaines=2), prerequis=[], correspondance='Decryptage du probleme'), date_debut=Date(jours=23, mois=12, annees=1998), date_fin=Date(jours=6, mois=1, annees=2002)),
        Datation(tache=Tache(nom='B', duree=Duree(semaines=2, jours=4), prerequis=[Prerequis(nom='A', typ='fin', latence=Duree(jours=2, heures=3))], correspondance ='Developpement du projet'), date_debut=Date(jours=8, mois=1, annees=2002, heures=3, minutes=0, secondes=0), date_fin=Date(jours=26, mois=1, annees=2002, heures=3, minutes=0, secondes=0)),
        Datation(tache=Tache(nom='C', duree=Duree(heures=2, minutes=23), prerequis=[Prerequis(nom='B', typ='debut', latence=Duree(jours=2, heures=3))], correspondance="Envoyer la requête à l'agence"), date_debut=Date(jours=10, mois=1, annees=2002, heures=6, minutes=0, secondes=0), date_fin=Date(jours=10,mois=1, annees=2002, heures=8, minutes=23, secondes=0))])

        >>> list(calendrier.dates)
    [
    Datation(tache=Tache(nom='A', duree=Duree(annees=3, semaines=2), prerequis=[], correspondance='Decryptage du probleme'), date_debut=Date(jours=23, mois=12, annees=1998), date_fin=Date(jours=6, mois=1, annees=2002)),
    Datation(tache=Tache(nom='B', duree=Duree(semaines=2, jours=4), prerequis [Prerequis(nom='A', typ='fin', latence=Duree(jours=2, heures=3))], correspondance ='Developpement du projet'), date_debut=Date(jours=8, mois=1, annees=2002, heures=3, minutes=0, secondes=0), date_fin=Date(jours=26, mois=1, annees=2002, heures=3, minutes=0, secondes=0)),
    Datation(tache=Tache(nom='C', duree=Duree(heures=2, minutes =23), prerequis=[Prerequis(nom='B', typ='debut', latence=Duree(jours=2, heures=3))], correspondance="Envoyer la requête à l' agence"), date_debut=Date(jours=10, mois=1, annees=2002, heures=6, minutes=0, secondes=0), date_fin=Date(jours=10, mois=1, annees=2002, heures=8, minutes=23, secondes=0))
    ]

    >>> calendrier["A"]
    Datation(tache=Tache(nom='A', duree=Duree(annees=3, semaines=2), prerequis=[], correspondance='Decryptage du probleme'), date_debut=Date(jours=23, mois=12, annees=1998), date_fin=Date(jours=6, mois=1, annees=2002))

        >>> calendrier.est_valide()
    False

        >>> calendrier_bis=Calendrier(dates=[])

        >>> calendrier_bis.ajoute(calendrier["A"])

        >>> calendrier_bis.est_valide()
    True

        >>> calendrier_bis
    Calendrier(dates=[Datation(tache=Tache(nom='A', duree=Duree(annees=3, semaines=2), prerequis=[], correspondance='Decryptage du probleme'), date_debut=Date(jours=23, mois=12, annees=1998), date_fin=Date(jours=6, mois=1, annees=2002))])

        >>> calendrier_bis.ajoute(calendrier["B"])

        >>> calendrier_bis.ajoute(calendrier["C"])

        >>> calendrier_bis==calendrier
    True

        >>> calendrier.affiche()
                          Solution du problème : calendrier
    ┌───────┬──────────────────────────┬─────────────────────────┐
    │ Tâche │ Début                    │ Fin                     │
    ├───────┼──────────────────────────┼─────────────────────────┤
    │ A     │ 23 décembre 1998 à 00h00 │ 6 janvier 2002 à 00h00  │
    │ B     │ 8 janvier 2002 à 03h00   │ 26 janvier 2002 à 03h00 │
    │ C     │ 10 janvier 2002 à 06h00  │ 10 janvier 2002 à 08h23 │
    └───────┴──────────────────────────┴─────────────────────────┘

    >>> calendrier.affiche(entier=True)
                           Solution du problème : calendrier
    ┌───────┬──────────────────────┬───────────────────────┬──────────────────────┐
    │ Tâche │ Nature               │ Début                 │ Fin                  │
    ├───────┼──────────────────────┼───────────────────────┼──────────────────────┤
    │ A     │ Decryptage du        │ 23 décembre 1998 à    │ 6 janvier 2002 à     │
    │       │ probleme             │ 00h00                 │ 00h00                │
    │ B     │ Developpement du     │ 8 janvier 2002 à      │ 26 janvier 2002 à    │
    │       │ projet               │ 03h00                 │ 03h00                │
    │ C     │ Envoyer la requête à │ 10 janvier 2002 à     │ 10 janvier 2002 à    │
    │       │ l'agence             │ 06h00                 │ 08h23                │
    └───────┴──────────────────────┴───────────────────────┴──────────────────────┘"""

    def __init__(self, dates: List[Datation]):
        """Instancie à partir de la liste de date."""
        self._dates: List[Datation] = []
        for date in dates:
            self.ajoute(date)

    def __eq__(self, autre: Any) -> bool:
        """Pour ne pas tester l'identité de python."""
        if type(autre) != type(self):
            return False
        return self._dates == autre._dates

    def __repr__(self) -> str:
        """Représentation."""
        return f"Calendrier(dates={self._dates})"

    @property
    def dates(self) -> Generator[Datation, None, None]:
        """Itére sur les dates."""
        yield from self._dates

    def __getitem__(self, nom: Nom) -> Datation:
        """Accède aux date par leur nom de tâche."""
        for date in self._dates:
            if date.tache.nom == nom:
                return date

        raise ValueError("Pas d'activité avec ce nom de tâche.")

    def ajoute(self, date: Date) -> "Calendrier":
        """Rajoute une nouvelle activité."""
        if any(date.tache.nom == autre.tache.nom for autre in self.dates):
            raise ValueError(
                f"La tache {date.tache.nom} est déjà présente "
                "dans l'emploi du temps."
            )
        self._dates.append(date)

    def est_valide(self) -> bool:
        """Vérifie si le calendrier respecte les contraintes."""
        for datation in self.dates:
            for prerequis in datation.tache.prerequis:
                if datation.date_debut < self[prerequis.nom].date_fin:
                    return False
        return True

    def _genere_table(self, entier: bool) -> Table:
        """Retourne une table rich."""
        if entier:
            resultat = Table(title="Solution du problème : calendrier")
            resultat.add_column("Tâche")
            resultat.add_column("Nature")
            resultat.add_column("Début")
            resultat.add_column("Fin")
            for date in self._dates:
                resultat.add_row(
                    date.tache.nom,
                    date.tache.correspondance,
                    self._choix_affichage_date(date.date_debut),
                    self._choix_affichage_date(date.date_fin),
                )
        else:
            resultat = Table(title="Solution du problème : calendrier")
            resultat.add_column("Tâche")
            resultat.add_column("Début")
            resultat.add_column("Fin")
            for date in self._dates:
                resultat.add_row(
                    date.tache.nom,
                    self._choix_affichage_date(date.date_debut),
                    self._choix_affichage_date(date.date_fin),
                )

        return resultat

    def affiche(self, entier: Optional[bool] = False):
        """Affiche le calendrier en tableau.

        [optionnel] entier est un argument donnant la table avec ou sans les correspondances.

        [optionnel] brute est un argument qui re-travaille ou non les durées.

        """
        from rich import print

        print(self._genere_table(entier=entier))

    def genere_graphique(self) -> plt.Figure:
        """Renvoie une figure matplotlib."""
        figure, repere = plt.subplots()
        repere.set_ylabel("Tâches")
        repere.set_xlabel("Dates")
        repere.set_title("Solution du problème d'ordonnancement")
        x_ticks = list()
        x_labels = list()
        for indice, datation in enumerate(self.dates):
            repere.plot(
                [
                    datation.date_debut._convertit_datetime().int_timestamp,
                    datation.date_fin._convertit_datetime().int_timestamp,
                ],
                [-indice, -indice],
                linewidth=5,
            )
            x_ticks.append(datation.date_debut._convertit_datetime().int_timestamp)
            x_ticks.append(datation.date_fin._convertit_datetime().int_timestamp)
            x_labels.append(datation.date_debut._retourne_date())
            x_labels.append(datation.date_fin._retourne_date())
        repere.set_yticks([-indice for indice, _ in enumerate(self.dates)])
        repere.set_yticklabels([datation.tache.nom for datation in self.dates])
        repere.set_xticks(x_ticks)
        repere.set_xticklabels(x_labels, rotation="vertical")
        return repere

    def _choix_affichage_date(self, date_a_traiter: Date) -> str:
        """Décide de l'affichage des dates dans le tableau"""
        if any(
            datation.date_fin.secondes > 0 or datation.date_debut.secondes > 0
            for datation in self.dates
        ):
            return date_a_traiter._retourne_date_heure_secondes()
        elif any(
            datation.date_fin.heures > 0
            or datation.date_debut.heures > 0
            or datation.date_fin.minutes > 0
            or datation.date_debut.minutes > 0
            for datation in self.dates
        ):
            return date_a_traiter._retourne_date_heure()
        else:
            return date_a_traiter._retourne_date()
