# ml-model/train_dummy_model.py
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib
import os

print("Entrenando modelo de ejemplo...")

# Crear datos de ejemplo
np.random.seed(42)  # Para resultados reproducibles
X = np.random.rand(100, 5)  # 100 muestras, 5 características
y = np.random.randint(0, 2, 100)  # Clases binarias (0 o 1)

# Entrenar modelo simple
print("Entrenando Random Forest...")
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X, y)

# Crear carpeta models si no existe
os.makedirs("models", exist_ok=True)

# Guardar modelo
model_path = "models/dummy_model.pkl"
joblib.dump(model, model_path)
print(f"✅ Modelo guardado en: {os.path.abspath(model_path)}")
print("Puedes usar este modelo en tu aplicación con MODEL_PATH='models/dummy_model.pkl'")