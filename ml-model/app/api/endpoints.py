"""
Endpoints de la API para el servicio de detección de amenazas.
Implementa el Model Context Protocol (MCP) para estandarizar las operaciones.
"""
import logging
from typing import Dict, Any, List, Optional
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends, 
    status,
    Request,
    Security,
    BackgroundTasks
)
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Importaciones locales
from ..services.ml_service import ml_service
from ..schemas.mcp import ModelInput, ModelOutput, ModelMetadata, ThreatLevel, ProtocolType
from ..core.config import settings

# Configuración de logging
logger = logging.getLogger(__name__)

# Configuración de seguridad
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Router principal
router = APIRouter(
    prefix="/api/v1",
    tags=["threat-detection"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "API key faltante o inválida"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Error interno del servidor"}
    },
)

# Modelos de respuesta
class HealthCheckResponse(BaseModel):
    """Modelo de respuesta para el endpoint de salud."""
    status: str = Field(..., description="Estado del servicio")
    timestamp: datetime = Field(..., description="Marca de tiempo de la respuesta")
    version: str = Field(..., description="Versión de la API")
    service: str = Field(..., description="Nombre del servicio")
    environment: str = Field(..., description="Entorno de ejecución")
    uptime_seconds: float = Field(..., description="Tiempo de actividad en segundos")

class ErrorResponse(BaseModel):
    """Modelo de respuesta para errores."""
    error: str = Field(..., description="Mensaje de error")
    code: int = Field(..., description="Código de error")
    request_id: str = Field(..., description="ID de la solicitud")
    timestamp: datetime = Field(..., description="Marca de tiempo del error")

# Variables globales
STARTUP_TIME = datetime.now(timezone.utc)

# Dependencias de autenticación
def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """Valida la API key proporcionada en el header."""
    if settings.ENVIRONMENT == "development" and not settings.API_KEYS:
        return "dev-key"
        
    if not api_key_header or api_key_header not in settings.API_KEYS.values():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida o faltante"
        )
    return api_key_header

# Endpoints
@router.post(
    "/analyze",
    response_model=ModelOutput,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Análisis completado exitosamente"},
        status.HTTP_400_BAD_REQUEST: {"description": "Datos de entrada inválidos"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Error de validación de datos"},
    },
    summary="Analiza una solicitud de red en busca de amenazas",
    description="""
    Este endpoint analiza una solicitud de red utilizando el modelo de IA entrenado
    y devuelve un análisis de amenazas con un nivel de confianza.
    
    **Ejemplo de solicitud:**
    ```json
    {
        "request_id": "req_123456789",
        "source_ip": "192.168.1.100",
        "source_port": 54321,
        "destination_ip": "10.0.0.1",
        "destination_port": 22,
        "protocol": "tcp",
        "timestamp": "2025-08-10T11:05:00Z",
        "payload_size": 128,
        "flags": {"SYN": true, "ACK": false},
        "additional_metadata": {"service": "ssh", "ttl": 64}
    }
    """
)
async def analyze_threat(
    request: Request,
    input_data: ModelInput,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key)
) -> ModelOutput:
    """
    Analiza una solicitud de red en busca de patrones de amenaza.
    
    Args:
        request: Objeto de solicitud HTTP
        input_data: Datos de entrada según el esquema ModelInput
        background_tasks: Tareas en segundo plano
        api_key: API key del cliente
        
    Returns:
        ModelOutput: Resultado del análisis con predicción y metadatos
    """
    # Registrar la solicitud
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    logger.info(f"Nueva solicitud de análisis - ID: {request_id}")
    
    try:
        # Validar y procesar la solicitud
        if not input_data.request_id:
            input_data.request_id = request_id
            
        # Registrar la tarea en segundo plano (ejemplo: para análisis posteriores)
        background_tasks.add_task(
            log_analysis_request,
            request_id=request_id,
            client_ip=request.client.host if request.client else "unknown",
            input_data=input_data
        )
        
        # Procesar la solicitud
        result = await ml_service.analyze_threat(input_data)
        
        # Registrar resultado exitoso
        logger.info(f"Análisis completado - ID: {request_id}, Predicción: {result.prediction}")
        
        return result
        
    except HTTPException:
        # Re-lanzar excepciones HTTP existentes
        raise
        
    except Exception as e:
        # Registrar el error
        error_msg = f"Error al procesar la solicitud: {str(e)}"
        logger.error(f"{error_msg} - ID: {request_id}", exc_info=True)
        
        # Devolver error 500 con formato estándar
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg
        )

@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Verifica el estado del servicio",
    description="""
    Este endpoint verifica el estado del servicio y devuelve información básica
    sobre su estado operativo.
    """
)
async def health_check() -> HealthCheckResponse:
    """
    Verifica el estado del servicio.
    
    Returns:
        HealthCheckResponse: Estado actual del servicio
    """
    uptime = (datetime.now(timezone.utc) - STARTUP_TIME).total_seconds()
    
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        version=settings.MODEL_VERSION,
        service=settings.MODEL_NAME,
        environment=settings.ENVIRONMENT,
        uptime_seconds=round(uptime, 2)
    )

@router.get(
    "/model/info",
    response_model=ModelMetadata,
    status_code=status.HTTP_200_OK,
    summary="Obtiene información del modelo",
    description="""
    Devuelve información detallada sobre el modelo implementado,
    incluyendo su versión, esquemas de entrada/salida y métricas de rendimiento.
    """
)
async def get_model_info() -> ModelMetadata:
    """
    Obtiene los metadatos del modelo según el estándar MCP.
    
    Returns:
        ModelMetadata: Metadatos actualizados del modelo
    """
    return await ml_service.get_model_info()

# Funciones de utilidad
async def log_analysis_request(
    request_id: str, 
    client_ip: str, 
    input_data: ModelInput
) -> None:
    """
    Registra información sobre la solicitud de análisis.
    
    Args:
        request_id: ID único de la solicitud
        client_ip: Dirección IP del cliente
        input_data: Datos de entrada de la solicitud
    """
    # En una implementación real, esto podría guardar en una base de datos
    # o enviar a un servicio de logging
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "client_ip": client_ip,
        "source_ip": input_data.source_ip,
        "destination_port": input_data.destination_port,
        "protocol": input_data.protocol.value
    }
    
    logger.info(f"Registro de análisis: {log_entry}")

# Nota: Manejadores de errores globales deben registrarse en app, no en router.