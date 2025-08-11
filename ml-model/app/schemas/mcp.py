from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, Any, List, Optional, Literal
from datetime import datetime
from enum import Enum

class ProtocolType(str, Enum):
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    OTHER = "other"

class ThreatLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ModelInput(BaseModel):
    """
    Esquema para los datos de entrada del modelo de detección de amenazas.
    Basado en el protocolo MCP (Model Context Protocol).
    """
    # Identificación
    request_id: str = Field(..., description="Identificador único de la solicitud")
    
    # Datos de la conexión
    source_ip: str = Field(..., description="Dirección IP de origen")
    source_port: Optional[int] = Field(None, description="Puerto de origen")
    destination_ip: str = Field(..., description="Dirección IP de destino")
    destination_port: int = Field(..., description="Puerto de destino")
    
    # Metadatos de la red
    protocol: ProtocolType = Field(..., description="Protocolo de red utilizado")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Marca de tiempo de la conexión")
    
    # Datos adicionales
    payload_size: Optional[int] = Field(None, description="Tamaño del payload en bytes")
    flags: Optional[Dict[str, bool]] = Field(
        None, 
        description="Banderas de protocolo (ej: SYN, ACK, etc.)"
    )
    additional_metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Metadatos adicionales de la conexión"
    )

    class Config:
        schema_extra = {
            "example": {
                "request_id": "req_123456789",
                "source_ip": "192.168.1.100",
                "source_port": 54321,
                "destination_ip": "10.0.0.1",
                "destination_port": 22,
                "protocol": "tcp",
                "timestamp": "2025-08-10T11:05:00Z",
                "payload_size": 128,
                "flags": {"SYN": True, "ACK": False},
                "additional_metadata": {"service": "ssh", "ttl": 64}
            }
        }

class ModelOutput(BaseModel):
    """
    Esquema para la salida del modelo de detección de amenazas.
    Sigue el estándar MCP para respuestas de modelos.
    """
    request_id: str = Field(..., description="Identificador único de la solicitud")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Marca de tiempo de la respuesta")
    
    # Resultados de la predicción
    prediction: int = Field(..., description="Predicción del modelo (0: normal, 1: amenaza)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Nivel de confianza de la predicción")
    risk_level: ThreatLevel = Field(..., description="Nivel de riesgo identificado")
    
    # Explicación y contexto
    explanation: str = Field(..., description="Explicación legible de la predicción")
    indicators: List[str] = Field(
        default_factory=list,
        description="Indicadores de amenaza detectados"
    )
    
    # Metadatos adicionales
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadatos adicionales de la predicción"
    )

class ModelMetadata(BaseModel):
    """
    Metadatos del modelo siguiendo el estándar MCP.
    Proporciona información sobre el modelo implementado.
    """
    # Identificación
    name: str = Field(..., description="Nombre descriptivo del modelo")
    version: str = Field(..., description="Versión del modelo (semver)")
    model_id: str = Field(..., description="Identificador único del modelo")
    
    # Información técnica
    framework: str = Field(..., description="Framework de ML utilizado")
    framework_version: str = Field(..., description="Versión del framework")
    
    # Capacidades
    input_schema: Dict[str, Any] = Field(
        ...,
        description="Esquema JSON de los datos de entrada esperados"
    )
    output_schema: Dict[str, Any] = Field(
        ...,
        description="Esquema JSON de los datos de salida generados"
    )
    
    # Metadatos descriptivos
    description: str = Field(..., description="Descripción del propósito del modelo")
    author: str = Field(..., description="Persona u organización responsable")
    license: str = Field(..., description="Licencia del modelo")
    
    # Fechas
    created_at: datetime = Field(..., description="Fecha de creación del modelo")
    last_updated: datetime = Field(..., description="Última actualización del modelo")
    
    # Métricas de rendimiento
    performance_metrics: Dict[str, float] = Field(
        default_factory=dict,
        description="Métricas de rendimiento del modelo"
    )
    
    # Documentación adicional
    documentation_url: Optional[HttpUrl] = Field(
        None,
        description="URL de documentación adicional del modelo"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Red Sentinel Threat Detector",
                "version": "1.0.0",
                "model_id": "red-sentinel-threat-v1",
                "framework": "scikit-learn",
                "framework_version": "1.2.2",
                "input_schema": ModelInput.schema(),
                "output_schema": ModelOutput.schema(),
                "description": "Modelo para detección de amenazas en tráfico de red",
                "author": "Red Sentinel Team",
                "license": "MIT",
                "created_at": "2025-01-15T00:00:00Z",
                "last_updated": "2025-08-01T00:00:00Z",
                "performance_metrics": {
                    "accuracy": 0.987,
                    "precision": 0.983,
                    "recall": 0.972,
                    "f1_score": 0.977,
                    "inference_time_ms": 5.2
                },
                "documentation_url": "https://github.com/yourorg/red-sentinel/docs"
            }
        }
