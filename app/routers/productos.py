from fastapi import APIRouter, HTTPException, Query
from app.services.productos_service import ProductosService
from app.models.productos import ProductoInput
from app.database.bigquery import BigQueryClient
from app.config import config
from typing import Optional
import pandas as pd
from decimal import Decimal

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/")
async def upsert_producto(producto: ProductoInput):
    """
    Crea o actualiza un producto (solo datos maestros).
    
    - Si id_externo NO existe → INSERTA
    - Si id_externo YA existe → ACTUALIZA
    """
    try:
        resultado = ProductosService.upsert_producto(producto)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def listar_productos(
    activo: Optional[bool] = Query(True, description="Filtrar por estado activo"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    search: Optional[str] = Query(None, description="Buscar por nombre, SKU o código de barras")
):
    """
    Lista productos con filtros opcionales.
    """
    try:
        query = f"""
            SELECT 
                id_producto,
                id_externo,
                codigo,
                codigo_barras,
                nombre,
                descripcion,
                categoria,
                marca,
                modelo,
                precio_base,
                activo,
                stock_minimo,
                foto,
                fecha_creacion,
                fecha_actualizacion
            FROM `{config.PROJECT_ID}.{config.DATASET_ID}.productos`
            WHERE 1=1
        """
        params = {}
        
        if activo is not None:
            query += " AND activo = @activo"
            params["activo"] = activo
        
        if categoria:
            query += " AND categoria = @categoria"
            params["categoria"] = categoria
        
        if search:
            query += " AND (nombre LIKE @search OR codigo LIKE @search OR codigo_barras LIKE @search)"
            params["search"] = f"%{search}%"
        
        query += " ORDER BY nombre"
        
        df = BigQueryClient.execute_query_safe(query, **params)
        
        # 🔥 Convertir a JSON serializable (con manejo de NaN)
        data = []
        for _, row in df.iterrows():
            record = {}
            for col in df.columns:
                value = row[col]
                
                # 🔥 PRIMERO: verificar si es NaN/Null
                if pd.isna(value):
                    record[col] = None
                elif hasattr(value, 'item'):  # numpy types
                    record[col] = value.item()
                elif isinstance(value, pd.Timestamp):
                    record[col] = value.isoformat()
                elif isinstance(value, Decimal):
                    record[col] = float(value)
                else:
                    record[col] = value
            data.append(record)
        
        return {
            "status": "success",
            "total": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id_producto}")
async def get_producto(id_producto: str):
    """
    Obtiene un producto específico por su ID interno (STRING).
    """
    try:
        query = f"""
            SELECT 
                id_producto,
                id_externo,
                codigo,
                codigo_barras,
                nombre,
                descripcion,
                categoria,
                marca,
                modelo,
                precio_base,
                activo,
                stock_minimo,
                foto,
                fecha_creacion,
                fecha_actualizacion
            FROM `{config.PROJECT_ID}.{config.DATASET_ID}.productos`
            WHERE id_producto = @id_producto
        """
        df = BigQueryClient.execute_query_safe(query, id_producto=id_producto)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # 🔥 Convertir a JSON serializable (con manejo de NaN)
        row = df.iloc[0]
        record = {}
        for col in df.columns:
            value = row[col]
            
            # 🔥 PRIMERO: verificar si es NaN/Null
            if pd.isna(value):
                record[col] = None
            elif hasattr(value, 'item'):
                record[col] = value.item()
            elif isinstance(value, pd.Timestamp):
                record[col] = value.isoformat()
            elif isinstance(value, Decimal):
                record[col] = float(value)
            else:
                record[col] = value
        
        return record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))