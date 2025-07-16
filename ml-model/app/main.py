# En app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .services.ml_service import ml_service  # Importa el servicio

app = FastAPI(
    title="Red Sentinel ML API",
    description="API para análisis de amenazas de red con IA",
    version="0.1.0"
)

# ... (resto de la configuración)

@app.post("/analyze")
async def analyze(data: dict):
    """Endpoint para análisis de amenazas."""
    return await ml_service.analyze_threat(data)

# ... (resto de los endpoints)