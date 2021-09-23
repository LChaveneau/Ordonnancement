"""Description
Test simple sur l'algorithme"""

from ordonnancement import Probleme, Tache, Prerequis, genere_graphe, resous_EDT, resous_Calendrier, Activite, EDT, Date, Calendrier, Duree, Datation
import pytest
import ordonnancement as ordo

@pytest.fixture
def probleme():
    return Probleme.par_str("""
    A / 1 annee / B fin (1 annees) |  C debut  / cA
    B / 2 annees / C fin/ cB
    C / 4 annees / / cC
    """)

@pytest.fixture
def date():
    return Date(jours=12, mois=10, annees=1998, heures=12)

def test_convertit_valide_repos(date):
    """Teste si la date est bien décalée aprés les jours de repos"""
    entree=date
    attendu=Date(jours=14, mois=10, annees=1998, heures=12)
    assert ordo.algorithme._convertit_valide_repos(entree, jours_repos="lundi mardi") == attendu

def test_convertit_valide_repos(date):
    """Teste si la date n'est pas décalée si le jours de la date n'appartient pas aux jours de repos"""
    entree=date
    attendu=Date(jours=14, mois=10, annees=1998, heures=12)
    assert ordo.algorithme._convertit_valide_repos(entree, jours_repos="samedi dimanche") == entree

def test_convertit_valide_heure(date):
    """Teste si la date est bien décalée aux heures de travail"""
    entree=date
    attendu=Date(jours=12, mois=10, annees=1998, heures=13)
    assert ordo.algorithme._convertit_valide_heure(entree, heures_execution="13-18") == attendu
    
def test_convertit_valide_heure2(date):
    """Teste si la date n'est pas décalée si elle est déjà comprise dans les heures de travail"""
    entree=date
    assert ordo.algorithme._convertit_valide_heure(entree, heures_execution="11-18") == entree

def test_calcule_duree_max_journalier():
    """Teste le calcul de travail journalier entre une plage horaire d'heure"""
    entree1="12-23"
    attendu=11
    entree2="14-01"
    assert ordo.algorithme._calcule_duree_max_journalier(entree1)==attendu
    assert ordo.algorithme._calcule_duree_max_journalier(entree2)==attendu
    
def test_resous_Calendrier(probleme):
    """Teste simplement sur la résolution du calendrier."""
    entree=probleme
    attendu = Calendrier(
        dates=[
            Datation(
                tache=Tache(
                    nom='C', 
                    duree=Duree(annees=4), 
                    prerequis=[], 
                    correspondance='cC'), 
                date_debut=Date(jours=23, mois=12, annees=1998), 
                date_fin=Date(jours=23, mois=12, annees=2002)), 
            Datation(
                tache=Tache(
                    nom='B', 
                    duree=Duree(annees=2), 
                    prerequis=[
                        Prerequis(
                            nom='C', 
                            typ='fin', 
                            latence=Duree())], 
                    correspondance='cB'), 
                date_debut=Date(jours=23, mois=12, annees=2002), 
                date_fin=Date(jours=23, mois=12, annees=2004)), 
            Datation(tache=Tache(
                nom='A', 
                duree=Duree(annees=1), 
                prerequis=[
                    Prerequis(
                        nom='B', 
                        typ='fin', 
                        latence=Duree(annees=1)), 
                    Prerequis(
                        nom='C', 
                        typ='debut', 
                        latence=Duree())], 
                correspondance='cA'),
            date_debut=Date(jours=23, mois=12, annees=2005), 
            date_fin=Date(jours=23, mois=12, annees=2006)
                    )
        ]
    )

    assert resous_Calendrier(entree, date_commencement="23/12/1998") == attendu
    
def test_resous_EDT(probleme):
    """Teste simplement sur la résolution de l'emploi du temps"""
    entree=probleme
    attendu=EDT(
        activites=[
            Activite(
                tache=Tache(
                    nom='C', 
                    duree=Duree(annees=4), 
                    prerequis=[], 
                    correspondance='cC'), 
                debut=Duree(), 
                fin=Duree(annees=4)), 
            Activite(
                tache=Tache(
                    nom='B', 
                    duree=Duree(annees=2), 
                    prerequis=[
                        Prerequis(
                            nom='C', 
                            typ='fin', 
                            latence=Duree())], 
                    correspondance='cB'), 
                debut=Duree(annees=4), 
                fin=Duree(annees=6)), 
            Activite(
                tache=Tache(
                    nom='A', 
                    duree=Duree(annees=1), 
                    prerequis=[
                        Prerequis(
                            nom='B', 
                            typ='fin', 
                            latence=Duree(annees=1)), 
                        Prerequis(nom='C', typ='debut', 
                                  latence=Duree())], 
                    correspondance='cA'), 
                debut=Duree(annees=7), 
                fin=Duree(annees=8)
            )
        ]
    )
    assert resous_EDT(probleme)==attendu
    
def test_calcule_repos():
    """Teste sur le calcule de temps d'éxécution des tâches si il y a présence de jours de repos."""
    entree=Duree(jours=7)
    attendu=Duree(jours=9)
    assert ordo.algorithme._calcule_repos(entree,nb_jours_repos=2)==attendu

def test_calcule_journalier():
    """Teste sur le calcule de temps d'éxécution des tâches si il y a présence d'heure maximum d'éxécution de tâches journalier."""
    entree=Duree(heures=12)
    attendu=Duree(heures=24)
    assert ordo.algorithme._calcule_journalier(entree, duree_max_journalier=12)
    
def test_erreur_algorithme():
    """Teste si les conditions de bon déroulement de l'algorithme ne sont pas tenues."""
    probleme_sans_solution=Probleme.par_str("""
    A / 1 annee / B fin (1 annees) |  C debut  / cA
    B / 2 annees / C fin/ cB
    C / 4 annees / A fin/ cC
    """)
    with pytest.raises(ValueError):
        resous_EDT(probleme_sans_solution)
    with pytest.raises(ValueError):
        resous_Calendrier(probleme_sans_solution, date_commencement="23/12/1998")

def test_calcule_demarrage(probleme):
    """Teste sur quel prérequis doit-t'il commencer"""
    edt=resous_EDT(probleme)
    nouvelle_tache=Tache(nom="D", 
                         duree=Duree(annees=1), 
                         prerequis=[
                             Prerequis(
                                 nom="B", 
                                 typ="fin", 
                                 latence=Duree(annees=3)
                             ),
                             Prerequis(
                             nom="A",
                             typ="fin",
                             latence=Duree(annees=14)
                             )
                         ],
                         correspondance="cD"
                        )
    attendu = Duree(annees=22)
    non_attendu = Duree(annees=9)
    assert ordo.algorithme._calcule_demarrage(nouvelle_tache, edt)==attendu
    assert not ordo.algorithme._calcule_demarrage(nouvelle_tache, edt)!=non_attendu
    

def test_calcule_demarrage_commencement(probleme):
    """Teste sur quel prérequis doit-t'il commencer. Ici l'emploi du temps est vide, il commencera donc a la durée 0."""
    edt=EDT(activites=[])
    nouvelle_tache=Tache(nom="D", 
                         duree=Duree(annees=1), 
                         prerequis=[],
                         correspondance="cD"
                        )
    assert ordo.algorithme._calcule_demarrage(nouvelle_tache, edt)==Duree()
    
def test_calcule_demarrage2_commencement():
    """Teste sur quel prérequis doit-t'il commencer. Ici l'emploi du temps est vide, il commencera donc à la date de commencement."""
    calendrier=Calendrier(dates=[])
    nouvelle_tache=Tache(nom="D", 
                         duree=Duree(annees=1), 
                         prerequis=[],
                         correspondance="cD"
                        )
    assert ordo.algorithme._calcule_demarrage2(nouvelle_tache, calendrier, date_commencement=Date(annees=1998, mois=12, jours=23))==Date(jours=23, mois=12, annees=1998)

def test_calcule_demarrage(probleme):
    """Teste sur quel prérequis doit-t'il commencer."""
    calendrier=resous_Calendrier(probleme, date_commencement="23/12/1998")
    nouvelle_tache=Tache(nom="D", 
                         duree=Duree(annees=1), 
                         prerequis=[
                             Prerequis(
                                 nom="B", 
                                 typ="fin", 
                                 latence=Duree(annees=3)
                             ),
                             Prerequis(
                             nom="A",
                             typ="fin",
                             latence=Duree(annees=14)
                             )
                         ],
                         correspondance="cD"
                        )
    
    attendu = Date(jours=23, mois=12, annees=2020)
    non_attendu = Date(jours=23, mois=12, annees=2007)
    assert ordo.algorithme._calcule_demarrage2(nouvelle_tache, calendrier, date_commencement=Date(annees=1998, mois=12, jours=23))==attendu
    assert not ordo.algorithme._calcule_demarrage2(nouvelle_tache, calendrier, date_commencement=Date(annees=1998, mois=12, jours=23))==non_attendu