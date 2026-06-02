def test_predict_edge_values(client):
    payload = {
        "age": 79,
        "genre": "M",
        "statut_marital": "Marié(e)",
        "departement": "Consulting",
        "poste": "Tech Lead",
        "nombre_experiences_precedentes": 1,
        "annee_experience_totale": 1,
        "annees_dans_l_entreprise": 1,
        "annees_dans_le_poste_actuel": 1,
        "satisfaction_employee_environnement": 0,
        "note_evaluation_precedente": 0,
        "satisfaction_employee_nature_travail": 0,
        "satisfaction_employee_equipe": 0,
        "satisfaction_employee_equilibre_pro_perso": 0,
        "note_evaluation_actuelle": 0,
        "heure_supplementaires": "Oui",
        "augementation_salaire_precedente": 0.0,
        "nombre_participation_pee": 0,
        "nb_formations_suivies": 0,
        "distance_domicile_travail": 1,
        "niveau_education": 1,
        "domaine_etude": "Infra & Cloud",
        "frequence_deplacement": "Aucun",
        "annees_depuis_la_derniere_promotion": 0,
        "annes_sous_responsable_actuel": 0
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert 0 <= data["probability"] <= 1
    assert data["prediction"] in [0, 1]