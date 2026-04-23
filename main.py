from huggingface_hub import HfApi
import joblib
import os
from src.data_loader import load_data
from src.data_process import preprocess_data
from src.train_model import train_model, find_best_threshold, save_model
from src.evaluate_model import evaluate_model

def upload_to_hf():

    api = HfApi(token=os.environ["HF_TOKEN"])

    repo_id = "maryamb123/p4-classification-app"

    # upload model
    api.upload_file(
        path_or_fileobj="models/model.pkl",
        path_in_repo="model.pkl",
        repo_id=repo_id,
        repo_type="space"
    )

    # upload threshold
    api.upload_file(
        path_or_fileobj="models/threshold.pkl",
        path_in_repo="threshold.pkl",
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

    print("Metrics:", metrics)
    print(f"Threshold: {threshold:.3f}")

    # ======================
    # V1 SAVE LOCAL
    # ======================
    # save_model(model)
    # joblib.dump(threshold, "models/threshold.pkl")

    # ======================
    # V2 UPLOAD sur Hugging Face (SAVE)
    # ======================
    upload_to_hf()

if __name__ == "__main__":
    main()