# main.py (versión simplificada para prueba)
from fastapi import FastAPI
from app.routers import inventario, productos
from app.config import config
from datetime import datetime

app = FastAPI(
    title="GITECH Platform API",
    version=config.API_VERSION,
    description="API de integración con BigQuery"
)

app.include_router(inventario.router)
app.include_router(productos.router)

@app.get("/")
async def root():
    return {
        "message": "🚀 GITECH Platform API",
        "version": config.API_VERSION,
        "environment": config.ENV,
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/inventario",
            "/productos"
        ]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "environment": config.ENV,
        "timestamp": datetime.now().isoformat()
    }