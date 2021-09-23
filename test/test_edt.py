#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description

Tests sur le module edt.
"""
import pytest
from ordonnancement import Probleme, Tache, Prerequis, Activite, EDT, Duree

## Test sur la classe Activite


def test_post_init():
    """Vérifie que la duree de fin est supérieur à la durée de debut."""
    with pytest.raises(ValueError):
        Activite(
            Tache(nom="A", duree=Duree(jours=34), prerequis=[], correspondance="Rien"),
            debut=Duree(secondes=23),
            fin=Duree(secondes=22),
        )


## Test sur la classe EDT


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
def activites():
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
        Activite(tache=a, debut=Duree(), fin=Duree(jours=1)),
        Activite(tache=b, debut=Duree(jours=1), fin=Duree(jours=3)),
        Activite(tache=c, debut=Duree(jours=4), fin=Duree(jours=7)),
        Activite(tache=d, debut=Duree(jours=1), fin=Duree(jours=5)),
    ]


def test_verification_activite():
    """Compatibilité."""
    a = Tache(nom="A", duree=Duree(jours=2), prerequis=[])
    with pytest.raises(ValueError):
        Activite(tache=a, debut=Duree(), fin=Duree(jours=1))


def test_instanciation(activites):
    """Création."""
    edt = EDT(activites=activites)
    assert isinstance(edt, EDT)


def test_repr():
    """Pour débogguer."""
    edt = EDT(
        activites=[
            Activite(
                tache=Tache(nom="A", duree=Duree(jours=2), prerequis=[]),
                debut=Duree(),
                fin=Duree(jours=2),
            )
        ]
    )
    assert (
        repr(edt)
        == "EDT(activites=[Activite(tache=Tache(nom='A', duree=Duree(jours=2), prerequis=[], correspondance=' '), debut=Duree(Aucune durée), fin=Duree(jours=2))])"
    )


def test_egalite(activites):
    """Et pas l'identité."""
    assert EDT(activites) == EDT(activites)


def test_activites(activites):
    """Test de la propriété."""
    edt = EDT(activites)
    assert "activites" not in vars(edt)
    assert activites == list(edt.activites)


def test_acces(activites):
    """Test de get item."""
    edt = EDT(activites)
    assert edt["A"] == activites[0]


def test_ajoute():
    """Mutation de l'EDT."""
    edt = EDT(activites=[])
    assert edt._activites == []
    tache = Activite(
        tache=Tache(nom="A", duree=Duree(jours=1), prerequis=[]),
        debut=Duree(),
        fin=Duree(jours=1),
    )
    edt.ajoute(tache)
    assert edt._activites == [tache]


def test_verification_duree_activites():
    """Au moment de l'ajout."""
    edt = EDT(activites=[])
    with pytest.raises(ValueError):
        edt.ajoute(
            Activite(
                tache=Tache(nom="A", duree=Duree(jours=2), prerequis=[]),
                debut=Duree(),
                fin=Duree(jours=1),
            )
        )


def test_verification_doublon(activites):
    """Au moment de l'ajout."""
    edt = EDT(activites=activites)
    with pytest.raises(ValueError):
        edt.ajoute(
            Activite(
                tache=Tache(nom="A", duree=Duree(jours=2), prerequis=[]),
                debut=Duree(),
                fin=Duree(jours=2),
            )
        )


def test_valide(activites):
    """Cas ok."""
    edt = EDT(activites)
    assert edt.est_valide()


def test_invalide(activites):
    """Cas pas ok."""
    a, b, c, d = activites
    d.debut = Duree()
    edt = EDT(activites=[a, b, c, d])
    assert not edt.est_valide()
