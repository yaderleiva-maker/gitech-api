from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
from app.services.inventario_service import InventarioService
from app.models.inventario import InventarioResponse, Producto

# 🔥 ESTO ES LO QUE FALTABA
router = APIRouter(prefix="/inventario", tags=["Inventario"])

@router.get("/", response_model=InventarioResponse)
async def get_inventario(
    estado: Optional[str] = Query(None, description="Filtrar por estado (Activo/Inactivo)"),
    stock_min: Optional[int] = Query(None, description="Stock mínimo"),
    stock_max: Optional[int] = Query(None, description="Stock máximo")
):
    try:
        if estado or stock_min is not None or stock_max is not None:
            df = InventarioService.filter_by(estado, stock_min, stock_max)
        else:
            df = InventarioService.get_all()
        
        data = df.to_dict(orient='records')
        
        return InventarioResponse(
            status="success",
            total=len(data),
            timestamp=datetime.now(),
            data=[Producto(**item) for item in data]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{producto_id}")
async def get_producto(producto_id: int):
    try:
        producto = InventarioService.get_by_id(producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stock-bajo")
async def stock_bajo(
    limite: int = Query(5, description="Límite de stock para alerta")
):
    try:
        df = InventarioService.get_stock_bajo(limite)
        return {
            "status": "success",
            "total": len(df),
            "alerta": len(df) > 0,
            "limite": limite,
            "data": df.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))