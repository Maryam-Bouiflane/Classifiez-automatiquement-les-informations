import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def build_features(df):
    X = df.drop(columns=["a_quitte_l_entreprise", "id_employee"], errors='ignore')
    y = df["a_quitte_l_entreprise"]

    df_cat = X.select_dtypes(exclude='number')
    df_num = X.select_dtypes(include='number')
    df_num = df_num.drop(columns=['niveau_hierarchique_poste', 'revenu_mensuel'], errors='ignore')

    ohe = OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False)

    X_cat = pd.DataFrame(
        ohe.fit_transform(df_cat),
        columns=ohe.get_feature_names_out(df_cat.columns),
        index=df_cat.index
    )

    X = pd.concat([df_num, X_cat], axis=1)

    return X, y, ohe