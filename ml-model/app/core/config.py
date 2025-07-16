from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # Configuración de la aplicación
    DEBUG: bool = Field(True, env="DEBUG")
    API_PREFIX: str = Field("/api/v1", env="API_PREFIX")
    
    # Configuración del modelo
    MODEL_PATH: str = Field("models/dummy_model.pkl", env="MODEL_PATH")
    
    # Configuración de seguridad (opcional)
    SECRET_KEY: str = Field("your-secret-key", env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()