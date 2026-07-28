import numpy as np
import pandas as pd

np.random.seed(42)

# ---------------------------------------------------------------------------
# Generador del dataset de entrenamiento de ALYRA
#
# IMPORTANTE: las unidades de cada variable deben coincidir EXACTAMENTE con
# las que produce la aplicacion movil, de lo contrario el modelo recibe
# valores fuera de su rango de entrenamiento y siempre predice la misma clase.
#
#   pace          -> minutos por kilometro   (SensorPrecisionUtils.calcularPaceSeguro)
#   heart_rate    -> latidos por minuto      (sensor del reloj)
#   cadence       -> pasos por minuto        (SensorPrecisionUtils.calcularCadencia)
#   acceleration  -> metros por segundo^2    (magnitud del acelerometro del reloj)
#   time          -> segundos                (duracion de la sesion)
# ---------------------------------------------------------------------------


def crear_datos(n, pace_m, pace_s, hr_m, hr_s, cad_m, cad_s, acc_m, acc_s, label):
    pace = np.random.normal(pace_m, pace_s, n)
    hr = np.random.normal(hr_m, hr_s, n)
    cad = np.random.normal(cad_m, cad_s, n)
    acc = np.random.normal(acc_m, acc_s, n)
    time = np.random.uniform(0, 3600, n)

    # Limites realistas, alineados con los rangos que la app puede entregar
    pace = np.clip(pace, 3.0, 12.0)     # min/km
    hr = np.clip(hr, 90, 200)           # bpm
    cad = np.clip(cad, 120, 200)        # pasos/min
    acc = np.clip(acc, 0.3, 4.0)        # m/s^2

    return pd.DataFrame({
        "pace": pace.round(2),                  # decimales: 5.83 min/km, no 6
        "heart_rate": hr.round().astype(int),
        "cadence": cad.round().astype(int),
        "acceleration": acc.round(3),
        "time": time.round().astype(int),
        "label": np.full(n, label, dtype=int)
    })


n = 400

# 0 = ritmo bajo, 1 = ritmo optimo, 2 = ritmo alto
# A mayor intensidad: el pace BAJA (mas rapido) y suben bpm, cadencia y aceleracion.
df0 = crear_datos(n, pace_m=7.0, pace_s=0.60, hr_m=135, hr_s=10,
                  cad_m=150, cad_s=8, acc_m=1.0, acc_s=0.25, label=0)

df1 = crear_datos(n, pace_m=5.8, pace_s=0.50, hr_m=158, hr_s=10,
                  cad_m=165, cad_s=7, acc_m=1.6, acc_s=0.30, label=1)

df2 = crear_datos(n, pace_m=4.7, pace_s=0.50, hr_m=178, hr_s=10,
                  cad_m=180, cad_s=7, acc_m=2.4, acc_s=0.35, label=2)

dataset = pd.concat([df0, df1, df2], ignore_index=True)
dataset = dataset.sample(frac=1, random_state=42).reset_index(drop=True)

dataset.to_csv("dataset_entrenamiento.csv", index=False)

print("Dataset generado: dataset_entrenamiento.csv")
print(dataset.head())

print("\nDistribucion de clases:")
print(dataset["label"].value_counts().sort_index())

print("\nRangos por variable:")
print(dataset.drop(columns=["label"]).describe().loc[["min", "mean", "max"]].round(2))
