from app.database.bigquery import BigQueryClient
from app.config import config
from typing import Optional
import pandas as pd

class InventarioService:
    
    @staticmethod
    def get_all():
        query = f"""
            SELECT id, sku, producto, stock, precio, estado
            FROM `{config.PROJECT_ID}.{config.DATASET_ID}.{config.TABLE_ID}`
            ORDER BY id
        """
        return BigQueryClient.execute_query(query)
    
    @staticmethod
    def get_by_id(producto_id: int):
        query = f"""
            SELECT id, sku, producto, stock, precio, estado
            FROM `{config.PROJECT_ID}.{config.DATASET_ID}.{config.TABLE_ID}`
            WHERE id = @id
        """
        df = BigQueryClient.execute_query_safe(query, id=producto_id)
        return df.iloc[0].to_dict() if not df.empty else None
    
    @staticmethod
    def filter_by(
        estado: Optional[str] = None,
        stock_min: Optional[int] = None,
        stock_max: Optional[int] = None
    ):
        query = f"""
            SELECT id, sku, producto, stock, precio, estado
            FROM `{config.PROJECT_ID}.{config.DATASET_ID}.{config.TABLE_ID}`
            WHERE 1=1
        """
        params = {}
        
        if estado:
            query += " AND UPPER(estado) = UPPER(@estado)"
            params["estado"] = estado
        
        if stock_min is not None:
            query += " AND stock >= @stock_min"
            params["stock_min"] = stock_min
        
        if stock_max is not None:
            query += " AND stock <= @stock_max"
            params["stock_max"] = stock_max
        
        query += " ORDER BY id"
        
        df = BigQueryClient.execute_query_safe(query, **params)
        return df
    
    @staticmethod
    def get_stock_bajo(limite: int = 5):
        query = f"""
            SELECT id, sku, producto, stock, precio, estado
            FROM `{config.PROJECT_ID}.{config.DATASET_ID}.{config.TABLE_ID}`
            WHERE stock < @limite
            ORDER BY stock ASC
        """
        df = BigQueryClient.execute_query_safe(query, limite=limite)
        return df