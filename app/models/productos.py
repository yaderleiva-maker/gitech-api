from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductoInput(BaseModel):
    """Modelo que espera recibir desde el sistema web"""
    
    # 🔗 Datos del sistema externo
    id_externo: int = Field(..., description="ID del producto en el sistema web")
    
    # 📦 Datos del producto
    nombre_prod: str = Field(..., description="Nombre del producto")
    descripcion: Optional[str] = Field(None, description="Descripción del producto")
    precio_base: float = Field(0.0, description="Precio base sugerido")
    activo: bool = Field(True, description="¿Está activo?")
    min_stock: int = Field(0, description="Stock mínimo de alerta")
    categoria: Optional[str] = Field(None, description="Categoría")
    marca: Optional[str] = Field(None, description="Marca")
    modelo: Optional[str] = Field(None, description="Modelo")
    foto: Optional[str] = Field(None, description="URL de la foto")
    
    # 📊 Campos calculados
    total_compras: int = Field(0, description="Total de unidades compradas")
    total_ventas: int = Field(0, description="Total de unidades vendidas")
