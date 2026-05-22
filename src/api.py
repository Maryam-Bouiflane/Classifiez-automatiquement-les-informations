from fastapi import FastAPI
from schemas import EmployeeData

import joblib
import pandas as pd

# ======================
# LOAD MODEL
# ======================

model = joblib.load("../models/model.pkl")
threshold = joblib.load("../models/threshold.pkl")

# ======================
# FASTAPI
# ======================

app = FastAPI(
    title="Churn Prediction API"
)

# ======================
# ROOT
# ======================

@app.get("/")
def root():

    return {
        "message": "API is running"
    }

# ======================
# HEALTH
# ======================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }

# ======================
# PREDICT
# ======================

@app.post("/predict")
def predict(data: EmployeeData):

    # Pydantic → dict
    input_data = data.model_dump()

    # dict → dataframe
    df = pd.DataFrame([input_data])

    # only churn prediction probability : return P(classe 1) of this observation
    prob = model.predict_proba(df)[0][1]

    # threshold : comparaison si la proba >= au seuil, si true → 1 sinon 0
    prediction = int(prob >= threshold)

    return {
        "prediction": prediction,
        "probability": float(prob)
    }