import json
from fastapi import FastAPI, Path, Body, HTTPException
from src.schemas import EmployeeData
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import joblib
import pandas as pd
import os
from dotenv import load_dotenv

# ======================
# LOAD MODEL
# ======================

model = joblib.load("models/model.pkl")
threshold = joblib.load("models/threshold.pkl")

# ======================
# FASTAPI
# ======================

app = FastAPI(
    title="Churn Prediction API"
)

# ======================
# DATABASE
# ======================

load_dotenv()
user = os.getenv("API_USER")
password = os.getenv("API_USER_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
DB_URL = f"postgresql://{user}:{password}@{host}:{port}/churn_db"

# Connexion à la base
engine = create_engine(DB_URL)
# Création d'une session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
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

    try:
        input_data = data.model_dump()

        employee_id = input_data.get("id_employee", None)

        df = pd.DataFrame([input_data])
        df = df.drop(columns=["id_employee"], errors="ignore")

        prob = model.predict_proba(df)[0][1]
        prediction = int(prob >= threshold)

        output_data = {
            "prediction": prediction,
            "probability": float(prob)
        }

        with SessionLocal() as session:
            session.execute(
                text("""
                    INSERT INTO predictions_log (employee_id, input_data, output_data)
                    VALUES (:employee_id, :input, :output)
                """),
                {
                    "employee_id": employee_id,
                    "input": json.dumps(input_data),
                    "output": json.dumps(output_data)
                }
            )
            session.commit()

        return output_data

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )


# ======================
# GET EMPLOYEE BY ID
# ======================

@app.get("/employee/{id}")
def get_employee(id: int = Path(..., description="ID of the employee to retrieve")):

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT * 
                FROM employees 
                WHERE id_employee = :id
            """),
            {"id": id}
        )

        employee = result.fetchone()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return dict(employee._mapping)
