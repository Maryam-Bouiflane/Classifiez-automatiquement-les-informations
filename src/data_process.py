import pandas as pd

def preprocess_data(df_eval, df_sirh, df_sondage):

    df_eval['augementation_salaire_precedente'] = (
        df_eval['augementation_salaire_precedente']
        .str.replace('%', '', regex=False)
        .str.strip()
        .astype(float)
    )

    df_eval['eval_number'] = (
        df_eval['eval_number']
        .astype(str)
        .str.rsplit('_', n=1)
        .str[-1]
    )

    df_eval['eval_number'] = pd.to_numeric(df_eval['eval_number'], errors='coerce')

    df_sirh = df_sirh.drop(columns=["nombre_heures_travailless"], errors='ignore')
    df_sondage = df_sondage.drop(
        columns=["nombre_employee_sous_responsabilite", "ayant_enfants"],
        errors='ignore'
    )

    df = df_sirh.merge(df_eval, left_on="id_employee", right_on="eval_number", how="left")
    df = df.merge(df_sondage, left_on="id_employee", right_on="code_sondage", how="left")

    df['a_quitte_l_entreprise'] = df['a_quitte_l_entreprise'].map({'Oui': 1, 'Non': 0})

    df = df.drop(columns=["eval_number", "code_sondage", "niveau_hierarchique_poste", "revenu_mensuel"], errors='ignore')
    df.to_csv("data/clean/final_dataset.csv", index=False)  # Sauvegarde du dataset final
    
    return df