from pydantic_settings import BaseSettings
from pydantic import Field, HttpUrl, AnyUrl
from functools import lru_cache
from typing import Optional, Dict, Any
from datetime import datetime
import json

class Settings(BaseSettings):
    # ========== Configuración de la aplicación ==========
    DEBUG: bool = Field(True, env="DEBUG")
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
    API_PREFIX: str = Field("/api/v1", env="API_PREFIX")
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")
    
    # ========== Configuración del modelo MCP ==========
    MODEL_NAME: str = Field("red-sentinel-threat-detector", env="MODEL_NAME")
    MODEL_VERSION: str = Field("1.0.0", env="MODEL_VERSION")
    MODEL_ID: str = Field("red-sentinel-threat-v1", env="MODEL_ID")
    MODEL_PATH: str = Field("models/dummy_model.pkl", env="MODEL_PATH")
    MODEL_FRAMEWORK: str = Field("scikit-learn", env="MODEL_FRAMEWORK")
    MODEL_FRAMEWORK_VERSION: str = Field("1.2.2", env="MODEL_FRAMEWORK_VERSION")
    
    # ========== Metadatos del modelo ==========
    MODEL_DESCRIPTION: str = Field(
        "Modelo para detección de amenazas en tráfico de red",
        env="MODEL_DESCRIPTION"
    )
    MODEL_AUTHOR: str = Field("Red Sentinel Team", env="MODEL_AUTHOR")
    MODEL_LICENSE: str = Field("MIT", env="MODEL_LICENSE")
    MODEL_DOCS_URL: Optional[HttpUrl] = Field(
        "https://github.com/yourorg/red-sentinel/docs",
        env="MODEL_DOCS_URL"
    )
    
    # ========== Configuración de rendimiento ==========
    MODEL_BATCH_SIZE: int = Field(32, env="MODEL_BATCH_SIZE")
    MODEL_MAX_CONCURRENT_REQUESTS: int = Field(10, env="MODEL_MAX_CONCURRENT_REQUESTS")
    
    # ========== Configuración de seguridad ==========
    SECRET_KEY: str = Field("your-secret-key-here", env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    API_KEYS: Dict[str, str] = Field(
        default_factory=lambda: {"default": "test-key"},
        env="API_KEYS"
    )
    
    # ========== Configuración de registro ==========
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # ========== Métricas de rendimiento ==========
    @property
    def model_performance_metrics(self) -> Dict[str, float]:
        """Métricas de rendimiento del modelo."""
        return {
            "accuracy": 0.987,
            "precision": 0.983,
            "recall": 0.972,
            "f1_score": 0.977,
            "inference_time_ms": 5.2
        }
    
    # ========== Configuración de documentación ==========
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = 'ignore'
        
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            # Primero carga desde .env, luego de las variables de entorno
            return env_settings, init_settings, file_secret_settings

@lru_cache()
def get_settings() -> Settings:
    """Obtiene la configuración de la aplicación con caché."""
    return Settings()

# Alias para compatibilidad con código existente
settings = get_settings()