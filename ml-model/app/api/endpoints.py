from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from ..services.ml_service import ml_service
from ..core.config import get_settings

router = APIRouter()
settings = get_settings()

@router.post("/analyze")
async def analyze_threat(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Endpoint para analizar amenazas de red.
    
    Ejemplo de entrada:
    {
        "source_ip": "192.168.1.1",
        "ports": [80, 443, 22],
        "timestamp": "2025-07-16T02:05:20Z"
    }
    """
    try:
        return await ml_service.analyze_threat(data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la solicitud: {str(e)}"
        )

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Verifica el estado del servicio."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Red Sentinel ML"
    }