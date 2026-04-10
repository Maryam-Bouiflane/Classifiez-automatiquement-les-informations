from src.data_loader import load_data
from src.data_preprocess import preprocess_data
import config

def test_preprocess():
    df_eval, df_sirh, df_sondage = load_data(
        config.DATA_EVAL_PATH,
        config.DATA_SIRH_PATH,
        config.DATA_SONDAGE_PATH
    )

    df = preprocess_data(df_eval, df_sirh, df_sondage)

    assert df is not None
    assert df.shape[0] > 0