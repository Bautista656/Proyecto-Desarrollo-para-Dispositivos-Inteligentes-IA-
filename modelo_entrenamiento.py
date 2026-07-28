import pandas as pd
import numpy as np
import tensorflow as tf
import json
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

FEATURES = ["pace", "heart_rate", "cadence", "acceleration", "time"]
ETIQUETAS = ["ritmo_bajo", "ritmo_optimo", "ritmo_alto"]

# 1) Leer datos
data = pd.read_csv("dataset_entrenamiento.csv")
print("Dataset cargado:")
print(data.head())

# 2) Entradas (X) y salida (y)
X = data[FEATURES]
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

print("\nTamanos:")
print("Train:", X_train.shape, y_train.shape)
print("Test :", X_test.shape, y_test.shape)

# 5) Crear modelo (red neuronal simple)
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(5,)),
    tf.keras.layers.Dense(16, activation="relu"),
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
print(f"\nPrecision en prueba: {acc*100:.2f}%")

# 9) Predicciones
y_probs = model.predict(X_test, verbose=0)
y_pred = np.argmax(y_probs, axis=1)

# 10) Metricas
print("\nMatriz de confusion:")
print(confusion_matrix(y_test, y_pred))

print("\nReporte de clasificacion:")
print(classification_report(y_test, y_pred, target_names=ETIQUETAS, digits=4))

# 11) Guardar modelo en formato Keras
model.save("pace_model.keras")
print("\nModelo guardado como pace_model.keras")

# 12) Convertir a TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open("pace_model.tflite", "wb") as f:
    f.write(tflite_model)

print("Modelo exportado como pace_model.tflite")

# 13) Guardar configuracion del scaler
#     La llave DEBE llamarse "std": es la que lee PaceClassifier.kt en la app.
scaler_data = {
    "mean": scaler.mean_.tolist(),
    "std": scaler.scale_.tolist(),
    "features": FEATURES,
    "labels": {
        "0": "ritmo_bajo",
        "1": "ritmo_optimo",
        "2": "ritmo_alto"
    }
}

with open("scaler_config.json", "w") as f:
    json.dump(scaler_data, f, indent=4)

print("Configuracion guardada como scaler_config.json")


# ---------------------------------------------------------------------------
# 14) VERIFICACION FINAL
#     Se ejecuta el .tflite ya exportado con valores realistas, en las mismas
#     unidades que entrega la app, para confirmar que las tres clases se
#     distinguen correctamente antes de copiar el modelo al proyecto Android.
# ---------------------------------------------------------------------------
print("\n" + "=" * 62)
print("VERIFICACION CON VALORES REALES DE LA APP")
print("=" * 62)

interpreter = tf.lite.Interpreter(model_path="pace_model.tflite")
interpreter.allocate_tensors()
entrada = interpreter.get_input_details()[0]
salida = interpreter.get_output_details()[0]

media = np.array(scaler_data["mean"])
desv = np.array(scaler_data["std"])


def predecir(valores):
    x = ((np.array(valores, dtype=np.float64) - media) / desv).astype(np.float32)
    interpreter.set_tensor(entrada["index"], x.reshape(1, -1))
    interpreter.invoke()
    probs = interpreter.get_tensor(salida["index"])[0]
    return ETIQUETAS[int(np.argmax(probs))], float(np.max(probs)) * 100


# pace(min/km), bpm, cadencia(pasos/min), aceleracion(m/s^2), tiempo(seg)
casos = [
    ("Trote suave    (7:00 min/km)", [7.0, 132, 148, 0.9, 1500], "ritmo_bajo"),
    ("Ritmo moderado (5:50 min/km)", [5.8, 157, 165, 1.6, 1500], "ritmo_optimo"),
    ("Ritmo fuerte   (4:40 min/km)", [4.7, 180, 181, 2.5, 1500], "ritmo_alto"),
]

correctos = 0
for descripcion, valores, esperado in casos:
    etiqueta, confianza = predecir(valores)
    ok = etiqueta == esperado
    correctos += ok
    print(f"{descripcion} -> {etiqueta:<13} {confianza:6.2f}%   {'OK' if ok else 'ERROR'}")

print("=" * 62)
if correctos == len(casos):
    print("VERIFICACION SUPERADA: el modelo distingue las tres clases.")
    print("Ya puedes copiar pace_model.tflite y scaler_config.json a la app.")
else:
    print(f"ATENCION: solo {correctos}/{len(casos)} casos correctos. NO copies el modelo a la app.")
print("=" * 62)
