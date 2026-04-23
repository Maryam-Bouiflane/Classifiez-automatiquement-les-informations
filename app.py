import gradio as gr
import pandas as pd
import joblib
from huggingface_hub import hf_hub_download

# ======================
# LOAD MODEL + DATA (V2 : depuis Hugging Face)
# ======================
repo_id="maryamb123/p4-classification-app"
model_path = hf_hub_download(
    repo_id=repo_id,
    filename="model.pkl",
    repo_type="space"
)
threshold_path = hf_hub_download(
    repo_id=repo_id,
    filename="threshold.pkl",
    repo_type="space"
)
model = joblib.load(model_path)
threshold = joblib.load(threshold_path)

# V1 locale
# model = joblib.load("models/model.pkl")
# threshold = joblib.load("models/threshold.pkl")

# dataset utilisé pour prédire
df = pd.read_csv("clean/final_dataset.csv")  # adapte le chemin

# ======================
# GET IDS
# ======================
employee_ids = df["id_employee"].astype(str).tolist()

# ======================
# PREDICT FROM ID
# ======================
def predict_from_id(employee_id):

    row = df[df["id_employee"].astype(str) == str(employee_id)]

    if row.empty:
        return "ID not found", None, "Check dataset"

    X = row.drop(columns=["a_quitte_l_entreprise", "id_employee"], errors="ignore")

    proba = model.predict_proba(X)[0][1]
    pred = int(proba >= threshold)

    if pred == 1:
        label = "⚠️ Employee likely to leave"
        advice = "High churn risk → retention action recommended"
    else:
        label = "✅ Employee stable"
        advice = "Low churn risk"

    return label, round(float(proba), 3), advice


# ======================
# UI
# ======================
gr.Interface(
    fn=predict_from_id,
    inputs=gr.Dropdown(employee_ids, label="Select Employee ID"),
    outputs=[
        gr.Text(label="Prediction"),
        gr.Number(label="Probability"),
        gr.Text(label="Advice")
    ],
    title="Employee Attrition Prediction (by ID)"
).launch()