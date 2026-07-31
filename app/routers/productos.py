from fastapi import APIRouter, HTTPException, status
from app.services.productos_service import ProductosService
from app.models.productos import ProductoInput

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/")
async def upsert_producto(producto: ProductoInput):
    """
    Sincroniza un producto desde el sistema web.
    
    - Si id_externo NO existe → INSERTA
    - Si id_externo YA existe → ACTUALIZA
    """
    try:
        resultado = ProductosService.upsert_producto(producto)
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/")
async def listar_productos(
    activo: Optional[bool] = True,
    categoria: Optional[str] = None,
    min_stock: Optional[int] = None
):
    """Lista productos con filtros opcionales."""
    from app.database.bigquery import BigQueryClient
    from app.config import config
    
    try:
        query = f"""
            SELECT * FROM `{config.PROJECT_ID}.{config.DATASET_ID}.productos`
            WHERE 1=1
        """
        params = {}
        
        if activo is not None:
            query += " AND activo = @activo"
            params["activo"] = activo
        
        if categoria:
            query += " AND categoria = @categoria"
            params["categoria"] = categoria
        
        if min_stock is not None:
            query += " AND existencia < @min_stock"
            params["min_stock"] = min_stock
        
        query += " ORDER BY nombre_prod"
        
        df = BigQueryClient.execute_query_safe(query, **params)
        return {
            "status": "success",
            "total": len(df),
            "data": df.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
