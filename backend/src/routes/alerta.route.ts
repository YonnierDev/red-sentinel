import { Router } from 'express';
import { procesarAlerta } from '../controllers/alerta.controller.js';
import { validateNmapLog } from '../schemas/alerta.schema.js';

const router = Router();

// Middleware de validación para logs de Nmap
const validateNmapLogMiddleware = (req: any, res: any, next: any) => {
  const { error } = validateNmapLog(req.body);
  
  if (error) {
    return res.status(400).json({ 
      success: false, 
      message: 'Error de validación del log',
      details: error.details.map((d: any) => ({
        message: d.message,
        path: d.path,
        type: d.type
      }))
    });
  }
  
  next();
};

// Ruta para recibir logs de Nmap
router.post('/nmap', validateNmapLogMiddleware, procesarAlerta);

// Ruta de salud mejorada
router.get('/health', (req, res) => {
  const healthCheck = {
    status: 'operational',
    service: 'Red Sentinel API',
    version: '1.0.0',
    uptime: `${process.uptime().toFixed(2)} seconds`,
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development',
    checks: {
      database: 'connected',  // En una implementación real, verificaría la conexión a la BD
      memoryUsage: `${(process.memoryUsage().heapUsed / 1024 / 1024).toFixed(2)} MB`,
      status: 'ok'
    }
  };

  try {
    res.status(200).json(healthCheck);
  } catch (error) {
    const errorResponse = {
      ...healthCheck,
      status: 'error',
      checks: {
        ...healthCheck.checks,
        status: 'error'
      },
      error: error instanceof Error ? error.message : 'Unknown error'
    };
    res.status(503).json(errorResponse);
  }
});

export { router };
