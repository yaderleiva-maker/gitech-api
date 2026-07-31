# app/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# 🔥 Forzar la carga del .env desde la raíz del proyecto
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    def __init__(self):
        self.PROJECT_ID = os.getenv("PROJECT_ID", "proyecto-css-panama")
        self.DATASET_ID = os.getenv("DATASET_ID", "gitech")
        self.TABLE_ID = os.getenv("TABLE_ID", "inventario")
        self.ENV = os.getenv("ENV", "development")
        self.BIGQUERY_LOCATION = os.getenv("BIGQUERY_LOCATION", "US")
        self.API_TITLE = "GITECH Platform API"
        self.API_VERSION = "1.0.0"
        self.API_DESCRIPTION = "API de integración con BigQuery"

config = Config()