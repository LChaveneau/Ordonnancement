#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Classes Tache, Duree, Prerequis et Probleme permettant de décrire le problème d'ordonnancement.

"""
from typing import Any, Dict, List, Union, Generator, Tuple, Optional
from dataclasses import dataclass
from rich.table import Table
from pendulum import duration
import functools

Nom = str
Typ = str
Correspondance = str


@dataclass
class Duree:
    """Représente une durée
        >>> ma_duree_bis=Duree.par_str("56 annees + 23 jours + 34 semaines + 32 secondes")
        >>> ma_duree=Duree(jours=23, semaines=34, annees=56, secondes=32)
        >>> ma_duree==ma_duree_bis
    True
        >>> ma_duree+ma_duree_bis
    Duree(annees=112, semaines=68, jours=46, secondes=64)
        >>> ma_duree.add(ma_duree_bis)
    Duree(annees=112, semaines=68, jours=46, secondes=64)
        >>> ma_duree-ma_duree_bis
    Duree(Aucune durée)
        >>> ma_duree["secondes"]
    32"""

    def __init__(
        self, secondes=0, minutes=0, heures=0, jours=0, semaines=0, mois=0, annees=0
    ):

        ## Construction de l'objet.
        self.secondes = secondes
        self.minutes = minutes
        self.heures = heures
        self.jours = jours
        self.semaines = semaines
        self.mois = mois
        self.annees = annees

        ## Dict sur les temps.
        self._temps = dict()
        self._temps["secondes"] = self.secondes
        self._temps["minutes"] = self.minutes
        self._temps["heures"] = self.heures
        self._temps["jours"] = self.jours
        self._temps["semaines"] = self.semaines
        self._temps["mois"] = self.mois
        self._temps["annees"] = self.annees

        ## Verification si les valeurs ne sont pas négatifs.
        for clefs in self._temps.keys():
            if self._temps[clefs] < 0:
                raise ValueError("Vous devez indiquer des durées positifs.")

    def _convertit_duration(self) -> duration:
        """Renvoie le temps sous forme d'objet Duration"""
        return duration(
            days=self.jours,
            seconds=self.secondes,
            minutes=self.minutes,
            hours=self.heures,
            weeks=self.semaines,
            months=self.mois,
            years=self.annees,
        )

    @classmethod
    def _convertit_duree(cls, duration: duration) -> "Duree":
        """Convertit un objet duration en objet Duree."""
        return Duree(
            secondes=duration.seconds,
            jours=duration.days,
            minutes=duration.minutes,
            heures=duration.hours,
        )

    def _choisi_brute(self, brute: bool) -> str:
        """Traite le retour message de la durée re-calculée ou non."""
        if brute:
            message = self._retourne_temps_brut()
        else:
            message = self._retourne_temps_calculee()
        return message

    def _retourne_temps_calculee(self) -> str:
        """Retourne la durée re-travaillée sous forme de message."""
        if self == Duree():
            return "Débute au temps 0"
        else:
            temps_brut = self._convertit_duration()
            return temps_brut.in_words(locale="fr")

    def _retourne_temps_brut(self) -> str:
        "Retourne la durée brute sous forme de message"
        if self == Duree():
            return "0"
        else:
            message = ""
            for temps in self.temps():
                message += f"{self.temps()[temps]} {temps} "
            return message

    def add(self, autre: Any) -> "Duree":
        """Additionne les durées de deux objets Duree"""
        return Duree(
            secondes=self.secondes + autre.secondes,
            minutes=self.minutes + autre.minutes,
            heures=self.heures + autre.heures,
            jours=self.jours + autre.jours,
            semaines=self.semaines + autre.semaines,
            mois=self.mois + autre.mois,
            annees=self.annees + autre.annees,
        )

    def temps(self) -> Dict:
        """Renvoie un dict des durées supérieurs à 0."""
        temps = dict()
        if self.annees > 0:
            temps["annees"] = self.annees
        if self.mois > 0:
            temps["mois"] = self.mois
        if self.semaines > 0:
            temps["semaines"] = self.semaines
        if self.jours > 0:
            temps["jours"] = self.jours
        if self.heures > 0:
            temps["heures"] = self.heures
        if self.minutes > 0:
            temps["minutes"] = self.minutes
        if self.secondes > 0:
            temps["secondes"] = self.secondes
        return temps

    def __eq__(self, autre: Any) -> bool:
        """Egalite."""
        if type(autre) != type(self):
            raise ValueError(
                "Vous ne pouvez comparer l'égalité entre des types d'objets différents"
            )
        return self._convertit_duration() == autre._convertit_duration()

    def __ne__(self, autre: Any) -> bool:
        """Inégalite."""
        if type(autre) != type(self):
            raise ValueError(
                "Vous ne pouvez comparer l'inégalité entre des types d'objets différents"
            )
        return self._convertit_duration() != autre._convertit_duration()

    def __ge__(self, autre: Any) -> bool:
        """Supériorité"""
        if type(autre) != type(self):
            raise ValueError(
                "Vous ne pouvez comparer la supériorité entre des types d'objets différents"
            )
        return self._convertit_duration() >= autre._convertit_duration()

    def __gt__(self, autre: Any) -> bool:
        """Supériorité stricte"""
        if type(autre) != type(self):
            raise ValueError(
                "Vous ne pouvez comparer la supériorité stricte entre des types d'objets différents"
            )
        return self._convertit_duration() > autre._convertit_duration()

    def __le__(self, autre: Any) -> bool:
        """Infériorité"""
        if type(autre) != type(self):
            raise ValueError(
                "Vous ne pouvez comparer l'infériorité entre des types d'objets différents"
            )
        return self._convertit_duration() <= autre._convertit_duration()

    def __lt__(self, autre: Any) -> bool:
        """Infériorité stricte"""
        if type(autre) != type(self):
            raise ValueError(
                "Vous ne pouvez comparer l'infériorité stricte entre des types d'objets différents"
            )
        return self._convertit_duration() < autre._convertit_duration()

    def __add__(self, autre: Any) -> "Duree":
        """Additionne deux durées."""
        return self.add(autre)

    def __sub__(self, autre: Any) -> "Duree":
        """Soustrait deux durées."""
        return Duree(
            secondes=self.secondes - autre.secondes,
            minutes=self.minutes - autre.minutes,
            heures=self.heures - autre.heures,
            jours=self.jours - autre.jours,
            semaines=self.semaines - autre.semaines,
            mois=self.mois - autre.mois,
            annees=self.annees - autre.annees,
        )

    def __repr__(self) -> str:
        """Renvoie la liste de construction."""
        i = 0
        message = ""
        if self == Duree():
            message = "Aucune durée"
        else:
            for temps in self.temps():
                i = i + 1
                if i < len(self.temps()):
                    message += f"{temps}={self.temps()[temps]}, "
                else:
                    message += f"{temps}={self.temps()[temps]}"
        return f"Duree({message})"

    def __getitem__(self, temps: str) -> int:
        """Accès aux valeurs des temporalités."""
        return self._temps[temps]

    @classmethod
    def par_str(cls, message: str) -> "Duree":
        """Constructeur alternatif pour la classe Duree."""
        duree = Duree()
        for temps in message.split("+"):
            valeur, type_temps = temps.split()
            try:
                valeur_valide = int(valeur)
            except ValueError:
                raise ValueError(f"La valeur {valeur} n'est pas numérique")
            duree = duree.add(cls._traite_methode(valeur_valide, type_temps.strip()))
        return duree

    @staticmethod
    def _traite_methode(valeur: int, type_temps: str) -> "Duree":
        """Aide au constructeur alternatif"""
        if type_temps == "secondes" or type_temps == "seconde":
            return Duree(secondes=valeur)
        if type_temps == "minutes" or type_temps == "minute":
            return Duree(minutes=valeur)
        if type_temps == "heures" or type_temps == "heure":
            return Duree(heures=valeur)
        if type_temps == "jours" or type_temps == "jour":
            return Duree(jours=valeur)
        if type_temps == "semaines" or type_temps == "semaine":
            return Duree(semaines=valeur)
        if type_temps == "mois":
            return Duree(mois=valeur)
        if (
            type_temps == "annee"
            or type_temps == "annees"
            or type_temps == "ans"
            or type_temps == "an"
        ):
            return Duree(annees=valeur)
        else:
            raise ValueError(f"Le type de temps {type_temps} n'est pas valide.")


@dataclass
class Prerequis:
    """Représente un prérequis"""

    nom: Nom
    typ: Typ
    latence: Duree

    def __post_init__(self):
        """Vérification"""
        if self.typ == "debut" or self.typ == "fin":
            pass
        else:
            raise ValueError("Le type de prérequis doit-être 'fin' ou 'debut'")
        if not isinstance(self.latence, Duree):
            raise ValueError("La latence doit-être un objet Duree")

    @classmethod
    def par_str(cls, message: str) -> "Prerequis":
        """Constructeur alternatif pour un objet Prérequis."""
        return cls._encode(message)

    @staticmethod
    def _encode(message: str) -> "Prerequis":
        """Aide pour le constructeur alternatif"""
        if len(message.split("(")) == 2:
            typage, duree = message.split("(")
            typage = typage.strip()
            for valeur in duree.split(")"):
                if valeur.strip():
                    duree_valide = Duree.par_str(valeur)
        ## Accepte le fait qu'il n'y ait rien remplis pour la durée. La durée sera égale à 0.
        elif len(message.split("(")) == 1:
            typage = message.strip()
            duree_valide = Duree()
        nom_valide, typ_valide = typage.strip().split(" ")
        return Prerequis(nom=nom_valide, typ=typ_valide, latence=duree_valide)


@dataclass
class Tache:
    """Représente une tâche."""

    nom: Nom
    duree: Duree
    prerequis: List[Prerequis]
    correspondance: Optional[Correspondance] = " "

    def __post_init__(self):
        """Vérifie que la durée d'une tâche est positive."""
        liste_verification = list()
        if self.duree._convertit_duration() == duration(0):
            raise ValueError("Veuillez indiquer une durée non nul")
        for prerequis in self.prerequis:
            if prerequis.nom in liste_verification:
                raise ValueError(
                    f"Les prérequis doivent comporter des noms de tâches différents.\n{prerequis.nom} est présent plusieurs fois "
                )
            else:
                liste_verification.append(prerequis.nom)
            if prerequis.nom in self.nom:
                raise ValueError(
                    f"Vous ne pouvez pas associé un pré-requis à un nom de tâche, qui à le même nom."
                )
        liste_verification = None

    def _messages_(self, brute: bool) -> str:
        """Choisit si le message est de type brute ou non brute."""
        i = 0
        message = ""
        for prerequis in self.prerequis:
            if brute:
                message += self._message_brut(prerequis, i, len(self.prerequis))
                i = i + 1
            else:
                message += self._message_non_brut(prerequis, i, len(self.prerequis))
                i = i + 1
        return message

    @staticmethod
    def _message_non_brut(prerequis: Prerequis, i: int, borne: int) -> str:
        """Décrit un prérequis sous forme de texte. Les durées sont en format re-calculé"""
        message = ""
        if i == 0:
            if prerequis.latence == Duree():
                message = prerequis.typ + " de " + prerequis.nom
            else:
                message = (
                    prerequis.typ
                    + " de "
                    + prerequis.nom
                    + " + "
                    + prerequis.latence._retourne_temps_calculee()
                )
        elif i < borne - 1:
            if prerequis.latence == Duree():
                message += ", " + prerequis.typ + " de " + prerequis.nom
            else:
                message += (
                    ", "
                    + prerequis.typ
                    + " de "
                    + prerequis.nom
                    + " + "
                    + prerequis.latence._retourne_temps_calculee()
                )
        else:
            if prerequis.latence == Duree():
                message += " et " + prerequis.typ + " de " + prerequis.nom
            else:
                message += (
                    " et "
                    + prerequis.typ
                    + " de "
                    + prerequis.nom
                    + " + "
                    + prerequis.latence._retourne_temps_calculee()
                )
        return message

    @staticmethod
    def _message_brut(prerequis: Prerequis, i: int, borne: int) -> str:
        """Décrit un prérequis sous forme de texte. Les durées sont en format brute."""
        message = ""

        ## Commencement du message
        if i == 0:
            if prerequis.latence == Duree():
                message = prerequis.typ + " de " + prerequis.nom
                i = i + 1
            else:
                message = (
                    prerequis.typ
                    + " de "
                    + prerequis.nom
                    + " + "
                    + prerequis.latence._retourne_temps_brut()
                )
                i = i + 1
        ## Suite du message
        elif i < borne - 1:
            if prerequis.latence == Duree():
                message += ", " + prerequis.typ + " de " + prerequis.nom
                i = i + 1
            else:
                message += (
                    ", "
                    + prerequis.typ
                    + " de "
                    + prerequis.nom
                    + " + "
                    + prerequis.latence._retourne_temps_brut()
                )
                i = i + 1
        ## Fin de message
        else:
            if prerequis.latence == Duree():
                message += " et " + prerequis.typ + " de " + prerequis.nom
                i = i + 1
            else:
                message += (
                    " et "
                    + prerequis.typ
                    + " de "
                    + prerequis.nom
                    + " + "
                    + prerequis.latence._retourne_temps_brut()
                )
                i = i + 1
        return message


class Probleme:
    """Représente un problème d'ordonnancement

        mon_probleme = Probleme(taches=[
        Tache(nom='A', duree=Duree(annees=3, semaines=2), prerequis=[], correspondance='Decryptage du probleme'),
        Tache(nom='B', duree=Duree(semaines=2, jours=4), prerequis=[Prerequis(nom='A', typ='fin', latence=Duree(jours=2, heures=3))], correspondance='Developpement du projet'),
        Tache(nom='C', duree=Duree(heures=2, minutes=23), prerequis=
        [Prerequis(nom='B', typ='debut', latence=Duree(jours=2, heures=3))], correspondance="Envoyer la requête à l'agence"),
        Tache(nom='D', duree=Duree(annees=3), prerequis=[Prerequis(nom='A', typ='fin', latence=Duree(Aucune durée)), Prerequis(nom='C', typ='fin', latence =Duree(mois=10))], correspondance='Developpement de la plateforme publique'),
        Tache(nom='E', duree=Duree(secondes=1), prerequis=[Prerequis(nom='D', typ='fin', latence=Duree(Aucune durée))], correspondance='Ouverture du projet')])

        >>> mon_probleme_bis = Probleme.par_str('''
    ... A / 3 ans + 2 semaines / / Decryptage du probleme
    ... B / 2 semaine + 4 jours / A fin (2 jours + 3 heures) / Developpement du projet
    ... C / 2 heures + 23 minutes / B debut (2 jours + 3 heures) / Envoyer la requête à l'agence
    ... D / 3 ans / A fin | C fin (10 mois) / Developpement de la plateforme publique
    ... E / 1 seconde / D fin / Ouverture du projet
    ... ''')

        >>> mon_probleme == mon_probleme_bis
    True

        >>> print(list(mon_probleme.noms))
    ['A', 'B', 'C', 'D', 'E']

        >>> print(list(mon_probleme.correspondances))
    ['Decryptage du probleme', 'Developpement du projet', "Envoyer la requête à l'agence", '
    Developpement de la plateforme publique', 'Ouverture du projet']

        >>> print(list(mon_probleme.taches))
    [Tache(nom='A', duree=Duree(annees=3, semaines=2), prerequis=[], correspondance='Decryptage du probleme'), Tache(nom='B', duree=Duree(semaines=2, jours=4), prerequis=[Prerequis (nom='A', typ='fin', latence=Duree(jours=2, heures=3))], correspondance='Developpement du projet'), Tache(nom='C', duree=Duree(heures=2, minutes=23), prerequis=[Prerequis(nom='B', typ='debut', latence=Duree(jours=2, heures=3))], correspondance="Envoyer la requête à l'agence"), Tache(nom='D', duree=Duree(annees=3), prerequis=[Prerequis(nom='A', typ='fin', latence=Duree(Aucune durée)), Prerequis(nom='C', typ='fin', latence=Duree(mois=10))], correspondance='Developpement de la plateforme publique'), Tache(nom='E', duree=Duree(secondes=1), prerequis=[Prerequis(nom='D', typ='fin', latence=Duree(Aucune durée))], correspondance='Ouverture du projet')]

        >>> print(mon_probleme)
    Tache(nom='A', duree=Duree(annees=3, semaines=2), prerequis=[], correspondance='Decryptage du probleme')
    Tache(nom='B', duree=Duree(semaines=2, jours=4), prerequis=[Prerequis(nom='A', typ='fin', latence=Duree(jours=2, heures=3))], correspondance='Developpement du p
    rojet')
    Tache(nom='C', duree=Duree(heures=2, minutes=23), prerequis=[Prerequis(nom='B',typ='debut', latence=Duree(jours=2, heures=3))], correspondance="Envoyer la requ
    ête à l'agence")
    Tache(nom='D', duree=Duree(annees=3), prerequis=[Prerequis(nom='A', typ='fin', latence=Duree(Aucune durée)), Prerequis(nom='C', typ='fin', latence=Duree(mois=10))], correspondance='Developpement de la plateforme publique')
    Tache(nom='E', duree=Duree(secondes=1), prerequis=[Prerequis(nom='D', typ='fin',latence=Duree(Aucune durée))], correspondance='Ouverture du projet')

        >>> mon_probleme["A"]
    Tache(nom='A', duree=Duree(annees=3, semaines=2), prerequis=[], correspondance='Decryptage du
    probleme')

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

    >>> mon_probleme.affiche_correspondance()
                      Correspondances
    ┌─────────────────────────────────────────┬───────┐
    │ Nature                                  │ Tâche │
    ├─────────────────────────────────────────┼───────┤
    │ Decryptage du probleme                  │ A     │
    │ Developpement du projet                 │ B     │
    │ Envoyer la requête à l'agence           │ C     │
    │ Developpement de la plateforme publique │ D     │
    │ Ouverture du projet                     │ E     │
    └─────────────────────────────────────────┴───────┘
    """

    def __init__(self, taches: List[Tache]):
        """Stocke la liste des tâches sous forme de dictionnaire."""
        self._taches: Dict[Nom, Tache] = dict()
        self._correspondances: Dict[Nom, Correspondance] = dict()
        for tache in taches:
            if tache.nom in self._taches:
                raise ValueError(
                    f"Le nom de tâche {tache.nom} est présent plusieurs fois."
                )
            self._taches[tache.nom] = tache
            if tache.correspondance in self._correspondances.keys():
                raise ValueError(
                    f"La correspondance {tache.correspondances} est utilisée plusieurs fois."
                )
            self._correspondances[tache.nom] = tache.correspondance
        self._est_valide()

    @staticmethod
    def _encode(ligne) -> Tache:
        """Encode une ligne en tâche."""
        prerequis_valide = list()
        nom, duree, prerequis, correspondance = ligne.split("/")
        nom_valide = nom.strip()
        correspondance_valide = correspondance.strip()
        if duree.strip():
            duree_valide = Duree.par_str(duree)
        else:
            raise ValueError("Vous devez renseigner une durée de tâche.")
        if prerequis.strip():
            for prerequi in prerequis.split("|"):
                prerequis_valide.append(Prerequis.par_str(prerequi))
        return Tache(
            nom=nom_valide,
            duree=duree_valide,
            prerequis=prerequis_valide,
            correspondance=correspondance_valide,
        )

    @classmethod
    def par_str(cls, message: str) -> "Probleme":
        """Constructeur alternatif pour un problème."""
        taches = list()
        for ligne in message.strip().splitlines():
            taches.append(cls._encode(ligne))

        return cls(taches)

    @property
    def taches(self) -> Generator[Tache, None, None]:
        """Itére sur les tâches."""
        yield from self._taches.values()

    @property
    def noms(self) -> Generator[Nom, None, None]:
        """Itére sur les noms des tâches."""
        yield from self._taches.keys()

    @property
    def correspondances(self) -> Generator[Correspondance, None, None]:
        """Itére sur les correspondances des tâches"""
        yield from self._correspondances.values()

    def _est_valide(self):
        """Vérifie que toutes les tâches dans les prérequis existent.
        Vérifie si le type de prérequis est fin ou début."""
        for tache in self.taches:
            for prerequis in tache.prerequis:
                if prerequis.nom not in self._taches:
                    raise ValueError(f"{prerequis.nom} n'est pas une tâche existante.")
                if prerequis.typ != "fin" and prerequis.typ != "debut":
                    raise ValueError(
                        f'{prerequis.typ} n\'indique pas le type de prérequis.\nVeuillez indiquer si le prérequis est de type  "fin" ou "debut".'
                    )

    def __eq__(self, autre: Any) -> bool:
        """Egalite."""
        if type(autre) != type(self):
            return False
        return self._taches == autre._taches

    def __repr__(self) -> str:
        """Renvoie la liste de construction."""
        return f"Probleme(taches={list(self.taches) !r})"

    def __str__(self) -> str:
        """Affiche les tâches par ligne."""
        return "\n".join(repr(tache) for tache in self.taches)

    def __getitem__(self, nom: Nom) -> Tache:
        """Accès aux tâches par leurs noms."""
        return self._taches[nom]

    def _genere_table_probleme(self, entier: bool, brute: bool) -> Table:
        """Renvoie une table rich."""
        if entier:
            resultat = Table(title="Problème d'ordonnancement")
            resultat.add_column("Tâche")
            resultat.add_column("Nature")
            resultat.add_column("Durée")
            resultat.add_column("Prérequis")
            for tache in self.taches:
                resultat.add_row(
                    tache.nom,
                    tache.correspondance,
                    tache.duree._choisi_brute(brute),
                    tache._messages_(brute),
                )

        else:
            resultat = Table(title="Problème d'ordonnancement")
            resultat.add_column("Tâche")
            resultat.add_column("Durée")
            resultat.add_column("Prérequis")
            for tache in self.taches:
                resultat.add_row(
                    tache.nom, tache.duree._choisi_brute(brute), tache._messages_(brute)
                )

        return resultat

    def affiche_probleme(
        self, entier: Optional[bool] = False, brute: Optional[bool] = False
    ):
        """Affiche le probleme en tableau.

        [optionnel] entier est un argument donnant la table avec ou sans les correspondances.

        [optionnel] brute est un argument qui re-travaille ou non les durées.

        """
        if type(entier) != bool:
            raise ValueError(f"L'argument de entier '{entier}' doit être True ou False")
        if type(brute) != bool:
            raise ValueError(f"L'argument de entier '{entier}' doit être True ou False")
        from rich import print

        print(self._genere_table_probleme(entier, brute))

    def get_correspondance(self) -> Dict:
        """Renvoie un dict des correspondances"""
        return self._correspondances

    def _genere_table_correspondance(self) -> Table:
        dictionnaire = self.get_correspondance()
        clefs = dictionnaire.keys()
        resultat = Table(title="Correspondances")
        resultat.add_column("Nature")
        resultat.add_column("Tâche")
        for nom_reel in clefs:
            resultat.add_row(dictionnaire[nom_reel], nom_reel)
        return resultat

    def affiche_correspondance(self):
        """Affiche les correspondances en tableau."""
        from rich import print

        print(self._genere_table_correspondance())
