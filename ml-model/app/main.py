# En app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.endpoints import router as api_router

app = FastAPI(
    title="Red Sentinel ML API",
    description="API para análisis de amenazas de red con IA",
    version=getattr(settings, "MODEL_VERSION", "0.1.0")
)

# Configuración de CORS (ajusta orígenes según tu entorno)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los endpoints MCP (ya llevan prefijo /api/v1 en el router)
app.include_router(api_router)

@app.get("/")
async def root():
    return {
        "message": "Red Sentinel ML API",
        "docs": "/docs",
        "health": "/api/v1/health"
    }