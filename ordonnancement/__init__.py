#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Cette librairie sert à la résolution de probleme d'ordonnancement à prérequis composé.
Une tâche peut avoir des prérequis avant d'être commencé.
Ces prérequis sont composé par :
    - Le nom de la tâche auquel le prérequis fait référence.
    - Le type de prérequis : fin ou debut. C'est à dire attendre la fin ou le début d'une tâche.
    - La latence : si il y a un décalage de commencement d'une tâche aprés la fin ou le début d'une autre.
Par exemple : la tache A peut commencer quand B a terminé plus 4 jours.

Les durées des tâches ou la latence d'une prérequis sont assurées par l'objet Durée.
L'objet Durée représente une durée composée de :
    - années 
    - mois 
    - semaines
    - jours
    - heures
    - minutes
    - secondes
    
L'objet Durée est supervisé par le module Duration de Pendulum.

L'algorithme de résolution nous donne deux sorties :

1) La sortie est de type durée.
    L'algorithme sortira un emploi du temps optimal composée de durée de debut et de durée de fin de tâche.
    Nous pouvons rajouter plusieurs paramètres à cet algorithme de résolution :
        - Rajouter un temps journalier d'éxécution de tâches. C'est à dire que l'éxécution des tâches ne se fera que pendant X temps par jours.
        Ce temps est une heure avec possibilité de rajouter des minutes convertit en heures. Exemple 13.50 = 13heures et 30minutes
        - Rajouter un nombre de jours hebdomadaire de repos. L'avancement des tâches ne se fera pas pendant X jours par semaines.

2) La sortie est de type date.
    L'algorithme sortira un calendrier optimal composée d'une date de début et une date de fin.
    Nous pouvons rajouter sensiblement les mêmes paramètres qu'à la précédente type de sortie :
        - Définir une plage horaire d'éxécution de tâche. L'éxécution de tâche ne se fera que dans cette plage horaire.
        - Définir des jours de repos. L'éxécution de tâche ne se fera pas sur ces jours prédéfinis.

Une date est gérée par l'objet Date.
L'objet Date est un objet représentant une date mais peu également représenter une date et une heure avec les secondes.
L'objet Date est supervisée par l'objet datetime de Pendulum.

Exemple :

    >>> mon_probleme=Probleme(
        taches=[
            Tache(
                nom='A', 
                duree=Duree(annees=3, semaines=2), 
                prerequis=[], correspondance='Decryptage du probleme'), 
            Tache(
                nom='B', 
                duree=Duree(semaines=2, jours=4), 
                prerequis=[
                    Prerequis(nom='A', typ='fin', latence=Duree(jours=2, heures=3))
                    ], 
                correspondance='Developpement du projet'), 
            Tache(
                nom='C', 
                duree=Duree(heures=2, minutes=23), 
                prerequis=[
                    Prerequis(nom='B', typ='debut', latence=Duree(jours=2, heures=3))
                    ], 
                correspondance="Envoyer la requête à l'agence"), 
            Tache(
                nom='D', 
                duree=Duree(annees=3), 
                prerequis=[
                    Prerequis(nom='A', typ='fin', latence=Duree()), 
                    Prerequis(nom='C', typ='fin', latence=Duree(mois=10))
                    ], 
                correspondance='Developpement de la plateforme publique'), 
            Tache(
                nom='E', 
                duree=Duree(secondes=1), 
                prerequis=[
                    Prerequis(nom='D', typ='fin', latence=Duree())
                    ], 
                correspondance='Ouverture du projet')
            ]
        )

    >>> mon_probleme.affiche_probleme(entier=True)
                           Problème d'ordonnancement
┌───────┬───────────────────────┬─────────────────────┬───────────────────────┐
│ Tâche │ Nature                │ Durée               │ Prérequis             │
├───────┼───────────────────────┼─────────────────────┼───────────────────────┤
│ A     │ Decryptage du         │ 3 ans 2 semaines    │                       │
│       │ probleme              │                     │                       │
│ B     │ Developpement du      │ 2 semaines 4 jours  │ fin de A + 2 jours 3  │
│       │ projet                │                     │ heures                │
│ C     │ Envoyer la requête à  │ 2 heures 23 minutes │ debut de B + 2 jours  │
│       │ l'agence              │                     │ 3 heures              │
│ D     │ Developpement de la   │ 3 ans               │ fin de A et fin de C  │
│       │ plateforme publique   │                     │ + 10 mois             │
│ E     │ Ouverture du projet   │ 1 seconde           │ fin de D              │
└───────┴───────────────────────┴─────────────────────┴───────────────────────┘

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

>>> resolution_sans_condition_EDT=resous_EDT(mon_probleme)
>>> resolution_sans_condition_EDT.affiche()

                    Solution du problème : emploi du temps
┌───────┬──────────────────────────────────┬──────────────────────────────────┐
│ Tâche │ Début                            │ Fin                              │
├───────┼──────────────────────────────────┼──────────────────────────────────┤
│ A     │ Débute au temps 0                │ 3 ans 2 semaines                 │
│ B     │ 3 ans 2 semaines 2 jours 3       │ 3 ans 4 semaines 6 jours 3       │
│       │ heures                           │ heures                           │
│ C     │ 3 ans 2 semaines 4 jours 6       │ 3 ans 2 semaines 4 jours 8       │
│       │ heures                           │ heures 23 minutes                │
│ D     │ 3 ans 10 mois 2 semaines 4 jours │ 6 ans 10 mois 2 semaines 4 jours │
│       │ 8 heures 23 minutes              │ 8 heures 23 minutes              │
│ E     │ 6 ans 10 mois 2 semaines 4 jours │ 6 ans 10 mois 2 semaines 4 jours │
│       │ 8 heures 23 minutes              │ 8 heures 23 minutes 1 seconde    │
└───────┴──────────────────────────────────┴──────────────────────────────────┘

>>> resolution_avec_condition_EDT=resous_EDT(mon_probleme,duree_max_journalier=12,nb_jours_repos=3)
>>> resolution_avec_condition_EDT.affiche()

                    Solution du problème : emploi du temps
┌───────┬──────────────────────────────────┬──────────────────────────────────┐
│ Tâche │ Début                            │ Fin                              │
├───────┼──────────────────────────────────┼──────────────────────────────────┤
│ A     │ Débute au temps 0                │ 10 ans 7 mois 3 semaines 2 jours │
│ B     │ 10 ans 7 mois 3 semaines 4 jours │ 10 ans 9 mois 3 semaines 4 jours │
│       │ 3 heures                         │ 3 heures                         │
│ C     │ 10 ans 7 mois 3 semaines 6 jours │ 10 ans 7 mois 3 semaines 6 jours │
│       │ 6 heures                         │ 20 heures 18 minutes             │
│ D     │ 10 ans 17 mois 3 semaines 6      │ 20 ans 22 mois 8 semaines 1 jour │
│       │ jours 20 heures 18 minutes       │ 20 heures 18 minutes             │
│ E     │ 20 ans 22 mois 8 semaines 1 jour │ 20 ans 22 mois 8 semaines 1 jour │
│       │ 20 heures 18 minutes             │ 20 heures 18 minutes 1 seconde   │
└───────┴──────────────────────────────────┴──────────────────────────────────┘

>>> resolution_sans_condition_Calendrier=resous_Calendrier(mon_probleme, date_commencement="23/12/1998")
>>> resolution_sans_condition_Calendrier.affiche()

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

>>> resolution_avec_condition_Calendrier=resous_Calendrier(mon_probleme, date_commencement="23/12/1998", jours_repos="Lundi Mardi",heures_execution="10-23")
>>> resolution_avec_condition_Calendrier.affiche()

               Solution du problème : calendrier
┌───────┬──────────────────────────┬──────────────────────────┐
│ Tâche │ Début                    │ Fin                      │
├───────┼──────────────────────────┼──────────────────────────┤
│ A     │ 23 décembre 1998 à 10h00 │ 25 octobre 2006 à 18h28  │
│ B     │ 27 octobre 2006 à 21h28  │ 15 décembre 2006 à 10h00 │
│ C     │ 1 novembre 2006 à 10h00  │ 1 novembre 2006 à 14h02  │
│ D     │ 1 septembre 2007 à 14h02 │ 27 mai 2015 à 15h52      │
│ E     │ 27 mai 2015 à 15h52      │ 27 mai 2015 à 15h52      │
└───────┴──────────────────────────┴──────────────────────────┘
>>>

Remarque:
On pourra faire python -m ordonnancement pour un exemple.
"""
from .probleme import Tache, Probleme, Prerequis, Duree
from .edt import Activite, EDT
from .algorithme import resous_EDT, resous_Calendrier, genere_graphe
from .calendrier import Date, Calendrier, Datation

__all__ = [
    "Activite",
    "EDT",
    "Tache",
    "Probleme",
    "resous_EDT",
    "resous_Calendrier",
    "genere_graphe",
    "Prerequis",
    "Date",
    "Calendrier",
    "Duree",
    "Datation",
]
