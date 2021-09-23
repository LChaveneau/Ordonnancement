"""Description.
Contient les tests du module probleme.
"""
import pytest
from pendulum import duration, datetime
from ordonnancement import Probleme, Tache, Prerequis, Duree

#### Test sur la classe Duree

duree_A = Duree(annees=1, secondes=78)
duree_B = Duree(mois=14, minutes=23, semaines=2)
duree_C = Duree(heures=23, jours=42)
duree_D = Duree(minutes=34)
duree_E = Duree()


def est_duree():
    """Teste le type de l'objet"""
    for duree in [duree_A, duree_B, duree_C, duree_D, duree_E]:
        assert isinstance(duree, Duree)


def test_duree_positive():
    """Vérifie que la durée doit-être positive"""
    with pytest.raises(ValueError):
        Duree(secondes=-1)


def test_convertit_duration():
    """Teste la convertion en objet Duration"""
    entree = duree_A
    attendu = duration(seconds=78, years=1)
    assert entree._convertit_duration() == attendu


def test_convertit_duree():
    """Teste la convertion d'un objet Duration vers un objet Duree"""
    entree = duration(years=23, seconds=12)
    attendu = Duree(annees=23, secondes=12)
    assert Duree._convertit_duree(entree) == attendu


def test_add():
    """Teste l'addition par la fonction add"""
    entree = Duree(annees=23, secondes=12)
    attendu = Duree(annees=24, secondes=23)
    assert entree.add(Duree(annees=1, secondes=11)) == attendu


def test_addition():
    """Teste l'addition"""
    entree = Duree(annees=23, secondes=12)
    attendu = Duree(annees=24, secondes=23)
    assert entree + Duree(annees=1, secondes=11) == attendu


def test_soustraction():
    """Teste la soustraction"""
    entree = Duree(annees=23, secondes=12)
    attendu = Duree(annees=22, secondes=1)
    assert entree - Duree(annees=1, secondes=11) == attendu


def test_egalite_inegalite():
    """Teste l'egalité ou l'inégalité"""
    assert not duree_A == duree_B
    assert duree_A != duree_B
    assert Duree(minutes=1) == Duree(secondes=60)
    assert not Duree(minutes=2) != Duree(secondes=120)
    assert duree_E == Duree(secondes=0)


def test_superiorite_inferiorite():
    """Teste l'infériorité et la supériorité"""
    assert duree_A < duree_B
    assert not duree_B < duree_C
    assert duree_C > duree_D
    assert duree_D < duree_C
    assert Duree(minutes=1) >= Duree(secondes=60)
    assert Duree(minutes=1, secondes=1) >= Duree(secondes=60)


def test_par_str():
    """Teste le constructeur alternatif"""
    entree = Duree.par_str("1 annees + 78 secondes")
    attendu = duree_A
    assert entree == attendu


def test_get_item():
    """Teste le get_item"""
    entree = Duree(secondes=6788)
    attendu = 6788
    assert entree["secondes"] == attendu


def test_repr():
    """Teste la représentation"""
    assert repr(Duree(secondes=12, annees=34)) == "Duree(secondes=12, annees=34)"


def test_repr_aucune_duree():
    """Teste la représentation de l'objet Duree quand il n'a aucune durée"""
    assert repr(Duree()) == "Duree(Aucune durée)"


#### Test sur la classe Prerequis


def test_post_init():
    """Teste les erreurs"""
    with pytest.raises(ValueError):
        Prerequis(nom="A", typ="ej", latence=Duree(annees=23, jours=8395))
    with pytest.raises(ValueError):
        Prerequis(nom="A", typ="debut", latence=23)


def test_constructeur_alternatif_Prerequis():
    """Teste le constructeur alternatif"""
    entree = Prerequis.par_str("A debut (13 annees + 56 secondes)")
    attendu = Prerequis(nom="A", typ="debut", latence=Duree(annees=13, secondes=56))
    assert entree == attendu


#### Test sur la classe Tache

A = Tache(nom="A", duree=Duree(jours=3), prerequis=[], correspondance="Poncer")

B = Tache(
    nom="B",
    duree=Duree(jours=67),
    prerequis=[Prerequis(nom="A", typ="debut", latence=Duree())],
    correspondance="Plaquo",
)
C = Tache(
    nom="C",
    duree=Duree(jours=34),
    prerequis=[
        Prerequis(nom="B", typ="debut", latence=Duree()),
        Prerequis(nom="A", typ="fin", latence=Duree(secondes=56)),
    ],
    correspondance="Peinture",
)


def test_post_init_tache():
    """Teste les erreurs de conception."""
    ###Teste si un nom est utilisé pour un prérequis et pour un nom de tache
    with pytest.raises(ValueError):
        Tache(
            nom="A",
            duree=Duree(jours=34),
            prerequis=[
                Prerequis(nom="B", typ="debut", latence=Duree()),
                Prerequis(nom="A", typ="fin", latence=Duree(secondes=56)),
            ],
            correspondance="Rien",
        )
    # Test si deux prérequis dans une tâche porte le même nom
    with pytest.raises(ValueError):
        Tache(
            nom="A",
            duree=Duree(jours=34),
            prerequis=[
                Prerequis(nom="B", typ="debut", latence=Duree()),
                Prerequis(nom="B", typ="fin", latence=Duree(secondes=56)),
            ],
            correspondance="Rien",
        )

    ### Test si la durée de la tache n'est pas égale à 0.
    with pytest.raises(ValueError):
        Tache(
            nom="A",
            duree=Duree(),
            prerequis=[
                Prerequis(nom="B", typ="debut", latence=Duree()),
                Prerequis(nom="C", typ="fin", latence=Duree(secondes=56)),
            ],
            correspondance="Rien",
        )


def constructeur_alternatif_Tache():
    """Teste le constructeur alternatif"""
    entree = Tache.par_str("A / 34 secondes / B debut | C fin (67 secondes) / Rien")
    attendu = Tache(
        nom="A",
        duree=Duree(secondes=34),
        prerequis=[
            Prerequis(nom="B", typ="debut", duree=Duree()),
            Prerequis(nom="C", typ="fin", duree=Duree(secondes=67)),
        ],
        correspondance="Rien",
    )
    assert entree == attendu


def test_message():
    """Test le message des prerequis d'une tâche"""
    entree = C
    attendu = "debut de B et fin de A + 56 secondes"
    assert C._messages_(brute=False) == attendu


#### Test sur la classe Probleme


def test_objet_latence():
    pass


@pytest.fixture
def taches():
    """4 taches pour les tests suivants."""
    a = A
    b = B
    c = C
    return [a, b, c]


def test_instanciation(taches):
    """Création."""
    probleme = Probleme(taches=taches)
    assert isinstance(probleme, Probleme)
    assert probleme._taches == {tache.nom: tache for tache in taches}


def test_egalite(taches):
    """Doit être différent de l'identité."""
    probleme1 = Probleme(taches)
    probleme2 = Probleme(taches)
    assert probleme1 == probleme2


def test_validation_doublon(taches):
    """Vérifie la détection de deux tâches avec le même nom."""
    a, b, c = taches
    d = Tache(
        nom="A",
        duree=Duree(secondes=1),
        prerequis=[
            Prerequis(nom="B", typ="debut", latence=Duree()),
            Prerequis(nom="C", typ="fin", latence=Duree(secondes=56)),
        ],
        correspondance="Rien",
    )
    with pytest.raises(ValueError):
        Probleme([a, b, c, d])


def test_validation_taches(taches):
    """Vérifie la détection de prérequis phantome."""
    a, b, c = taches
    d = Tache(
        nom="D",
        duree=Duree(secondes=1),
        prerequis=[
            Prerequis(nom="F", typ="debut", latence=Duree()),
            Prerequis(nom="C", typ="fin", latence=Duree(secondes=56)),
        ],
        correspondance="Rien",
    )
    with pytest.raises(ValueError):
        Probleme([a, b, c, d])


def test_taches(taches):
    """Teste la propriété taches."""
    probleme = Probleme(taches)
    assert "taches" not in vars(probleme)
    assert taches == list(probleme.taches)


def test_noms(taches):
    """Teste la propriété noms."""
    probleme = Probleme(taches)
    assert "noms" not in vars(probleme)
    assert list("ABC") == list(probleme.noms)


def test_acces(taches):
    """Utilisation de []."""
    probleme = Probleme(taches)
    assert probleme["A"] == A


def test_repr():
    """Teste le repr."""
    probleme = Probleme(
        taches=[
            Tache(nom="A", duree=Duree(secondes=1), prerequis=[], correspondance="Gt")
        ]
    )
    assert (
        repr(probleme)
        == "Probleme(taches=[Tache(nom='A', duree=Duree(secondes=1), prerequis=[], correspondance='Gt')])"
    )


def test_constructeur(taches):
    """Constructeur alternatif."""
    entree = """
A / 3 jours // Poncer 
B / 67 jours / A debut / Plaquo
C / 34 jours / B debut | A fin (56 secondes) / Peinture
"""
    probleme = Probleme.par_str(entree)
    assert probleme == Probleme(taches)


def test_correspondances(taches):
    """Teste la propriété correspondances"""
    probleme = Probleme(taches)
    assert "prerequis" not in vars(probleme)
    assert ["Poncer", "Plaquo", "Peinture"] == list(probleme.correspondances)
