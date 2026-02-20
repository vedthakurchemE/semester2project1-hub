import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

# ==========================================================
# 1️⃣ SIMULATE DEGRADING EQUIPMENT DATA
# ==========================================================

def generate_degradation_data(n_units=50, time_steps=200):

    np.random.seed(42)

    data = []

    for unit in range(n_units):

        base_temp = np.random.normal(300, 5)
        base_vibration = np.random.normal(4, 0.2)

        failure_time = np.random.randint(150, time_steps)

        for t in range(time_steps):

            # Degradation pattern
            temp = base_temp + 0.05 * t + np.random.normal(0, 0.5)
            vibration = base_vibration + 0.02 * t + np.random.normal(0, 0.1)
            pressure = 10 - 0.01 * t + np.random.normal(0, 0.2)

            if t >= failure_time:
                break

            RUL = failure_time - t

            data.append([
                unit,
                t,
                temp,
                vibration,
                pressure,
                RUL
            ])

    columns = [
        "unit",
        "time",
        "temperature",
        "vibration",
        "pressure",
        "RUL"
    ]

    return pd.DataFrame(data, columns=columns)


print("Generating degradation dataset...")
df = generate_degradation_data()

# ==========================================================
# 2️⃣ FEATURE ENGINEERING
# ==========================================================

# Rolling mean features (captures trend)
df["temp_roll"] = df.groupby("unit")["temperature"].rolling(5).mean().reset_index(0,drop=True)
df["vib_roll"] = df.groupby("unit")["vibration"].rolling(5).mean().reset_index(0,drop=True)

df.dropna(inplace=True)

features = [
    "temperature",
    "vibration",
    "pressure",
    "temp_roll",
    "vib_roll"
]

X = df[features]
y = df["RUL"]

# ==========================================================
# 3️⃣ TRAIN / TEST SPLIT
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==========================================================
# 4️⃣ TRAIN RUL MODEL
# ==========================================================

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

print("Training RUL Estimator...")
model.fit(X_train, y_train)

# ==========================================================
# 5️⃣ EVALUATION
# ==========================================================

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n=== RUL MODEL PERFORMANCE ===")
print("RMSE:", round(rmse, 2))
print("R² Score:", round(r2, 4))

# ==========================================================
# 6️⃣ VISUALIZATION
# ==========================================================

plt.figure(figsize=(8,5))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual RUL")
plt.ylabel("Predicted RUL")
plt.title("RUL Prediction Performance")
plt.show()

# ==========================================================
# 7️⃣ SAVE MODEL
# ==========================================================

joblib.dump(model, "rul_model.pkl")
print("Model saved as rul_model.pkl")

# ==========================================================
# 8️⃣ REAL-TIME RUL ESTIMATION FUNCTION
# ==========================================================

def estimate_rul(temperature, vibration, pressure, temp_roll, vib_roll):

    sample = np.array([[temperature, vibration, pressure, temp_roll, vib_roll]])

    prediction = model.predict(sample)[0]

    print("\n=== RUL ESTIMATION ===")
    print("Estimated Remaining Useful Life:", round(prediction, 2), "cycles")

    return prediction


# Example
estimate_rul(
    temperature=320,
    vibration=6,
    pressure=8,
    temp_roll=319,
    vib_roll=5.8
)
