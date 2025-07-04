import axios from 'axios';

const FASTAPI_URL = process.env.FASTAPI_URL || 'http://localhost:8000';

export const callModel = async (data: any) => {
  try {
    const response = await axios.post(`${FASTAPI_URL}/predict`, data);
    return response.data;
  } catch (error) {
    console.error('Error al llamar al modelo de FastAPI:', error);
    throw new Error('Error al procesar la solicitud con el modelo');
  }
};
