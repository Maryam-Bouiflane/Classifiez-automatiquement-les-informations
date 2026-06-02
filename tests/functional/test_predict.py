valid_payload = {
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

def test_predict_success(client):
    response = client.post("/predict", json=valid_payload)

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "probability" in data

    assert data["prediction"] in [0, 1]
    assert 0 <= data["probability"] <= 1

def test_predict_invalid_age(client):
    payload = valid_payload.copy()
    payload["age"] = 10  # invalide (<18)

    response = client.post("/predict", json=payload)

    assert response.status_code == 422

def test_predict_invalid_type(client):
    payload = valid_payload.copy()
    payload["age"] = "trente"

    response = client.post("/predict", json=payload)

    assert response.status_code == 422

def test_predict_missing_field(client):
    payload = valid_payload.copy()
    del payload["genre"]

    response = client.post("/predict", json=payload)

    assert response.status_code == 422

