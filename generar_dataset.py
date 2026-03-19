import numpy as np
import pandas as pd

np.random.seed(42)

def crear_datos(n, pace_m, pace_s, hr_m, hr_s, cad_m, cad_s, acc_m, acc_s, label):
    pace = np.random.normal(pace_m, pace_s, n)
    hr = np.random.normal(hr_m, hr_s, n)
    cad = np.random.normal(cad_m, cad_s, n)
    acc = np.random.normal(acc_m, acc_s, n)
    time = np.random.uniform(0, 3600, n)
    pace = np.clip(pace, 220, 420)
    hr = np.clip(hr, 90, 200)
    cad = np.clip(cad, 120, 200)
    acc = np.clip(acc, 0.05, 0.30)

    return pd.DataFrame({
        "pace": pace.round().astype(int),
        "heart_rate": hr.round().astype(int),
        "cadence": cad.round().astype(int),
        "acceleration": acc.round(3),
        "time": time.round().astype(int),
        "label": np.full(n, label, dtype=int)
    })

n = 200

# 0 = bajo, 1 = óptimo, 2 = alto
df0 = crear_datos(n, 330, 15, 145, 10, 155, 8, 0.11, 0.02, 0)
df1 = crear_datos(n, 300, 12, 160, 10, 165, 7, 0.14, 0.02, 1)
df2 = crear_datos(n, 270, 12, 175, 10, 178, 7, 0.18, 0.02, 2)

dataset = pd.concat([df0, df1, df2], ignore_index=True)
dataset = dataset.sample(frac=1, random_state=42).reset_index(drop=True)

dataset.to_csv("dataset_entrenamiento.csv", index=False)

print("Dataset generado: dataset_entrenamiento.csv")
print(dataset.head())
print("\nDistribución de clases:")
print(dataset["label"].value_counts())