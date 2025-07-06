from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .model_utils import analyze_threat

app = FastAPI(
    title="Red Sentinel ML API",
    description="API para análisis de amenazas de red con IA",
    version="0.1.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(data: dict):
    """
    Endpoint para analizar amenazas de red
    """
    try:
        result = analyze_threat(data)
        return {
            "success": True,
            "data": result,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {"status": "healthy", "version": "0.1.0"}