import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# ==========================================================
# 1️⃣ SIMULATE MULTIVARIATE PLANT DATA
# ==========================================================

def generate_plant_data(n_samples=4000):

    np.random.seed(42)

    time = pd.date_range(start="2023-01-01", periods=n_samples, freq="H")

    temperature = np.random.normal(300, 5, n_samples)
    pressure = np.random.normal(10, 0.5, n_samples)
    flow_rate = np.random.normal(120, 8, n_samples)
    vibration = np.random.normal(4, 0.3, n_samples)

    # Inject anomalies
    anomaly_indices = np.random.choice(n_samples, 50, replace=False)

    temperature[anomaly_indices] += np.random.normal(30, 5, 50)
    pressure[anomaly_indices] -= np.random.normal(3, 0.5, 50)
    vibration[anomaly_indices] += np.random.normal(2, 0.5, 50)

    df = pd.DataFrame({
        "timestamp": time,
        "temperature": temperature,
        "pressure": pressure,
        "flow_rate": flow_rate,
        "vibration": vibration
    })

    return df


print("Generating plant data...")
df = generate_plant_data()

# ==========================================================
# 2️⃣ FEATURE SCALING
# ==========================================================

features = ["temperature", "pressure", "flow_rate", "vibration"]

scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[features])

# ==========================================================
# 3️⃣ TRAIN ISOLATION FOREST
# ==========================================================

model = IsolationForest(
    n_estimators=200,
    contamination=0.015,  # expected anomaly %
    random_state=42
)

print("Training Anomaly Detection Model...")
model.fit(scaled_data)

# ==========================================================
# 4️⃣ ANOMALY SCORING
# ==========================================================

df["anomaly_score"] = model.decision_function(scaled_data)
df["anomaly"] = model.predict(scaled_data)

# IsolationForest: -1 = anomaly, 1 = normal
df["anomaly_label"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

num_anomalies = df["anomaly_label"].sum()

print("\nDetected Anomalies:", num_anomalies)

# ==========================================================
# 5️⃣ VISUALIZATION
# ==========================================================

plt.figure(figsize=(10,5))
plt.plot(df["timestamp"], df["temperature"], label="Temperature")

anomaly_points = df[df["anomaly_label"] == 1]

plt.scatter(
    anomaly_points["timestamp"],
    anomaly_points["temperature"],
    color="red",
    label="Anomalies"
)

plt.title("Temperature with Detected Anomalies")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ==========================================================
# 6️⃣ SAVE MODEL
# ==========================================================

joblib.dump(model, "plant_anomaly_model.pkl")
joblib.dump(scaler, "plant_scaler.pkl")
print("Model and scaler saved.")

# ==========================================================
# 7️⃣ REAL-TIME ANOMALY CHECK FUNCTION
# ==========================================================

def check_anomaly(temperature, pressure, flow_rate, vibration):

    sample = np.array([[temperature, pressure, flow_rate, vibration]])
    sample_scaled = scaler.transform(sample)

    prediction = model.predict(sample_scaled)[0]
    score = model.decision_function(sample_scaled)[0]

    print("\n=== ANOMALY CHECK ===")
    print("Anomaly Score:", round(score, 4))

    if prediction == -1:
        print("⚠ Anomaly Detected")
    else:
        print("Normal Operation")


# Example
check_anomaly(
    temperature=340,
    pressure=6,
    flow_rate=120,
    vibration=7
)
