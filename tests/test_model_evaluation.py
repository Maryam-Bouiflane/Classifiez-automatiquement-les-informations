import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression
from src.model_evaluation import evaluate_model


def test_evaluate_model_basic():
    # Données simples
    X_test = np.array([[0], [1], [2], [3]])
    y_test = np.array([0, 0, 1, 1])

    # Modèle simple entraîné
    model = LogisticRegression()
    model.fit(X_test, y_test)

    # Appel de la fonction
    metrics = evaluate_model(model, X_test, y_test, threshold=0.5)

    # Vérifier que toutes les métriques existent
    assert "f1" in metrics
    assert "roc_auc" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "accuracy" in metrics

    # Vérifier que les valeurs sont entre 0 et 1
    for value in metrics.values():
        assert 0.0 <= value <= 1.0


def test_evaluate_model_threshold_effect():
    X_test = np.array([[0], [1], [2], [3]])
    y_test = np.array([0, 0, 1, 1])

    model = LogisticRegression()
    model.fit(X_test, y_test)

    metrics_low = evaluate_model(model, X_test, y_test, threshold=0.3)
    metrics_high = evaluate_model(model, X_test, y_test, threshold=0.7)

    # Les résultats doivent changer avec le threshold
    assert metrics_low != metrics_high


def test_evaluate_model_perfect_model():
    # Cas parfait : prédictions parfaites
    class PerfectModel:
        def predict_proba(self, X):
            return np.array([[1, 0], [1, 0], [0, 1], [0, 1]])

    X_test = np.array([[0], [1], [2], [3]])
    y_test = np.array([0, 0, 1, 1])

    model = PerfectModel()

    metrics = evaluate_model(model, X_test, y_test, threshold=0.5)

    # Toutes les métriques doivent être parfaites
    assert metrics["f1"] == 1.0
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["accuracy"] == 1.0
    assert metrics["roc_auc"] == 1.0


def test_evaluate_model_invalid_model():
    # Modèle sans predict_proba
    class BadModel:
        pass

    X_test = np.array([[0], [1]])
    y_test = np.array([0, 1])

    model = BadModel()

    with pytest.raises(AttributeError):
        evaluate_model(model, X_test, y_test, threshold=0.5)