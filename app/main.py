from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import inventario, productos
from app.config import config
from datetime import datetime
import traceback

app = FastAPI(
    title="GITECH Platform API",
    version=config.API_VERSION,
    description="API de integración con BigQuery"
)

# 🔥 Manejador de excepciones para debug
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "traceback": traceback.format_exc()
        }
    )

# Registrar routers
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