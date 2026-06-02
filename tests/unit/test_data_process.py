import pandas as pd
import pytest
from src.data_process import preprocess_data


# ======================
# FIXTURE DATA RÉALISTE
# ======================
@pytest.fixture
def sample_data():

    df_eval = pd.DataFrame({
        "eval_number": ["emp_1", "emp_2"],
        "augementation_salaire_precedente": ["10%", "5%"]
    })

    df_sirh = pd.DataFrame({
        "id_employee": [1, 2],
        "a_quitte_l_entreprise": ["Oui", "Non"],
        "nombre_heures_travailless": [40, 40]  # doit être supprimée
    })

    df_sondage = pd.DataFrame({
        "code_sondage": [1, 2],
        "nombre_employee_sous_responsabilite": [2, 3],
        "ayant_enfants": ["Oui", "Non"],
        "satisfaction": [0.8, 0.6]
    })

    return df_eval, df_sirh, df_sondage


# ======================
# TEST 1: nettoyage %
# ======================
def test_salary_percentage_cleaning(sample_data):

    df_eval, df_sirh, df_sondage = sample_data

    df = preprocess_data(df_eval, df_sirh, df_sondage)

    assert df["augementation_salaire_precedente"].dtype == float
    assert df["augementation_salaire_precedente"].iloc[0] == 10.0


# ======================
# TEST 2: extraction eval_number
# ======================
def test_eval_number_extraction(sample_data):

    df_eval, df_sirh, df_sondage = sample_data

    df = preprocess_data(df_eval, df_sirh, df_sondage)

    # Vérifie que merge fonctionne via conversion
    assert len(df) == 2


# ======================
# TEST 3: merge correct
# ======================
def test_merge_integrity(sample_data):

    df_eval, df_sirh, df_sondage = sample_data

    df = preprocess_data(df_eval, df_sirh, df_sondage)

    # Vérifie que données sont bien fusionnées
    assert "satisfaction" in df.columns


# ======================
# TEST 4: mapping target
# ======================
def test_target_mapping(sample_data):

    df_eval, df_sirh, df_sondage = sample_data

    df = preprocess_data(df_eval, df_sirh, df_sondage)

    assert set(df["a_quitte_l_entreprise"].unique()) <= {0, 1}


# ======================
# TEST 5: suppression colonnes
# ======================
def test_columns_dropped(sample_data):

    df_eval, df_sirh, df_sondage = sample_data

    df = preprocess_data(df_eval, df_sirh, df_sondage)

    assert "nombre_heures_travailless" not in df.columns
    assert "nombre_employee_sous_responsabilite" not in df.columns
    assert "ayant_enfants" not in df.columns


# ======================
# TEST 6: colonnes techniques supprimées
# ======================
def test_technical_columns_removed(sample_data):

    df_eval, df_sirh, df_sondage = sample_data

    df = preprocess_data(df_eval, df_sirh, df_sondage)

    assert "eval_number" not in df.columns
    assert "code_sondage" not in df.columns


# ======================
# TEST 7: robustesse valeurs invalides
# ======================
def test_invalid_eval_number():

    df_eval = pd.DataFrame({
        "eval_number": ["emp_x"],  # invalide
        "augementation_salaire_precedente": ["10%"]
    })

    df_sirh = pd.DataFrame({
        "id_employee": [1],
        "a_quitte_l_entreprise": ["Oui"]
    })

    df_sondage = pd.DataFrame({
        "code_sondage": [1]
    })

    df = preprocess_data(df_eval, df_sirh, df_sondage)

    # merge left → doit garder ligne
    assert len(df) == 1