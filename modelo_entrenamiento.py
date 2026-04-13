import pandas as pd
import numpy as np
import tensorflow as tf
import json
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

# 1) Leer datos
data = pd.read_csv("dataset_entrenamiento.csv")
print("Dataset cargado:")
print(data.head())

# 2) Entradas (X) y salida (y)
X = data[["pace", "heart_rate", "cadence", "acceleration", "time"]]
y = data["label"]

# 3) Normalizar X
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 4) Separar entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

print("\nTamaños:")
print("Train:", X_train.shape, y_train.shape)
print("Test :", X_test.shape, y_test.shape)

# 5) Crear modelo (red neuronal simple)
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation="relu", input_shape=(5,)),
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(3, activation="softmax")
])

# 6) Compilar
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# 7) Entrenar
model.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), verbose=1)

# 8) Evaluar
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(f"\nPrecisión en prueba: {acc*100:.2f}%")

# 9) Predicciones
y_probs = model.predict(X_test, verbose=0)
y_pred = np.argmax(y_probs, axis=1)

# 10) Métricas
print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))

print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred, digits=4))

# 11) Mostrar algunos ejemplos
print("\nEjemplos (10 primeros):")
y_test_list = list(y_test)
for i in range(min(10, len(y_test_list))):
    print(f"{i}) Real={y_test_list[i]}  Pred={y_pred[i]}  Probs={y_probs[i]}")

# 12) Guardar modelo en formato Keras
model.save("pace_model.keras")
print("\nModelo guardado como pace_model.keras")

# 13) Convertir a TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open("pace_model.tflite", "wb") as f:
    f.write(tflite_model)

print("Modelo exportado como pace_model.tflite")

# 14) Guardar configuración del scaler
scaler_data = {
    "mean": scaler.mean_.tolist(),
    "std": scaler.scale_.tolist(),
    "features": ["pace", "heart_rate", "cadence", "acceleration", "time"],
    "labels": {
        "0": "ritmo_bajo",
        "1": "ritmo_optimo",
        "2": "ritmo_alto"
    }
}

with open("scaler_config.json", "w") as f:
    json.dump(scaler_data, f, indent=4)

print("Configuración guardada como scaler_config.json")