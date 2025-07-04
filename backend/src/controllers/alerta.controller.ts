import { Request, Response } from 'express';
import { analyzeNmapLog } from '../services/nmapAnalyzer.js';

interface NmapLogEntry {
  timestamp: string;
  sourceIp: string;
  scanType: string;
  target: string;
  details: string;
}

export const procesarAlerta = async (req: Request, res: Response) => {
  try {
    const logEntry: NmapLogEntry = req.body;
    
    // Analizar el log con el servicio de análisis
    const analisis = await analyzeNmapLog(logEntry);
    
    res.status(200).json({
      success: true,
      data: analisis,
      isThreat: analisis.riskLevel === 'HIGH',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error al procesar el log de Nmap:', error);
    res.status(500).json({
      success: false,
      message: 'Error al procesar el log de Nmap',
      error: error instanceof Error ? error.message : 'Error desconocido'
    });
  }
};
