import pandas as pd
import numpy as np
import pytest
import os

from src.train_model import train_model, find_best_threshold, save_model


# ======================
# FIXTURE DATA RÉALISTE
# ======================
@pytest.fixture
def sample_training_data():

    df = pd.DataFrame({
        "age": [25, 30, 45, 50, 28, 40, 35, 29, 41, 38],
        "genre": ["Male", "Female"] * 5,
        "departement": ["IT", "HR", "Sales", "IT", "HR"] * 2,
        "satisfaction": np.random.rand(10),
        "revenu_mensuel": np.random.randint(3000, 6000, 10),
        "niveau_hierarchique_poste": [1, 2, 2, 3, 1] * 2,
        "id_employee": list(range(10)),
        "a_quitte_l_entreprise": [0, 1] * 5
    })

    return df


# ======================
# TEST 1: entraînement OK
# ======================
def test_train_model_returns_pipeline(sample_training_data):

    model, X_test, y_test = train_model(sample_training_data, test_mode=True)

    assert hasattr(model, "predict")
    assert hasattr(model, "predict_proba")

    assert len(X_test) > 0
    assert len(y_test) > 0


# ======================
# TEST 2: pipeline contient preprocessing
# ======================
def test_pipeline_structure(sample_training_data):

    model, _, _ = train_model(sample_training_data, test_mode=True)

    assert "preprocess" in model.named_steps
    assert "logreg" in model.named_steps


# ======================
# TEST 3: predict_proba shape
# ======================
def test_predict_proba_shape(sample_training_data):

    model, X_test, _ = train_model(sample_training_data, test_mode=True)

    proba = model.predict_proba(X_test)

    assert proba.shape[1] == 2  # binaire


# ======================
# TEST 4: threshold valide
# ======================
def test_find_best_threshold(sample_training_data):

    model, X_test, y_test = train_model(sample_training_data, test_mode=True)

    threshold = find_best_threshold(model, X_test, y_test)

    assert 0 <= threshold <= 1


# ======================
# TEST 5: threshold produit des prédictions
# ======================
def test_threshold_produces_predictions(sample_training_data):

    model, X_test, y_test = train_model(sample_training_data, test_mode=True)

    threshold = find_best_threshold(model, X_test, y_test)

    proba = model.predict_proba(X_test)[:, 1]
    preds = (proba >= threshold).astype(int)

    assert len(preds) == len(y_test)


# ======================
# TEST 6: sauvegarde modèle
# ======================
def test_save_model(tmp_path, sample_training_data):

    model, _, _ = train_model(sample_training_data, test_mode=True)

    path = tmp_path / "model.pkl"

    save_model(model, path)

    assert os.path.exists(path)


# ======================
# Test 7 : vérifie que le modèle génère des prédictions valides (non vide)
# ======================
def test_model_outputs_predictions(sample_training_data):

    model, X_test, _ = train_model(sample_training_data, test_mode=True)

    preds = model.predict(X_test)

    assert len(preds) == len(X_test)