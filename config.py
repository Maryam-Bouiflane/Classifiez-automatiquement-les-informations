DATA_EVAL_PATH = "data/extrait_eval.csv"
DATA_SIRH_PATH = "data/extrait_sirh.csv"
DATA_SONDAGE_PATH = "data/extrait_sondage.csv"

TEST_SIZE = 0.2
RANDOM_STATE = 42

PARAM_GRID = {
    "logreg__C": [0.01, 0.1, 1, 10],
    "logreg__solver": ["lbfgs", "liblinear"]
}