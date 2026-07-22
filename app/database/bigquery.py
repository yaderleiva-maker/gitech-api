from google.cloud import bigquery
from app.config import config
import pandas as pd

class BigQueryClient:
    _client = None
    
    @classmethod
    def get_client(cls):
        if cls._client is None:
            try:
                client = bigquery.Client(project=config.PROJECT_ID)
                client.query("SELECT 1").result()
                print(f"✅ BigQuery conectado: {config.PROJECT_ID} ({config.ENV})")
                cls._client = client
                return client
            except Exception as e:
                print(f"❌ Error conectando a BigQuery: {e}")
                raise
        return cls._client
    
    @classmethod
    def execute_query(cls, query, params=None):
        client = cls.get_client()
        
        if params:
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(key, value["type"], value["value"])
                    for key, value in params.items()
                ]
            )
            result = client.query(query, job_config=job_config)
        else:
            result = client.query(query)
        
        return result.to_dataframe()
    
    @classmethod
    def execute_query_safe(cls, query, **kwargs):
        params = {}
        for key, value in kwargs.items():
            if isinstance(value, int):
                param_type = "INT64"
            elif isinstance(value, float):
                param_type = "FLOAT64"
            elif isinstance(value, bool):
                param_type = "BOOL"
            else:
                param_type = "STRING"
            
            params[key] = {"type": param_type, "value": value}
        
        return cls.execute_query(query, params)