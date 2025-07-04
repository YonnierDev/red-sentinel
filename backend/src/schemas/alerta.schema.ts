import Joi from 'joi';

// Esquema de validación para logs de Nmap
export const nmapLogSchema = Joi.object({
  timestamp: Joi.date().iso().required(),
  sourceIp: Joi.string().ip().required(),
  scanType: Joi.string().required(),
  target: Joi.string().required(),
  details: Joi.string().required(),
  port: Joi.number().port().optional(),
  protocol: Joi.string().valid('tcp', 'udp', 'icmp').optional(),
  status: Joi.string().optional(),
  service: Joi.string().optional(),
  version: Joi.string().optional()
});

// Función de validación mejorada
export const validateNmapLog = (data: any) => {
  return nmapLogSchema.validate(data, { 
    abortEarly: false,
    allowUnknown: true // Permite campos adicionales
  });
};

// Alias para mantener compatibilidad
export const validateAlerta = validateNmapLog;
