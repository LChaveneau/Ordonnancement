"""Description.
Libraire pour un gui de la librairie ordonnancement.
"""
import ipywidgets as ipw
from IPython.display import display
from ordonnancement import *
from typing import List


class Application:
    def __init__(self):
        self.bouton = ipw.Button(description="Résoudre")

        self.zone_entree = ipw.Textarea(
            value="A / 1 semaine / /Créer la librairie \nB / 1 heure / A fin /Expliquer aux utilisateurs\nC / 34 secondes / A fin (3 jours) | B debut (2 heures + 56 minutes) / Mettre en ligne la librairie",
            layout=ipw.Layout(height="200px", width="700px"),
        )

        self.date_commencement = ipw.Text(
            value="23/12/1998",
            placeholder="Type something",
            description="Date de commencement des tâches:",
            disabled=False,
        )

        self.type_resolution = ipw.RadioButtons(
            options=["EDT", "Calendrier"],
            value="EDT",
            description="Type de résolution:",
            disabled=False,
        )

        self.determine_entier = ipw.Checkbox(
            value=False, description="Afficher la nature", disabled=False, indent=False
        )

        self.determine_brute = ipw.Checkbox(
            value=False,
            description="Afficher le temps brute",
            disabled=False,
            indent=False,
        )

        self.condition_nb_jours = ipw.IntSlider(
            value=0,
            min=0,
            max=6,
            step=1,
            description="Nombre de jours de repos",
            disabled=False,
            continuous_update=False,
            orientation="horizontal",
            readout=True,
            readout_format="d",
        )

        self.condition_jours = ipw.SelectMultiple(
            options=[
                "Lundi",
                "Mardi",
                "Mercredi",
                "Jeudi",
                "Vendredi",
                "Samedi",
                "Dimanche",
            ],
            description="Jours de repos",
            disabled=False,
            readout=True,
            continuous_update=False,
        )

        self.condition_nb_heures = ipw.FloatSlider(
            value=24,
            min=0.25,
            max=24,
            step=0.25,
            description="Nombre d'heure journaliers d'éxécution de tâches",
            disabled=False,
            continuous_update=False,
            orientation="horizontal",
            readout=True,
            readout_format=".1f",
        )

        self.condition_heures_min = ipw.FloatSlider(
            value=0,
            min=0,
            max=23.75,
            step=0.25,
            description="Heure debut",
            disabled=False,
            continuous_update=False,
            orientation="horizontal",
            readout=True,
            readout_format=".1f",
        )

        self.condition_heures_max = ipw.FloatSlider(
            value=0,
            min=0,
            max=23.75,
            step=0.25,
            description="Heure fin",
            disabled=False,
            continuous_update=False,
            orientation="horizontal",
            readout=True,
            readout_format=".1f",
        )

        self.zone_probleme = ipw.Output()
        self.zone_solution = ipw.Output()

    def affichage(self):
        sortie = ipw.interactive_output(
            self.construction, {"valeur": self.type_resolution}
        )
        widgets = ipw.HBox(
            [
                ipw.VBox(
                    [self.type_resolution, self.determine_brute, self.determine_entier]
                ),
                ipw.VBox([self.bouton, self.zone_entree]),
            ]
        )
        display(widgets, sortie)

    def construction(self, valeur: str = "EDT"):
        if valeur == "EDT":
            affichage = ipw.VBox(
                [
                    self.zone_probleme,
                    ipw.HBox([self.condition_nb_heures, self.condition_nb_jours]),
                    self.zone_solution,
                ]
            )
        else:
            affichage = ipw.VBox(
                [
                    self.date_commencement,
                    self.zone_probleme,
                    ipw.HBox(
                        [
                            ipw.VBox(
                                [self.condition_heures_min, self.condition_heures_max]
                            ),
                            self.condition_jours,
                        ]
                    ),
                    self.zone_solution,
                ]
            )
        self._sur_clique(self.bouton)
        self.bouton.on_click(self._sur_clique)
        display(affichage)

    def _sur_clique(self, b):
        self.zone_probleme.clear_output()
        self.zone_solution.clear_output()
        probleme = Probleme.par_str(self.zone_entree.value)
        brute = self.determine_brute.value
        entier = self.determine_entier.value
        if self.type_resolution.value == "EDT":
            heure = self.traite_heure(self.condition_nb_heures.value)
            jours = self.traite_nb_jours(self.condition_nb_jours.value)
            solution = resous_EDT(
                probleme, duree_max_journalier=heure, nb_jours_repos=jours
            )
            with self.zone_probleme:
                display(
                    probleme._genere_table_probleme(
                        brute=self.determine_brute.value,
                        entier=self.determine_entier.value,
                    )
                )
            with self.zone_solution:
                display(
                    solution._genere_table(
                        brute=self.determine_brute.value,
                        entier=self.determine_entier.value,
                    )
                )
        else:
            plage_horaire = self.traite_horaire(
                self.condition_heures_min.value, self.condition_heures_max.value
            )
            jours = self.traite_jours(self.condition_jours.value)
            solution = resous_Calendrier(
                probleme,
                date_commencement=self.date_commencement.value,
                heures_execution=plage_horaire,
                jours_repos=jours,
            )
            with self.zone_probleme:
                display(
                    probleme._genere_table_probleme(
                        brute=self.determine_brute.value,
                        entier=self.determine_entier.value,
                    )
                )
            with self.zone_solution:
                display(solution._genere_table(entier=self.determine_entier.value))

    @staticmethod
    def traite_horaire(valeur_min: float, valeur_max: float):
        if valeur_max - valeur_min == 24:
            return None
        elif valeur_min - valeur_max == 0:
            return None
        else:
            return f"{valeur_min}-{valeur_max}"

    @staticmethod
    def traite_nb_jours(valeur: int):
        if valeur == 0:
            return None
        else:
            return valeur

    @staticmethod
    def traite_jours(valeur: List[str]):
        if valeur:
            message=""
            for jours in valeur:
                 message+=f"{jours} "
            return message 
        else:
            return None

    @staticmethod
    def traite_heure(valeur: float):
        if valeur == 24:
            return None
        else:
            return valeur
