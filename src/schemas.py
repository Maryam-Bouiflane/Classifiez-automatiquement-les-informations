from pydantic import BaseModel, Field, PositiveInt
from typing import Literal

class EmployeeData(BaseModel):
    id_employee : int | None = None
    age : int = Field(ge=18, lt=80)
    genre : Literal["F", "M"]
    statut_marital : Literal["Célibataire", "Marié", "Marié(e)", "Divorcé", "Divorcé(e)"]
    departement : str
    poste : str
    nombre_experiences_precedentes : PositiveInt
    annee_experience_totale : PositiveInt
    annees_dans_l_entreprise : PositiveInt
    annees_dans_le_poste_actuel : PositiveInt
    satisfaction_employee_environnement : int = Field(ge=0, le=5)
    note_evaluation_precedente : int = Field(ge=0, le=5)
    satisfaction_employee_nature_travail : int = Field(ge=0, le=5)
    satisfaction_employee_equipe : int = Field(ge=0, le=5)
    satisfaction_employee_equilibre_pro_perso : int = Field(ge=0, le=5)
    note_evaluation_actuelle : int = Field(ge=0, le=5)
    heure_supplementaires : Literal["Oui", "Non"]
    augementation_salaire_precedente : float = Field(ge=0, le=100)
    nombre_participation_pee : int = Field(ge=0, le=70)
    nb_formations_suivies : int = Field(ge=0)
    distance_domicile_travail : PositiveInt
    niveau_education : int = Field(ge=1, le=5)
    domaine_etude : str
    frequence_deplacement : Literal["Aucun", "Frequent", "Occasionnel"]
    annees_depuis_la_derniere_promotion : int = Field(ge=0)
    annes_sous_responsable_actuel : int = Field(ge=0)