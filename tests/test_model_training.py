from sklearn.model_selection import train_test_split

from src.data_loader import load_data
from src.data_preprocess import preprocess_data
from src.build_features import build_features
from src.model_training import train_model
import config

def test_train_model():
    df_eval, df_sirh, df_sondage = load_data(
        config.DATA_EVAL_PATH,
        config.DATA_SIRH_PATH,
        config.DATA_SONDAGE_PATH
    )

    df = preprocess_data(df_eval, df_sirh, df_sondage)
    X, y, _ = build_features(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model = train_model(X_train, y_train, config.PARAM_GRID)

    assert model is not None