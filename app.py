import gradio as gr
import pandas as pd
import joblib

model = joblib.load("models/model.pkl")
threshold = joblib.load("models/threshold.pkl")
df = pd.read_csv("data/final_dataset.csv")
df =df.sort_values(by="id_employee").reset_index(drop=True)

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
demo = gr.Interface(
    fn=predict_from_id,
    inputs=gr.Dropdown(employee_ids, label="Select Employee ID"),
    outputs=[
        gr.Text(label="Prediction"),
        gr.Number(label="Probability"),
        gr.Text(label="Advice")
    ],
    title="Employee Attrition Prediction (by ID)",
    allow_flagging="never",
    flagging_mode="never"
)

demo.launch(server_name="0.0.0.0", server_port=7860)