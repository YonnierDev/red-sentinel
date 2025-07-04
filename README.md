# 🛡️ Red Sentinel

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)  
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)  
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)

**Red Sentinel** es un sistema inteligente de monitoreo de red que detecta patrones de escaneo sospechosos, predice su nivel de riesgo mediante IA y sugiere acciones de mitigación en tiempo real.

---

## 🚀 Características Principales

- 🔍 **Detección Avanzada**: Identifica patrones de escaneo tipo Nmap  
- 🧠 **IA Integrada**: Clasificación de amenazas con modelos de ML  
- 📊 **Dashboard en Tiempo Real**: Visualización interactiva de amenazas  
- 🛡️ **Acciones Automáticas**: Recomendaciones de mitigación  
- 📱 **Acceso Móvil**: Monitoreo desde cualquier lugar  

---

## 🏗️ Arquitectura

```mermaid
graph TD
    A[Frontend React] <--> B[Backend Node.js]
    B <--> C[Modelo ML Python (FastAPI)]
    D[Dispositivos de Red] -->|Envía logs| B
    B -->|Alertas| E[Dashboard]
    B -->|Notificaciones| F[App Móvil]
📦 Stack Tecnológico
Backend: Node.js + Express + TypeScript

IA/ML: Python + FastAPI + Scikit-learn / TensorFlow

Frontend: React + TailwindCSS + TypeScript

Mobile: Android Studio (Java) / Flutter

Base de Datos: MongoDB / PostgreSQL

Despliegue: Vercel, Docker, GitHub Actions

📡 API (v1)
GET /api/health
Verifica el estado del servicio y el entorno de ejecución.

json
Copiar
Editar
{
  "status": "operational",
  "service": "Red Sentinel API",
  "version": "1.0.0",
  "uptime": "207.69 seconds",
  "timestamp": "2025-07-04T04:29:19.105Z",
  "environment": "development",
  "checks": {
    "database": "connected",
    "memoryUsage": "8.83 MB",
    "status": "ok"
  }
}
POST /api/nmap
Envía datos simulados o reales de escaneo de red para evaluar riesgo.

Request Body

json
Copiar
Editar
{
  "ip": "192.168.1.1",
  "puerto": 22,
  "tiempo": "2025-07-04T04:59:00Z",
  "tipo": "SYN"
}
Response

json
Copiar
Editar
{
  "success": true,
  "data": {
    "riskLevel": "MEDIUM",
    "description": "Escaneo detectado desde 192.168.1.1",
    "detectedPatterns": [
      "Tipo de escaneo avanzado detectado"
    ],
    "recommendedAction": "Monitorear IP de origen"
  },
  "isThreat": false,
  "timestamp": "2025-07-04T05:04:08.343Z"
}
🧠 Inteligencia Artificial
El microservicio en Python (FastAPI):

Recibe datos del escaneo de red.

Procesa el evento con un modelo de machine learning.

Clasifica el nivel de riesgo (LOW, MEDIUM, HIGH).

Responde con recomendaciones automáticas según el contexto.

🗺️ Roadmap
 Backend Express funcional con endpoints /health y /nmap

 Microservicio IA con FastAPI

 Entrenar modelo de clasificación con logs reales o simulados

 Crear dashboard web con React para visualizar actividad

 App Android o Flutter para recibir alertas

 Dockerizar servicios para producción

 Agregar autenticación con JWT

 Automatizar todo con GitHub Actions (CI/CD)

🎯 Objetivo del Proyecto
Red Sentinel nace como una solución técnica y educativa para acercar la ciberseguridad inteligente a entornos reales, especialmente en países en desarrollo. El objetivo: detectar, visualizar y reaccionar ante amenazas, con herramientas open source, IA y una arquitectura moderna.

💬 Visión Personal
“La IA no reemplaza desarrolladores, potencia su impacto. Desde Colombia, quiero construir soluciones tecnológicas con propósito, entendiendo los problemas reales y utilizando herramientas modernas para resolverlos.” — Yonnier León

👨‍💻 Autor
Yonnier León
Desarrollador de Software en evolución, apasionado por la IA, la seguridad y la construcción de soluciones con impacto real.
GitHub: @YonnierDev
Desde Colombia para el mundo. 🌎🚀
