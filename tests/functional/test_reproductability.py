payload = {
        "age": 35,
        "genre": "M",
        "statut_marital": "Marié(e)",
        "departement": "Consulting",
        "poste": "Tech Lead",
        "nombre_experiences_precedentes": 2,
        "annee_experience_totale": 5,
        "annees_dans_l_entreprise": 3,
        "annees_dans_le_poste_actuel": 2,
        "satisfaction_employee_environnement": 3,
        "note_evaluation_precedente": 4,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "note_evaluation_actuelle": 4,
        "heure_supplementaires": "Non",
        "augementation_salaire_precedente": 10.5,
        "nombre_participation_pee": 2,
        "nb_formations_suivies": 1,
        "distance_domicile_travail": 10,
        "niveau_education": 3,
        "domaine_etude": "Infra & Cloud",
        "frequence_deplacement": "Aucun",
        "annees_depuis_la_derniere_promotion": 1,
        "annes_sous_responsable_actuel": 2
    }


def test_reproducibility(client):
    r1 = client.post("/predict", json=payload).json()
    r2 = client.post("/predict", json=payload).json()

    assert r1 == r2