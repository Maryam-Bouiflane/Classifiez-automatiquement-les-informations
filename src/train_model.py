import joblib
import numpy as np
import logging

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve
from sklearn.utils import shuffle

# ======================
# TRAIN MODEL
# ======================
def train_model(df, test_mode=False):

    # ======================
    # FEATURES / TARGET
    # ======================
    X = df.drop(
        columns=[
            "a_quitte_l_entreprise",
            "id_employee"
        ],
        errors="ignore"
    )

    y = df["a_quitte_l_entreprise"]

    # ======================
    # SAFETY CHECKS
    # ======================
    if y.nunique() < 2:
        raise ValueError("Need at least 2 classes in target")

    min_class_count = y.value_counts().min()

    if min_class_count < 2:
        raise ValueError(
            "Each class must have at least 2 samples for reliable training"
        )

    # ======================
    # PREPROCESSING
    # ======================
    num_cols = X.select_dtypes(include="number").columns
    cat_cols = X.select_dtypes(exclude="number").columns

    preprocess = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(
            drop="first",
            handle_unknown="ignore",
            sparse_output=False
        ), cat_cols)
    ])

    pipe = Pipeline([
        ("preprocess", preprocess),
        ("logreg", LogisticRegression(max_iter=11000))
    ])

    # ======================
    # ALWAYS SHUFFLE
    # ======================
    from sklearn.utils import shuffle
    X, y = shuffle(X, y, random_state=42)

    # ======================
    # TRAIN / TEST SPLIT (SAFE)
    # ======================
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y   # IMPORTANT: NEVER DISABLE
    )

    # ======================
    # MODE TEST (FAST)
    # ======================
    if test_mode:
        pipe.fit(X_train, y_train)
        return pipe, X_test, y_test

    # ======================
    # MODE PROD (GRIDSEARCH)
    # ======================
    param_grid = {
        "logreg__C": [0.01, 0.1, 1, 10],
        "logreg__solver": ["lbfgs", "liblinear"],
        "logreg__class_weight": [None, "balanced"]
    }

    cv = min(5, min_class_count)
    if cv < 2:
        cv = 2

    grid = GridSearchCV(
        pipe,
        param_grid,
        cv=cv,
        scoring="f1",
        refit=True,
        n_jobs=-1
    )

    grid.fit(X_train, y_train)

    model = grid.best_estimator_

    return model, X_test, y_test


# ======================
# THRESHOLD OPTIMISATION
# ======================
def find_best_threshold(model, X, y):

    y_proba = model.predict_proba(X)[:, 1]

    precisions, recalls, thresholds = precision_recall_curve(y, y_proba)

    f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-9)

    best_threshold = thresholds[np.argmax(f1_scores[:-1])]

    return best_threshold
