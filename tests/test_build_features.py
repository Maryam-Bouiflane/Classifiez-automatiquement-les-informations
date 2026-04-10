from src.data_loader import load_data
from src.data_preprocess import preprocess_data
from src.build_features import build_features
import config

def test_build_features():
    df_eval, df_sirh, df_sondage = load_data(
        config.DATA_EVAL_PATH,
        config.DATA_SIRH_PATH,
        config.DATA_SONDAGE_PATH
    )

    df = preprocess_data(df_eval, df_sirh, df_sondage)
    X, y, _ = build_features(df)

    assert X.shape[0] == y.shape[0]