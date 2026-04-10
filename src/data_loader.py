import pandas as pd

def load_data(path_eval, path_sirh, path_sondage):
    df_eval = pd.read_csv(path_eval)
    df_sirh = pd.read_csv(path_sirh)
    df_sondage = pd.read_csv(path_sondage)
    return df_eval, df_sirh, df_sondage