"""
Servicio de Machine Learning para detección de amenazas en tráfico de red.
Implementa el Model Context Protocol (MCP) para estandarizar las entradas/salidas.
"""
import json
import logging
import joblib
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

# Importaciones locales
from ..core.config import settings
from ..schemas.mcp import ModelInput, ModelOutput, ModelMetadata, ThreatLevel

# Configuración de logging
logger = logging.getLogger(__name__)

class MLService:
    """
    Servicio para el modelo de detección de amenazas.
    Implementa el Model Context Protocol (MCP) para estandarizar las operaciones.
    """
    
    def __init__(self):
        """Inicializa el servicio cargando el modelo y metadatos."""
        self.model = self._load_model()
        self.metadata = self._create_model_metadata()
        logger.info(f"Servicio ML inicializado con modelo: {self.metadata.name} v{self.metadata.version}")
    
    def _load_model(self):
        """Carga el modelo desde la ruta especificada en la configuración."""
        try:
            model_path = Path(settings.MODEL_PATH)
            if not model_path.exists():
                logger.warning(f"Modelo no encontrado en {model_path.absolute()}, usando modelo dummy")
                return self._create_dummy_model()
                
            logger.info(f"Cargando modelo desde {model_path.absolute()}")
            model = joblib.load(model_path)
            logger.info("Modelo cargado exitosamente")
            return model
            
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {str(e)}", exc_info=True)
            logger.info("Usando modelo dummy como respaldo")
            return self._create_dummy_model()
    
    def _create_dummy_model(self):
        """Crea un modelo dummy para desarrollo y pruebas."""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import make_classification
        
        # Generar datos de ejemplo para el modelo dummy
        X, y = make_classification(
            n_samples=100, 
            n_features=10, 
            n_classes=2, 
            random_state=42
        )
        
        # Entrenar un modelo simple
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        logger.info("Modelo dummy creado exitosamente")
        return model
    
    def _create_model_metadata(self) -> ModelMetadata:
        """Crea los metadatos del modelo según el estándar MCP."""
        from ..schemas.mcp import ModelInput, ModelOutput
        
        return ModelMetadata(
            name=settings.MODEL_NAME,
            version=settings.MODEL_VERSION,
            model_id=settings.MODEL_ID,
            framework=settings.MODEL_FRAMEWORK,
            framework_version=settings.MODEL_FRAMEWORK_VERSION,
            input_schema=ModelInput.schema(),
            output_schema=ModelOutput.schema(),
            description=settings.MODEL_DESCRIPTION,
            author=settings.MODEL_AUTHOR,
            license=settings.MODEL_LICENSE,
            created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
            last_updated=datetime.now(timezone.utc),
            performance_metrics=settings.model_performance_metrics,
            documentation_url=settings.MODEL_DOCS_URL
        )
    
    async def analyze_threat(self, input_data: ModelInput) -> ModelOutput:
        """
        Analiza una solicitud de red en busca de amenazas.
        
        Args:
            input_data: Datos de entrada según el esquema ModelInput
            
        Returns:
            ModelOutput: Resultado del análisis con predicción y metadatos
        """
        try:
            logger.info(f"Analizando solicitud {input_data.request_id}")
            start_time = datetime.now(timezone.utc)
            
            # Preprocesar los datos de entrada
            features = self._preprocess_input(input_data)
            
            # Realizar la predicción
            prediction, confidence = self._predict(features)
            
            # Determinar el nivel de amenaza
            risk_level = self._determine_risk_level(prediction, confidence)
            
            # Generar explicación
            explanation, indicators = self._generate_explanation(
                input_data, 
                prediction, 
                confidence, 
                risk_level
            )
            
            # Calcular tiempo de inferencia
            inference_time_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            
            logger.info(f"Análisis completado en {inference_time_ms:.2f}ms - Predicción: {prediction} (Confianza: {confidence:.2f})")
            
            # Crear y retornar la respuesta
            return ModelOutput(
                request_id=input_data.request_id,
                timestamp=datetime.now(timezone.utc),
                prediction=prediction,
                confidence=float(confidence),
                risk_level=risk_level,
                explanation=explanation,
                indicators=indicators,
                metadata={
                    "inference_time_ms": inference_time_ms,
                    "model_version": self.metadata.version,
                    "environment": settings.ENVIRONMENT
                }
            )
            
        except Exception as e:
            logger.error(f"Error en analyze_threat: {str(e)}", exc_info=True)
            raise
    
    def _preprocess_input(self, input_data: ModelInput) -> np.ndarray:
        """
        Preprocesa los datos de entrada para el modelo.
        
        Args:
            input_data: Datos de entrada según el esquema ModelInput
            
        Returns:
            np.ndarray: Características procesadas para el modelo
        """
        # TODO: Implementar preprocesamiento específico según las necesidades del modelo
        # Este es un ejemplo básico que debe adaptarse al modelo real
        
        # Convertir datos categóricos a numéricos
        protocol_map = {"tcp": 0, "udp": 1, "icmp": 2, "other": 3}
        
        # Extraer características básicas
        features = [
            input_data.source_port or 0,
            input_data.destination_port,
            protocol_map.get(input_data.protocol.value.lower(), 3),
            input_data.payload_size or 0,
            # Agregar más características según sea necesario
        ]
        
        # Agregar flags binarios si existen
        if input_data.flags:
            flags = [
                int(input_data.flags.get("SYN", False)),
                int(input_data.flags.get("ACK", False)),
                int(input_data.flags.get("FIN", False)),
                int(input_data.flags.get("RST", False)),
                int(input_data.flags.get("PSH", False)),
                int(input_data.flags.get("URG", False))
            ]
            features.extend(flags)
        
        return np.array([features])
    
    def _predict(self, features: np.ndarray) -> tuple[int, float]:
        """
        Realiza la predicción con el modelo.
        
        Args:
            features: Características de entrada ya preprocesadas
            
        Returns:
            tuple: (predicción, confianza)
        """
        try:
            # Realizar predicción
            prediction = self.model.predict(features)[0]
            
            # Obtener probabilidades (si el modelo lo soporta)
            if hasattr(self.model, "predict_proba"):
                proba = self.model.predict_proba(features)[0]
                confidence = float(max(proba))
            else:
                confidence = 1.0  # Valor por defecto si no hay probabilidades
                
            return int(prediction), confidence
            
        except Exception as e:
            logger.error(f"Error en la predicción: {str(e)}", exc_info=True)
            # En caso de error, retornar predicción segura (sin amenaza)
            return 0, 0.5
    
    def _determine_risk_level(self, prediction: int, confidence: float) -> ThreatLevel:
        """
        Determina el nivel de riesgo basado en la predicción y confianza.
        
        Args:
            prediction: 0 (normal) o 1 (amenaza)
            confidence: Nivel de confianza de la predicción (0-1)
            
        Returns:
            ThreatLevel: Nivel de riesgo determinado
        """
        if prediction == 0:
            return ThreatLevel.LOW
        
        # Si es una amenaza, determinar nivel basado en la confianza
        if confidence >= 0.9:
            return ThreatLevel.CRITICAL
        elif confidence >= 0.7:
            return ThreatLevel.HIGH
        else:
            return ThreatLevel.MEDIUM
    
    def _generate_explanation(
        self, 
        input_data: ModelInput, 
        prediction: int, 
        confidence: float, 
        risk_level: ThreatLevel
    ) -> tuple[str, List[str]]:
        """
        Genera una explicación legible de la predicción.
        
        Args:
            input_data: Datos de entrada originales
            prediction: Predicción del modelo (0 o 1)
            confidence: Nivel de confianza de la predicción
            risk_level: Nivel de riesgo determinado
            
        Returns:
            tuple: (explicación, lista de indicadores)
        """
        indicators = []
        
        # Explicación base según la predicción
        if prediction == 0:
            explanation = "No se detectaron amenazas en la solicitud."
        else:
            explanation = (
                f"Se detectó una posible amenaza de nivel {risk_level.value.upper()}. "
                f"Confianza del modelo: {confidence*100:.1f}%."
            )
            
            # Añadir indicadores específicos
            if input_data.destination_port in [22, 23, 3389]:
                indicators.append(f"Conexión a servicio de administración remota (puerto {input_data.destination_port})")
                
            if input_data.flags and input_data.flags.get("SYN") and not input_data.flags.get("ACK"):
                indicators.append("Paquete SYN sin ACK (posible escaneo de puertos)")
                
            if input_data.payload_size and input_data.payload_size > 1000:
                indicators.append(f"Tamaño de paquete inusualmente grande: {input_data.payload_size} bytes")
        
        # Si no hay indicadores específicos, usar uno genérico
        if prediction == 1 and not indicators:
            indicators.append("Patrón de tráfico inusual detectado por el modelo")
        
        return explanation, indicators
    
    async def get_model_info(self) -> ModelMetadata:
        """
        Obtiene los metadatos del modelo según el estándar MCP.
        
        Returns:
            ModelMetadata: Metadatos actualizados del modelo
        """
        # Actualizar la marca de tiempo de última actualización
        self.metadata.last_updated = datetime.now(timezone.utc)
        return self.metadata

# Instancia global del servicio
ml_service = MLService()