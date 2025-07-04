import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import { router as alertaRouter } from './routes/alerta.route.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/api', alertaRouter);

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Error:', err.stack);
  res.status(500).json({
    success: false,
    message: 'Error interno del servidor',
    error: process.env.NODE_ENV === 'development' ? err.message : {}
  });
});

// Start server
const server = app.listen(PORT, () => {
  console.log(`🚀 Servidor ejecutándose en http://localhost:${PORT}`);
  console.log(`📊 Panel de salud: http://localhost:${PORT}/api/health`);
});

// Manejo de cierres
gracefulShutdown();

function gracefulShutdown() {
  // Cierre ordenado
  process.on('SIGTERM', () => {
    console.log('Recibida señal SIGTERM. Cerrando servidor...');
    server.close(() => {
      console.log('Servidor cerrado exitosamente');
      process.exit(0);
    });
  });

  // Para reinicios
  process.on('SIGUSR2', () => {
    console.log('Reiniciando servidor...');
    server.close(() => {
      console.log('Servidor cerrado. Iniciando nuevo servidor...');
      process.kill(process.pid, 'SIGUSR2');
    });
  });
}

export default app;
