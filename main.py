from sklearn.model_selection import train_test_split

import config
from src.data_loader import load_data
from src.data_preprocess import preprocess_data
from src.build_features import build_features
from src.model_training import train_model, find_best_threshold
from src.model_evaluation import evaluate_model
from src.utils import save_object

def main():
    # Load
    df_eval, df_sirh, df_sondage = load_data(
        config.DATA_EVAL_PATH,
        config.DATA_SIRH_PATH,
        config.DATA_SONDAGE_PATH
    )

    # Preprocess
    df = preprocess_data(df_eval, df_sirh, df_sondage)

    # Features
    X, y, encoder = build_features(df)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE,
        stratify=y
    )

    # Train
    model = train_model(X_train, y_train, config.PARAM_GRID)

    # Threshold
    threshold = find_best_threshold(model, X_train, y_train)

    # Evaluate
    metrics = evaluate_model(model, X_test, y_test, threshold)

    print("Metrics:", metrics)
    print("Threshold:", threshold)

    # Save
    save_object(model, "model.pkl")
    save_object(threshold, "threshold.pkl")
    save_object(encoder, "encoder.pkl")


if __name__ == "__main__":
    main()