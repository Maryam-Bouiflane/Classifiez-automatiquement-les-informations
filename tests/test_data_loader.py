import pandas as pd
import pytest
from src.data_loader import load_data

# ======================
# FIXTURE: fichiers CSV temporaires
# ======================
@pytest.fixture
def sample_csv_files(tmp_path):

    eval_path = tmp_path / "eval.csv"
    sirh_path = tmp_path / "sirh.csv"
    sondage_path = tmp_path / "sondage.csv"

    df_eval = pd.DataFrame({"col1": [1, 2]})
    df_sirh = pd.DataFrame({"col2": [3, 4]})
    df_sondage = pd.DataFrame({"col3": [5, 6]})

    df_eval.to_csv(eval_path, index=False)
    df_sirh.to_csv(sirh_path, index=False)
    df_sondage.to_csv(sondage_path, index=False)

    return eval_path, sirh_path, sondage_path


# ======================
# TEST 1: chargement OK
# ======================
def test_load_data_success(sample_csv_files):

    eval_path, sirh_path, sondage_path = sample_csv_files

    df_eval, df_sirh, df_sondage = load_data(
        eval_path, sirh_path, sondage_path
    )

    assert isinstance(df_eval, pd.DataFrame)
    assert isinstance(df_sirh, pd.DataFrame)
    assert isinstance(df_sondage, pd.DataFrame)

    assert not df_eval.empty
    assert not df_sirh.empty
    assert not df_sondage.empty


# ======================
# TEST 2: contenu correct
# ======================
def test_load_data_content(sample_csv_files):

    eval_path, sirh_path, sondage_path = sample_csv_files

    df_eval, df_sirh, df_sondage = load_data(
        eval_path, sirh_path, sondage_path
    )

    assert "col1" in df_eval.columns
    assert "col2" in df_sirh.columns
    assert "col3" in df_sondage.columns


# ======================
# TEST 3: fichier manquant
# ======================
def test_load_data_file_not_found():

    with pytest.raises(FileNotFoundError):
        load_data("fake1.csv", "fake2.csv", "fake3.csv")