# app/routers/productos.py
from fastapi import APIRouter, HTTPException
from app.services.productos_service import ProductosService
from app.models.productos import ProductoInput
from app.database.bigquery import BigQueryClient
from app.config import config

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/")
async def upsert_producto(producto: ProductoInput):
    """Crea o actualiza un producto (solo datos maestros)"""
    try:
        resultado = ProductosService.upsert_producto(producto)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def listar_productos():
    """Lista todos los productos (datos maestros)"""
    try:
        query = f"""
            SELECT 
                id_producto,
                id_externo,
                codigo,
                nombre,
                descripcion,
                marca,
                categoria,
                modelo,
                precio_base,
                activo,
                stock_minimo,
                foto,
                fecha_creacion,
                fecha_actualizacion
            FROM `{config.PROJECT_ID}.{config.DATASET_ID}.productos`
            ORDER BY nombre
        """
        df = BigQueryClient.execute_query(query)
        
        # Convertir a JSON serializable
        data = []
        for _, row in df.iterrows():
            record = {}
            for col in df.columns:
                value = row[col]
                if hasattr(value, 'item'):  # numpy types
                    record[col] = value.item()
                elif isinstance(value, pd.Timestamp):
                    record[col] = value.isoformat()
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