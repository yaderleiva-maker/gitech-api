import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PROJECT_ID = os.getenv("PROJECT_ID", "proyecto-css-panama")
    DATASET_ID = os.getenv("DATASET_ID", "gitech")
    TABLE_ID = os.getenv("TABLE_ID", "inventario")
    ENV = os.getenv("ENV", "development")
    BIGQUERY_LOCATION = os.getenv("BIGQUERY_LOCATION", "US")
    
    API_TITLE = "GITECH Inventory API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "API de inventario para GITECH"

config = Config()