#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Description

Tests sur le module Calendrier
"""

import pytest
from ordonnancement import Probleme, Tache, Prerequis, Datation, Date, Calendrier, Duree
from pendulum import datetime
import ordonnancement as algo

### Test sur la classe Date


@pytest.fixture
def date():
    return Date.par_str("""23/12/1998/23:19""")


@pytest.fixture
def duree():
    return Duree.par_str("""3 jours + 23 secondes""")


def test_est_date():
    """Teste si l'objet est de type Date"""
    return isinstance(date, Date)


def test_non_identité(date):
    """Pour ne pas tester l'identité"""
    entree = date
    attendu = Date(jours=23, mois=12, annees=1998, heures=23, minutes=19)
    assert entree == attendu


def test_annees_out_of_range():
    """Teste si les valeurs de l'annee sont non correctes lors de la création d'un objet Date"""
    with pytest.raises(ValueError):
        Date(jours=1, mois=1, annees=0)
    with pytest.raises(ValueError):
        Date(jours=1, mois=1, annees=100000000)
    with pytest.raises(ValueError):
        Date(jours=1, mois=1, annees=-1)


def test_mois_out_of_range():
    """Teste si les valeurs du mois sont non correctes lors de la création d'un objet Date"""
    with pytest.raises(ValueError):
        Date(jours=1, mois=0, annees=1998)
    with pytest.raises(ValueError):
        Date(jours=1, mois=-1, annees=1998)
    with pytest.raises(ValueError):
        Date(jours=1, mois=13, annees=-1998)


def test_jours_out_of_range():
    """Teste si les valeurs du jour sont non correctes lors de la création d'un objet Date"""
    with pytest.raises(ValueError):
        Date(jours=0, mois=1, annees=1998)
    with pytest.raises(ValueError):
        Date(jours=-1, mois=1, annees=1998)
    with pytest.raises(ValueError):
        Date(jours=32, mois=1, annees=-1998)


def test_minutes_out_of_range():
    """Teste si les valeurs des minutes sont non correctes lors de la création d'un objet Date"""
    with pytest.raises(ValueError):
        Date(jours=1, mois=1, annees=1998, minutes=-1)
    with pytest.raises(ValueError):
        Date(jours=1, mois=1, annees=1998, minutes=60)
    with pytest.raises(ValueError):
        Date(jours=1, mois=1, annees=1998, minutes=61)


def test_heures_out_of_range():
    """Teste si les valeurs de l'heure sont non correctes lors de la création d'un objet Date"""
    with pytest.raises(ValueError):
        Date(jours=1, mois=1, annees=1998, heures=-1)
    with pytest.raises(ValueError):
        Date(jours=1, mois=1, annees=1998, heures=24)
    with pytest.raises(ValueError):
        Date(jours=1, mois=1, annees=1998, heures=25)


def test_secondes_out_of_range():
    """Teste si les valeurs des secondes sont non correctes lors de la création d'un objet Date"""
    with pytest.raises(ValueError):
        Date(jours=1, mois=1, annees=1998, secondes=-1)
    with pytest.raises(ValueError):
        Date(jours=1, mois=1, annees=1998, secondes=60)
    with pytest.raises(ValueError):
        Date(jours=1, mois=1, annees=1998, secondes=61)


def test_erreur_complexes():
    """Teste les erreurs plus complexes comme un mois ne comportant que 30 jours"""
    ## Annee bissextile
    assert Date(jours=29, mois=2, annees=2000)
    ## Annee non bissextile
    with pytest.raises(ValueError):
        Date(jours=29, mois=2, annees=2001)
    ##Mois avec 30 jours
    with pytest.raises(ValueError):
        Date(jours=31, mois=6, annees=1998)


def test_convertit_datetime(date):
    """Teste la convertion d'un objet Date à un objet datetime"""
    entree = date
    attendu = datetime(day=23, month=12, year=1998, hour=23, minute=19)
    assert entree._convertit_datetime() == attendu


def test_convertit_date(date):
    """Teste la convertion d'un objet datetime à un objet Date"""
    entree = datetime(day=23, month=12, year=1998, hour=23, minute=19)
    attendu = date
    assert algo.calendrier.Date._convertit_date(entree) == attendu


def test_add(date, duree):
    """Teste l'ajout d'une durée à une date"""
    entree = date
    attendu = Date(jours=26, mois=12, annees=1998, heures=23, minutes=19, secondes=23)
    assert entree.add(duree) == attendu


def test_temps(date):
    """Teste le retour de l'objet temps"""
    entree = date.temps()
    attendu = {"jours": 23, "mois": 12, "annees": 1998}
    assert entree == attendu


def test_temps_total(date):
    """Teste le retour de l'objet temps_total"""
    entree = date.temps_total()
    attendu = {
        "jours": 23,
        "mois": 12,
        "annees": 1998,
        "heures": 23,
        "minutes": 19,
        "secondes": 0,
    }
    assert entree == attendu


def test_heure(date):
    """Teste le retour dde l'objet heure"""
    entree = date.heure()
    attendu = {"heures": 23, "minutes": 19, "secondes": 0}
    assert entree == attendu


def test_egalite_inegalite(date, duree):
    """Teste l'egalité et la non égalité"""
    entree = date
    date_egale = Date(jours=23, mois=12, annees=1998, heures=23, minutes=19)
    date_non_egale = Date(jours=25, mois=10, annees=2000, heures=23, minutes=19)
    assert entree == date_egale
    assert not entree != date_egale
    assert entree != date_non_egale
    assert not entree == date_non_egale
    with pytest.raises(ValueError):
        entree == duree
        entree != duree


def test_superiorite_inferiorite(date, duree):
    """Teste la supériorité et l'infériorité entre deux dates"""
    entree = date
    date_egale = Date(jours=23, mois=12, annees=1998, heures=23, minutes=19)
    date_inferieur = Date(jours=10, mois=2, annees=1990, heures=1, minutes=19)
    date_superieur = Date(jours=8, mois=4, annees=2021, heures=13, minutes=52)
    assert date >= date_egale
    assert date <= date_egale
    assert not date > date_egale
    assert not date < date_egale
    assert date > date_inferieur
    assert date >= date_inferieur
    assert not date < date_inferieur
    assert not date <= date_inferieur
    assert not date > date_superieur
    assert not date >= date_superieur
    assert date < date_superieur
    assert date <= date_superieur
    ###erreur si comparé à un objet qui n'est pas de type Date
    with pytest.raises(ValueError):
        entree >= duree
        entree > duree
        entree < duree
        entreew <= duree


def test_addition(date, duree):
    """Teste l'addition entre un objet Date et un objet Duree"""
    entree = date
    attendu = Date(jours=26, mois=12, annees=1998, heures=23, minutes=19, secondes=23)
    assert entree + duree == attendu


def test_soustraction(date, duree):
    """Teste la soustraction entre un objet Date et un objet Duree"""
    entree = date
    attendu = Date(jours=20, mois=12, annees=1998, heures=23, minutes=18, secondes=37)
    assert entree - duree == attendu


def test_repr():
    """Teste la représentation"""
    entree = date
    attendu = "Date(jours=23, mois=12, annees=1998, heures=23, minutes=19, secondes=0)"
    assert repr(entree) == attendu


def test_get_item(date):
    """Teste le __get_item__"""
    entree = date
    assert entree["secondes"] == 0
    assert entree["heures"] == 23
    assert entree["minutes"] == 19
    assert entree["jours"] == 23
    assert entree["mois"] == 12
    assert entree["annees"] == 1998


def test_par_str():
    """Teste le constucteur alternatif"""
    date1 = Date.par_str("""23/12/1998/23:19""")
    date2 = Date.par_str("""23/12/1998""")
    date3 = Date.par_str("""23/12/1998/23:19:01""")
    assert date1 == Date(
        jours=23, mois=12, annees=1998, heures=23, minutes=19, secondes=0
    )
    assert date2 == Date(
        jours=23, mois=12, annees=1998, heures=0, minutes=0, secondes=0
    )
    assert date3 == Date(
        jours=23, mois=12, annees=1998, heures=23, minutes=19, secondes=1
    )


### Test sur la classe datation


def test_debut_fin_valide():
    a = Tache(nom="A", duree=Duree(jours=2), prerequis=[])
    with pytest.raises(ValueError):
        Datation(
            tache=a,
            date_debut=Date(jours=23, mois=12, annees=1998),
            date_fin=Date(jours=24, mois=12, annees=1998),
        )
    with pytest.raises(ValueError):
        Datation(
            tache=a,
            date_debut=Date(jours=25, mois=12, annees=1998),
            date_fin=Date(jours=24, mois=12, annees=1998),
        )


### Test sur la classe calendrier


@pytest.fixture
def taches():
    """Crée 4 taches."""
    probleme = Probleme.par_str(
        """
A / 1 jours / / A
B / 2 jours/ A fin (2 jours)/ B
C / 3 jours/ A debut (2 jours + 1 semaines) | B fin (1 jour)/ C
D / 4 jours/ A fin/ D
"""
    )
    return list(probleme.taches)


@pytest.fixture
def datations():
    probleme = Probleme.par_str(
        """
A / 1 jours / / A
B / 2 jours/ A fin (2 jours)/ B
C / 3 jours/ A debut (2 jours + 1 semaines) | B fin (1 jour)/ C
D / 4 jours/ A fin/ D
"""
    )
    a, b, c, d = probleme.taches
    return [
        Datation(
            tache=a,
            date_debut=Date(jours=23, mois=12, annees=1998),
            date_fin=Date(jours=24, mois=12, annees=1998),
        ),
        Datation(
            tache=b,
            date_debut=Date(jours=24, mois=12, annees=1998),
            date_fin=Date(jours=26, mois=12, annees=1998),
        ),
        Datation(
            tache=c,
            date_debut=Date(jours=27, mois=12, annees=1998),
            date_fin=Date(jours=30, mois=12, annees=1998),
        ),
        Datation(
            tache=d,
            date_debut=Date(jours=24, mois=12, annees=1998),
            date_fin=Date(jours=28, mois=12, annees=1998),
        ),
    ]


def test_instanciation(datations):
    """Création."""
    calendrier = Calendrier(dates=datations)
    assert isinstance(calendrier, Calendrier)


def test_repr():
    """Pour débogguer."""
    calendrier = Calendrier(
        dates=[
            Datation(
                tache=Tache(nom="A", duree=Duree(jours=2), prerequis=[]),
                date_debut=Date(jours=24, mois=12, annees=1998),
                date_fin=Date(jours=26, mois=12, annees=1998),
            )
        ]
    )
    assert (
        repr(calendrier)
        == "Calendrier(dates=[Datation(tache=Tache(nom='A', duree=Duree(jours=2), prerequis=[], correspondance=' '), date_debut=Date(jours=24, mois=12, annees=1998), date_fin=Date(jours=26, mois=12, annees=1998))])"
    )


def test_egalite(datations):
    """Et pas l'identité."""
    assert Calendrier(datations) == Calendrier(datations)


def test_datations(datations):
    """Test de la propriété."""
    calendrier = Calendrier(datations)
    assert "datations" not in vars(calendrier)
    assert datations == list(calendrier.dates)


def test_acces(datations):
    """Test de []."""
    calendrier = Calendrier(datations)
    assert calendrier["A"] == datations[0]


def test_ajoute():
    """Mutation du calendrier."""
    calendrier = Calendrier(dates=[])
    assert calendrier._dates == []
    tache = Datation(
        tache=Tache(nom="A", duree=Duree(jours=1), prerequis=[]),
        date_debut=Date(jours=24, mois=12, annees=1998),
        date_fin=Date(jours=25, mois=12, annees=1998),
    )
    calendrier.ajoute(tache)
    assert calendrier._dates == [tache]


def test_verification_duree_datations():
    """Au moment de l'ajout."""
    calendrier = Calendrier(dates=[])
    with pytest.raises(ValueError):
        calendrier.ajoute(
            Datation(
                tache=Tache(nom="A", duree=Duree(jours=2), prerequis=[]),
                date_debut=Date(jours=23, mois=12, annees=1998),
                date_fin=Date(jours=24, mois=12, annees=1998),
            )
        )


def test_verification_doublon(datations):
    """Au moment de l'ajout."""
    calendrier = Calendrier(dates=datations)
    with pytest.raises(ValueError):
        calendrier.ajoute(
            Datation(
                tache=Tache(nom="A", duree=Duree(jours=2), prerequis=[]),
                date_debut=Date(jours=24, mois=12, annees=1998),
                date_fin=Date(jours=24, mois=12, annees=1998),
            )
        )


def test_valide(datations):
    """Cas ok."""
    calendrier = Calendrier(datations)
    assert calendrier.est_valide()


def test_invalide(datations):
    """Cas pas ok."""
    a, b, c, d = datations
    d.date_debut = Date(jours=23, mois=12, annees=1998)
    calendrier = Calendrier(dates=[a, b, c, d])
    assert not calendrier.est_valide()
