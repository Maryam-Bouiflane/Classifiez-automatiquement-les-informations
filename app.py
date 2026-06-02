# v1 gradio interface only (no API mounted)
# import gradio as gr
# import pandas as pd
# import joblib

# model = joblib.load("models/model.pkl")
# threshold = joblib.load("models/threshold.pkl")
# df = pd.read_csv("data/final_dataset.csv")
# df =df.sort_values(by="id_employee").reset_index(drop=True)

# # ======================
# # GET IDS
# # ======================
# employee_ids = df["id_employee"].astype(str).tolist()

# # ======================
# # PREDICT FROM ID
# # ======================
# def predict_from_id(employee_id):

#     row = df[df["id_employee"].astype(str) == str(employee_id)]

#     if row.empty:
#         return "ID not found", None, "Check dataset"

#     X = row.drop(columns=["a_quitte_l_entreprise", "id_employee"], errors="ignore")

#     proba = model.predict_proba(X)[0][1]
#     pred = int(proba >= threshold)

#     if pred == 1:
#         label = "⚠️ Employee likely to leave"
#         advice = "High churn risk → retention action recommended"
#     else:
#         label = "✅ Employee stable"
#         advice = "Low churn risk"

#     return label, round(float(proba), 3), advice


# # ======================
# # UI
# # ======================
# demo = gr.Interface(
#     fn=predict_from_id,
#     inputs=gr.Dropdown(employee_ids, label="Select Employee ID"),
#     outputs=[
#         gr.Text(label="Prediction"),
#         gr.Number(label="Probability"),
#         gr.Text(label="Advice")
#     ],
#     title="Employee Attrition Prediction (by ID)"
# )

# demo.launch(server_name="0.0.0.0", server_port=7860)

# v2
import gradio as gr
from gradio.routes import mount_gradio_app
from fastapi import Body, FastAPI, Path
from src.schemas import EmployeeData
import pandas as pd
import joblib

# ======================
# LOAD MODEL & DATA
# ======================

model = joblib.load("models/model.pkl")
threshold = joblib.load("models/threshold.pkl")

df = pd.read_csv("data/final_dataset.csv")
df = df.sort_values(by="id_employee").reset_index(drop=True)

employee_ids = df["id_employee"].astype(str).tolist()

# ======================
# UTILS
# ======================

def predict_proba_df(input_df):

    # probability of churn (class 1)
    prob = model.predict_proba(input_df)[0][1]

    # threshold comparison
    pred = int(prob >= threshold)

    return pred, prob

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
# PREDICT
# ======================

@app.post("/predict")
def predict(data: EmployeeData):

    # Pydantic -> dict
    input_data = data.model_dump()

    # dict -> dataframe
    input_df = pd.DataFrame([input_data])

    pred, prob = predict_proba_df(input_df)

    return {
        "prediction": pred,
        "probability": float(prob)
    }

# ======================
# GRADIO UI FUNCTION
# ======================

def predict_ui(employee_id):

    row = df[df["id_employee"].astype(str) == str(employee_id)]

    if row.empty:
        return "ID not found", None, "Check dataset"

    X = row.drop(
        columns=["a_quitte_l_entreprise", "id_employee"],
        errors="ignore"
    )

    pred, prob = predict_proba_df(X)

    if pred == 1:
        label = "⚠️ Employee likely to leave"
        advice = "High churn risk → retention action recommended"
    else:
        label = "✅ Employee stable"
        advice = "Low churn risk"

    return label, round(float(prob), 3), advice

# ======================
# GRADIO INTERFACE
# ======================

demo = gr.Interface(
    fn=predict_ui,
    inputs=gr.Dropdown(
        employee_ids,
        label="Select Employee ID"
    ),
    outputs=[
        gr.Text(label="Prediction"),
        gr.Number(label="Probability"),
        gr.Text(label="Advice")
    ],
    title="Employee Churn Prediction"
)

# ======================
# MOUNT GRADIO
# ======================

app = mount_gradio_app(
    app,
    demo,
    path="/ui"
)