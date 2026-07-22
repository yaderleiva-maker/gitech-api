# main.py
from fastapi import FastAPI
from app.routers import inventario
from app.config import config
from datetime import datetime

app = FastAPI(
    title=config.API_TITLE,
    version=config.API_VERSION,
    description=config.API_DESCRIPTION
)

# Incluir routers
app.include_router(inventario.router)

@app.get("/")
async def root():
    return {
        "message": f"🚀 {config.API_TITLE}",
        "version": config.API_VERSION,
        "environment": config.ENV,  # 👈 AHORA SABEMOS DÓNDE ESTAMOS
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/inventario",
            "/inventario/{id}",
            "/inventario?estado=Activo&stock_min=5",
            "/inventario/stock-bajo?limite=5"
        ]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "environment": config.ENV,
        "timestamp": datetime.now().isoformat()
    }

