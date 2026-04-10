import pandas as pd
from src.data_loader import load_data
import config

def test_load_data():
    result_eval, result_sirh, result_sondage = load_data(
        config.DATA_EVAL_PATH,
        config.DATA_SIRH_PATH,
        config.DATA_SONDAGE_PATH
    )

    # Vérifie que les DataFrames sont vides
    assert not result_eval.empty
    assert not result_sirh.empty
    assert not result_sondage.empty