from huggingface_hub import HfApi
import joblib
import os
from src.data_loader import load_data
from src.data_process import preprocess_data
from src.train_model import train_model, find_best_threshold
from src.evaluate_model import evaluate_model

def upload_to_hf():

    api = HfApi(token=os.environ["HF_TOKEN"])

    repo_id = "maryamb123/p4-classification-app"

    # upload model
    api.upload_file(
        path_or_fileobj="models/model.pkl",
        path_in_repo="models/model.pkl",
        repo_id=repo_id,
        repo_type="space"
    )

    # upload threshold
    api.upload_file(
        path_or_fileobj="models/threshold.pkl",
        path_in_repo="models/threshold.pkl",
        repo_id=repo_id,
        repo_type="space"
    )

def main():

    # ======================
    # LOAD DATA
    # ======================
    df_eval, df_sirh, df_sondage = load_data(
        "data/raw/extrait_eval.csv",
        "data/raw/extrait_sirh.csv",
        "data/raw/extrait_sondage.csv"
    )

    # ======================
    # PREPROCESS
    # ======================
    df = preprocess_data(df_eval, df_sirh, df_sondage)

    # ======================
    # TRAIN
    # ======================
    model, X_test, y_test = train_model(df)

    # ======================
    # THRESHOLD
    # ======================
    threshold = find_best_threshold(model, X_test, y_test)

    # ======================
    # EVALUATION
    # ======================
    metrics = evaluate_model(model, X_test, y_test, threshold)
    
    print("RESULTS ON TEST SET:")
    print("Metrics:", metrics)
    print(f"Threshold: {threshold:.3f}")

    # ======================
    # SAVE LOCAL
    # ======================
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model.pkl")
    joblib.dump(threshold, "models/threshold.pkl")
    print("Model and threshold saved in 'models/' directory.")

    # ======================
    # UPLOAD sur Hugging Face
    # ======================
    # upload_to_hf()

if __name__ == "__main__":
    main()