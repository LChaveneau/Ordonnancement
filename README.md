# Présentation de la librairie ordonnancement 

## Objectif

L'objectif est de résoudre un quelconque problème d'ordonnancement à prérequis composé.
Un prérequis doit-être composé de : 
- Une tâche à attendre : c'est à dire que nous devons attendre l'éxécution de cette tâche avant de pouvoir commencer une certaine tâche.
- Un type d'attente : fin ou debut. Nous devons attendre qu'une certaine tâche commence, ou termine avant de commencer une autre tâche. 
- Une latence : c'est à dire que la tâche ne pourra commencer qu'aprés une durée établie aprés le commencement ou la fin d'une autre tâche.

Une tâche a une durée d'éxécution et peut avoir une correspondance/nature et peut avoir un ou des prérequis.

En effet, il est essentiel pour l'algorithme d'ajouter un nom de tâche non composé. C'est ainsi à quoi sert la correspondance d'une tâche. Il permet de faire un lien avec la vrai nature de la tâche.

## Explication des classes/objets.

L'explication compléte de ces classes sera développé dans le **notebook** `presentation_utilisateur`.

### L'objet Duree

L'objet duree gère toutes les durées présentes dans cette librairie. Comme la latence d'un prérequis ou la durée d'une tâche. 

Une durée peut-être composée:
- D'aucune durée 
- de secondes
- de minutes
- d'heures
- de jours
- de semaines
- de mois
- d'années

Cette objet est supervisée par l'objet **duration** de **Pendulum**.

### L'objet Prérequis 

Elle représente un prérequis.
Un prérequis est composé :
 - d'un nom : une tâche à laquelle une certaine tâche doit attendre.
 - d'un type : si on doit attendre la fin ou le début de cette tâche.
- d'une latence : combien doit-t'on attendre aprés la fin ou le début d'éxécution d'une certaine tâche.

### L'objet Tache

Cette objet à pour but de représenter une tâche.
Cette objet est composé :
- d'un nom de tâche.
- d'une durée d'éxécution.
- d'une liste de prérequis. En effet une tâche peut avoir plusieurs prérequis.

### L'objet Probleme
Elle représente notre problème d'ordonnancement. 
C'est une liste d'objet Tache. C'est sur quoi notre algorithme résoudra.

### L'objet Date

Elle sera créé automatiquement si nous résolvons notre problème d'ordonnancement en date.

Elle représente une date qui peut être composée seulement d'une date mais aussi qui peut être composée d'une heure (avec les secondes).

Elle est supervisée par l'objet **datetime** de **Pendulum**.

### L'objet Activite

Cet objet est créé aprés l'algorithme de résolution en Durée.

L'objet Activite représente l'activité d'éxécution d'une tâche. C'est à dire la particularité d'une tâche (l'objet **Tache**), mais aussi une durée de début et une durée de fin.

### L'objet EDT

C'est l'objet final de l'algorithme de résolution en durée.
Elle représente l'emploi du temps optimal d'un problème d'ordonnancement.
Elle est composé d'objets **Activite**

### L'objet Datation
Cet objet est créé depuis l'algorithme de résolution en Date.
Elle date une tâche d'aprés l'algorithme de résolution.
Elle est sensiblement identique à l'objet Activités, à la différence que ce ne sont pas des durées, mais des dates. Elle est donc composée :
- D'un objet **Tache**
- D'une date de début
- D'une date de fin

### L'objet Calendrier

C'est l'objet final de l'algorithme de résolution en date. 
Elle représente un calendrier/agenda optimal d'un problème d'ordonnancement.
Elle est composé d'objet **Datation**

## Explication des modules

### Module probleme

Ce module comprend les propriétés des objets :

- Duree
- Prerequis 
- Tache
- Probleme

Ce module sert à la construction de notre problème d'ordonnancement. Il régit toutes les erreurs associés aux mauvaises constructions de nos objets.
Il régit toutes les constructions de nos classes. 
Il permet aussi de représenter correctement notre problème d'ordonnancement sous forme de tableau.

### Module algorithme

Ce module comprend l'algorithme de résolution pour un problème d'ordonnancement.
Pour l'ordre des tâches a effectuer, nous utilisons **NetworkX**.

Nous avons deux algorithmes de résolution:
- L'un qui détermine un emploi de temps optimal. Il travail avec des durées et en ressort des durées optimales. Précisemment, il ressort un objet **EDT**. 

- L'autre qui determine un agenda optimal. Il travail avec des dates et en ressort des dates optimales. Précisemment, il ressort un objet **Calendrier**. 

Nous pouvons rajouter des conditions pour la résolution du problème d'ordonancement :

- Pour l'algorithme type emploi du temps:
    - Rajouter une durée maximum d'éxécution journalière.
    - Rajouter un nombre de jours de repos hebdomadaire.
- Pour l'algorithme type calendrier:
    - Définir une plage horaire d'éxécution de tâche.
    - Définir des jours de repos hebdomadaire.


Nos fonctions :
- determine sur quels prérequis commencer.
- determine une durée/date de début et de fin.
- calcule les nouvelles durées et dates si des conditions sont renseignées. 

### Module edt
Le module edt régit les classes suivantes :
- Activite
- EDT

Elle gère toutes les erreurs relatives aux mauvaises constructions de ces objets.
Elle permet aussi de faire un bel affichage de l'emploi optimal du problème d'ordonnancement.

### Module calendrier
Ce module régit les classes suivantes :
- Date
- Datation
- Calendrier

Elle permet aussi de faire un bel affichage du calendrier optimal.

## Points à améliorer et faiblesses

Lorsque nous rajoutons une durée quotidienne d'éxécution de tâche ou lorsque nous rajoutons des jours hebdomadaire de repos, nous perdons en précisions. Il serait important d'étailler ce problème.

Il serait aussi pertinent de rajouter plusieurs durées quotidiennes d'éxécution de tâche.

Nous pourrions aussi rajouter, à l'algorithme de résolution, des dates pour lesquelles l'éxécution de tâche est impossible. Je pense entre autre aux jours fériées. 

Un developpement complet des objet Duree et Date pour pouvoir fournir un spectre plus large d'utilisation de ces classes. 

Je n'ai notamment pas réussi à itérer sur les instances des objets Date et Duree. 

Un code plus clair et plus efficaces. En effet, je trouve que mon code est un peu trop primitif et pas assez explicite. 

Développement d'un app.py

Développement d'une représentation visuelle d'un emploi du temps ou d'un calendrier