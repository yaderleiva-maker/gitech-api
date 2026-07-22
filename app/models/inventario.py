from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Producto(BaseModel):
    id: int
    sku: str
    producto: str
    stock: int
    precio: float
    estado: str
    
    class Config:
        from_attributes = True

class InventarioResponse(BaseModel):
    status: str
    total: int
    timestamp: datetime
    data: List[Producto]

class ProductoUpdate(BaseModel):
    stock: Optional[int] = None
    precio: Optional[float] = None
    estado: Optional[str] = None