# Microservicio ML - Red Sentinel

Servicio de Machine Learning para el análisis de amenazas de red, desarrollado con FastAPI y Scikit-learn.

## Tabla de Contenidos
- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [API Reference](#-api-reference)
- [Desarrollo](#-desarrollo)
- [Despliegue](#-despliegue)
- [Próximos Pasos](#-próximos-pasos)
- [Licencia](#-licencia)

## Características

- **API RESTful** con documentación interactiva (Swagger/ReDoc)
- **Modelo de ML** para detección de amenazas
- **Arquitectura** modular y escalable
- **Variables de entorno** para configuración
- **Contenedor Docker** listo para producción

---

## Enfoque y Protocolo (MCP)

Este microservicio implementa el Model Context Protocol (MCP) para estandarizar:

- Esquema de entrada: `ModelInput` (tráfico de red: IPs, puertos, protocolo, timestamp, flags, metadatos).
- Esquema de salida: `ModelOutput` (predicción, confianza, nivel de riesgo, explicación, indicadores, metadatos).
- Metadatos del modelo: `ModelMetadata` (nombre, versión, framework, JSON Schemas, métricas, autor, licencia, URLs, timestamps).

Objetivo: facilitar interoperabilidad entre componentes, trazabilidad y mantenibilidad del servicio, independientemente del modelo subyacente.

Implementación:
- Esquemas MCP en `app/schemas/mcp.py` con Pydantic.
- Servicio ML en `app/services/ml_service.py` que procesa entrada, predice (modelo real o dummy), calcula confianza y riesgo, y arma explicación/indicadores.
- Endpoints FastAPI en `app/api/endpoints.py` (router con prefijo `/api/v1`).
- App principal en `app/main.py` que incluye el router MCP y CORS.

---

## Estructura del Proyecto

```
ml-model/
├─ app/
│  ├─ api/endpoints.py         # Endpoints MCP (/api/v1)
│  ├─ core/config.py           # Configuración y .env (Settings)
│  ├─ schemas/mcp.py           # Esquemas MCP (ModelInput/Output/Metadata)
│  ├─ services/ml_service.py   # Lógica de ML (carga modelo, predicción)
│  └─ main.py                  # FastAPI app, CORS, include_router
├─ models/                     # model.pkl (opcional)
├─ tests/
├─ train_dummy_model.py        # Script para generar modelo dummy
├─ requirements.txt
└─ README_ml_model.md
```

---

## Requisitos

- Python 3.10+ (recomendado)
- pip, venv

---

## Instalación

Desde la raíz `ml-model/`:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Git Bash/PowerShell (Windows)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
# (Opcional) generar modelo dummy en disco
python train_dummy_model.py
```

---

## Configuración

Archivo `.env` en la raíz (`ml-model/.env`):

```
# General
DEBUG=True
API_PREFIX=/api/v1
ENVIRONMENT=development

# Modelo
MODEL_PATH=models/dummy_model.pkl
MODEL_NAME=red-sentinel-threat-detector
MODEL_VERSION=1.0.0
MODEL_ID=red-sentinel-threat-v1
MODEL_FRAMEWORK=scikit-learn
MODEL_FRAMEWORK_VERSION=1.2.2
MODEL_DESCRIPTION=Modelo para detección de amenazas en tráfico de red
MODEL_AUTHOR=Red Sentinel Team
MODEL_LICENSE=MIT
MODEL_DOCS_URL=https://github.com/yourorg/red-sentinel/docs

# Seguridad
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API keys (opcional; si se define, se requiere una de estas claves)
# API_KEYS={"default":"test-key"}
```

Notas de autenticación:
- Si `ENVIRONMENT=development` y no se define `API_KEYS`, se permite usar `X-API-Key: dev-key` (modo dev).
- Si se define `API_KEYS`, debes enviar una key válida, p.ej. `X-API-Key: test-key`.

---

## Uso (levantar servidor)

Desde `ml-model/` con el venv activo:

```bash
python -m uvicorn app.main:app --reload
```

Documentación automática:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## API Reference (MCP)

Prefijo: `/api/v1`  |  Seguridad: Header `X-API-Key`

1) Health Check
- Método: GET
- URL: `/api/v1/health`
- Respuesta 200 (ejemplo):
```json
{
  "status": "healthy",
  "timestamp": "2025-08-11T03:24:48.707166Z",
  "version": "1.0.0",
  "service": "red-sentinel-threat-detector",
  "environment": "development",
  "uptime_seconds": 146.31
}
```

2) Metadatos del Modelo (MCP)
- Método: GET
- URL: `/api/v1/model/info`
- Headers: `X-API-Key: test-key` (o `dev-key` en modo dev)
- Respuesta 200: metadatos del modelo + `input_schema`/`output_schema` (JSON Schema MCP)

3) Analizar Amenaza (MCP)
- Método: POST
- URL: `/api/v1/analyze`
- Headers:
  - `Content-Type: application/json`
  - `X-API-Key: test-key` (o `dev-key` en modo dev)
  - `X-Request-ID: req_123456` (opcional)
- Body (ejemplo):
```json
{
  "request_id": "req_123456789",
  "source_ip": "192.168.1.100",
  "source_port": 54321,
  "destination_ip": "10.0.0.1",
  "destination_port": 22,
  "protocol": "tcp",
  "timestamp": "2025-08-10T18:00:00Z",
  "payload_size": 128,
  "flags": { "SYN": true, "ACK": false },
  "additional_metadata": { "service": "ssh", "ttl": 64 }
}
```
- Respuesta 200 (ejemplo):
```json
{
  "request_id": "req_123456789",
  "timestamp": "2025-08-11T03:34:05.110353Z",
  "prediction": 0,
  "confidence": 0.5,
  "risk_level": "low",
  "explanation": "No se detectaron amenazas en la solicitud.",
  "indicators": [],
  "metadata": {
    "inference_time_ms": 4.737,
    "model_version": "1.0.0",
    "environment": "development"
  }
}
```

Errores comunes:
- 401 Unauthorized → falta/clave inválida en `X-API-Key`.
- 422 Unprocessable Entity → validación Pydantic (ej. `protocol` inválido, timestamp mal formado).
- 500 Internal Server Error → error inesperado; revisar logs.

---

## ¿Cómo se construyeron los endpoints?

- `app/schemas/mcp.py`: define `ProtocolType`, `ThreatLevel`, `ModelInput`, `ModelOutput` y `ModelMetadata` con Pydantic. Estos modelos generan automáticamente los JSON Schemas para MCP.
- `app/services/ml_service.py`: servicio que carga el modelo desde `MODEL_PATH` (o usa un dummy si no existe), preprocesa entrada, predice y crea la respuesta MCP, calculando `risk_level`, `confidence`, `indicators` y `explanation`.
- `app/api/endpoints.py`: router FastAPI (`APIRouter`) con prefijo `/api/v1`. Implementa:
  - `POST /analyze` → recibe `ModelInput`, invoca el servicio y retorna `ModelOutput`.
  - `GET /health` → estado del servicio con uptime.
  - `GET /model/info` → devuelve `ModelMetadata` actualizado.
  Incluye dependencia `get_api_key` que valida el header `X-API-Key` según la config.
- `app/main.py`: instancia `FastAPI`, configura CORS, incluye el router MCP y expone `/` como endpoint raíz informativo.

Decisiones clave:
- Prefijo `/api/v1` para versionado claro.
- Esquemas MCP separados para compatibilidad e interoperabilidad.
- Autenticación sencilla por API key para entornos de desarrollo/pruebas.
- Logging y trazabilidad con `X-Request-ID` y tareas en background de ejemplo.

---

## Pruebas rápidas (cURL)

```bash
# Health
curl -X GET "http://127.0.0.1:8000/api/v1/health"

# Model info
curl -X GET "http://127.0.0.1:8000/api/v1/model/info" \
  -H "X-API-Key: test-key"

# Analyze
curl -X POST "http://127.0.0.1:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-key" \
  -d '{
    "request_id":"req_123456789",
    "source_ip":"192.168.1.100",
    "source_port":54321,
    "destination_ip":"10.0.0.1",
    "destination_port":22,
    "protocol":"tcp",
    "timestamp":"2025-08-10T18:00:00Z",
    "payload_size":128,
    "flags":{"SYN":true,"ACK":false},
    "additional_metadata":{"service":"ssh","ttl":64}
  }'
```

---

## Desarrollo

- Ejecutar con autoreload (`--reload`).
- Añadir pruebas en `tests/` (unitarias e integración).
- Instrumentación futura: Prometheus/OpenTelemetry, logs estructurados y tracing distribuido.

---

## Despliegue

- Variables sensibles via `.env`/secret manager.
- Ejecutar con workers (ej. `uvicorn --workers 2` detrás de un reverse proxy).
- Endurecer CORS y seguridad.

---

## Próximos Pasos

- Integrar un modelo real (pipeline de features y persistencia de artefactos).
- Rate limiting, CORS restrictivo y claves rotativas.
- Colección Postman y CI/CD para pruebas automáticas.
- Métricas de negocio y dashboards.

---

## Licencia

MIT