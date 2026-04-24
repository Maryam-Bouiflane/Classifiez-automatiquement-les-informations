import pandas as pd
from huggingface_hub import HfApi
import os

def upload_dataset_to_hf():

    api = HfApi(token=os.environ["HF_TOKEN"])

    # upload dataset
    api.upload_file(
        path_or_fileobj="data/clean/final_dataset.csv",
        path_in_repo="data/final_dataset.csv",
        repo_id="maryamb123/p4-classification-app",
        repo_type="space"
    )

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
    
    # Sauvegarde du dataset final
    df.to_csv("data/clean/final_dataset.csv", index=False)  # Sauvegarde locale du dataset final
    # upload_dataset_to_hf()
    
    return df