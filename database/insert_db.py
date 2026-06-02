from fastapi import Path
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("API_USER")
password = os.getenv("API_USER_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
DB_URL = f"postgresql://{user}:{password}@{host}:{port}/churn_db"

# Connexion à la base
engine = create_engine(DB_URL)

# Charger le dataset
df = pd.read_csv("data/clean/final_dataset.csv").drop(columns=["a_quitte_l_entreprise"])

# Injection dans la base
df.to_sql("employees", engine, if_exists="append", index=False)

print("Data inserted successfully")