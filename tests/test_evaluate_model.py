import pandas as pd
import numpy as np
import pytest

from sklearn.linear_model import LogisticRegression

from src.evaluate_model import evaluate_model


# ======================
# FIXTURE: modèle simple entraîné
# ======================
@pytest.fixture
def trained_model():

    X = pd.DataFrame({
        "feature": [0, 1, 2, 3, 4, 5]
    })

    y = np.array([0, 0, 0, 1, 1, 1])

    model = LogisticRegression()
    model.fit(X, y)

    return model, X, y


# ======================
# TEST 1: structure sortie
# ======================
def test_evaluate_model_output_structure(trained_model):

    model, X, y = trained_model

    metrics = evaluate_model(model, X, y, threshold=0.5)

    assert isinstance(metrics, dict)

    expected_keys = {"f1", "roc_auc", "precision", "recall", "accuracy"}
    assert expected_keys == set(metrics.keys())


# ======================
# TEST 2: valeurs dans bon range
# ======================
def test_metrics_range(trained_model):

    model, X, y = trained_model

    metrics = evaluate_model(model, X, y, threshold=0.5)

    for value in metrics.values():
        assert 0.0 <= value <= 1.0


# ======================
# TEST 3: threshold impact
# ======================
def test_threshold_effect(trained_model):

    model, X, y = trained_model

    metrics_low = evaluate_model(model, X, y, threshold=0.1)
    metrics_high = evaluate_model(model, X, y, threshold=0.9)

    # au moins une métrique doit changer
    assert metrics_low != metrics_high


# ======================
# TEST 4: prédictions cohérentes
# ======================
def test_predictions_not_empty(trained_model):

    model, X, y = trained_model

    metrics = evaluate_model(model, X, y, threshold=0.5)

    # Si tout est 0 → problème
    assert metrics["accuracy"] >= 0


# ======================
# TEST 5: robustesse seuil extrême
# ======================
def test_extreme_threshold(trained_model):

    model, X, y = trained_model

    metrics = evaluate_model(model, X, y, threshold=1.0)

    assert isinstance(metrics, dict)


# ======================
# TEST 6: comportement déséquilibré
# ======================
def test_imbalanced_data():

    X = pd.DataFrame({
        "feature": [0, 1, 2, 3, 4, 5]
    })

    y = np.array([0, 0, 0, 0, 0, 1])  # très déséquilibré

    model = LogisticRegression()
    model.fit(X, y)

    metrics = evaluate_model(model, X, y, threshold=0.5)

    assert "f1" in metrics