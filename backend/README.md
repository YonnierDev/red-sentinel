# 🛡️ Red Sentinel - Backend

> Sistema de análisis de seguridad para detección de escaneos de red sospechosos

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)
[![Express.js](https://img.shields.io/badge/Express.js-404D59?style=for-the-badge)](https://expressjs.com/)

## 📋 Descripción

Red Sentinel es un sistema de análisis de seguridad que monitorea y analiza patrones de tráfico de red para detectar actividades sospechosas, específicamente escaneos de puertos y vulnerabilidades utilizando Nmap y otras herramientas similares.

## 🚀 Características Principales

- 🎯 Detección de patrones de escaneo sospechosos
- 📊 Análisis en tiempo real de logs de red
- ⚡ API RESTful para integración con otros sistemas
- 📈 Panel de monitoreo de salud del servicio
- 🔍 Validación avanzada de datos de entrada

## 🛠️ Tecnologías

- **Lenguaje**: TypeScript
- **Runtime**: Node.js
- **Framework**: Express
- **Validación**: Joi
- **Desarrollo**: Nodemon, ts-node

## 📦 Estructura del Proyecto

```
src/
├── controllers/     # Lógica de negocio
├── routes/         # Definición de endpoints
├── services/       # Servicios externos
├── schemas/        # Validación de datos
└── index.ts        # Punto de entrada
```

## 🚀 Empezando

### Requisitos Previos

- Node.js 16+
- npm 8+
- TypeScript 4.7+

### Instalación

1. Clonar el repositorio
   ```bash
   git clone https://github.com/tu-usuario/red-sentinel.git
   cd red-sentinel/backend
   ```

2. Instalar dependencias
   ```bash
   npm install
   ```

3. Configurar variables de entorno
   ```bash
   cp .env.example .env
   # Editar .env según sea necesario
   ```

### Ejecución

**Modo desarrollo**:
```bash
npm run dev
```

**Modo producción**:
```bash
npm run build
npm start
```

## 📚 Documentación de la API

### Endpoints Principales

#### POST /api/nmap
Procesa logs de escaneos Nmap.

**Ejemplo de solicitud:**
```json
{
  "timestamp": "2025-07-03T23:30:00-05:00",
  "sourceIp": "192.168.1.100",
  "target": "192.168.1.1",
  "scanType": "SYN",
  "details": "Escaneo de puertos detectado",
  "port": 80,
  "protocol": "tcp"
}
```

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "data": {
    "riskLevel": "MEDIUM",
    "description": "Escaneo detectado desde 192.168.1.100",
    "detectedPatterns": ["Tipo de escaneo avanzado detectado"],
    "recommendedAction": "Monitorear IP de origen"
  },
  "isThreat": false
}
```

#### GET /api/health
Verifica el estado del servicio.

**Respuesta exitosa (200 OK):**
```json
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
```

## 🧪 Pruebas

Para ejecutar las pruebas:
```bash
npm test
```

## 🤝 Contribución

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

Desarrollado con ❤️ por [Tu Nombre] | [@tu-usuario](https://github.com/tu-usuario)
