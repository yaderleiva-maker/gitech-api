import os  # 🔥 ESTO ES IMPORTANTE
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.PROJECT_ID = os.getenv("PROJECT_ID", "proyecto-css-panama")
        self.DATASET_ID = os.getenv("DATASET_ID", "gitech")
        self.TABLE_ID = os.getenv("TABLE_ID", "inventario")
        self.ENV = os.getenv("ENV", "development")
        self.BIGQUERY_LOCATION = os.getenv("BIGQUERY_LOCATION", "US")
        
        self.API_TITLE = "GITECH Inventory API"
        self.API_VERSION = "1.0.0"
        self.API_DESCRIPTION = "API de inventario para GITECH"

# 🔥 Instancia global
config = Config()