# app/models/productos.py
from pydantic import BaseModel, Field
from typing import Optional

class ProductoInput(BaseModel):
    """Modelo para recibir productos desde el sistema web"""
    
    # 🔗 Identificadores
    id_externo: str = Field(..., description="ID del producto en el sistema web (STRING)")
    codigo: str = Field(..., description="SKU interno del producto")
    codigo_barras: Optional[str] = Field(None, description="Código de barras EAN/UPC")
    
    # 📦 Datos maestros
    nombre: str = Field(..., description="Nombre del producto")
    descripcion: Optional[str] = Field(None, description="Descripción del producto")
    
    # 🏷️ Categorización
    categoria: Optional[str] = Field(None, description="Categoría")
    marca: Optional[str] = Field(None, description="Marca")
    modelo: Optional[str] = Field(None, description="Modelo")
    
    # 💰 Precios
    precio_base: float = Field(0.0, description="Precio base (NUMERIC en BigQuery)")
    
    # 📊 Control
    activo: bool = Field(True, description="¿Está activo?")
    stock_minimo: int = Field(0, description="Stock mínimo para alerta")
    
    # 🖼️ Imagen
    foto: Optional[str] = Field(None, description="URL de la foto")