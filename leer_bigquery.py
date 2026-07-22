from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    "credenciales/api-gitech.json"
)

client = bigquery.Client(
    credentials=credentials,
    project="proyecto-css-panama"
)

query = """
SELECT *
FROM `proyecto-css-panama.gitech.inventario`
"""

df = client.query(query).to_dataframe()

print(df)