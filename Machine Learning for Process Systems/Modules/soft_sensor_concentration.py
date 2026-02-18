import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

# ==========================================================
# 1️⃣ SIMULATE PROCESS DATA
# ==========================================================

def generate_process_data(n_samples=6000):

    np.random.seed(42)

    temperature = np.random.normal(350, 15, n_samples)
    pressure = np.random.normal(8, 1, n_samples)
    flow_rate = np.random.normal(100, 10, n_samples)
    residence_time = np.random.normal(5, 0.5, n_samples)

    # Nonlinear concentration relationship (hidden chemistry)
    concentration = (
        0.02 * temperature
        + 0.5 * pressure
        - 0.01 * flow_rate
        + 2 * np.log(residence_time)
        + 0.0005 * temperature * pressure
        + np.random.normal(0, 0.5, n_samples)
    )

    df = pd.DataFrame({
        "temperature": temperature,
        "pressure": pressure,
        "flow_rate": flow_rate,
        "residence_time": residence_time,
        "concentration": concentration
    })

    return df


print("Generating synthetic process data...")
df = generate_process_data()

# ==========================================================
# 2️⃣ FEATURE ENGINEERING
# ==========================================================

df["temp_pressure_interaction"] = df["temperature"] * df["pressure"]
df["temp_squared"] = df["temperature"] ** 2

X = df.drop("concentration", axis=1)
y = df["concentration"]

# ==========================================================
# 3️⃣ TRAIN / TEST SPLIT
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==========================================================
# 4️⃣ TRAIN SOFT SENSOR MODEL
# ==========================================================

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

print("Training Soft Sensor Model...")
model.fit(X_train, y_train)

# ==========================================================
# 5️⃣ EVALUATION
# ==========================================================

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n=== SOFT SENSOR PERFORMANCE ===")
print("RMSE:", round(rmse, 4))
print("R² Score:", round(r2, 4))

# ==========================================================
# 6️⃣ FEATURE IMPORTANCE
# ==========================================================

importance = model.feature_importances_

plt.figure(figsize=(8,5))
sns.barplot(x=importance, y=X.columns)
plt.title("Soft Sensor Feature Importance")
plt.tight_layout()
plt.show()

# ==========================================================
# 7️⃣ SAVE MODEL
# ==========================================================

joblib.dump(model, "soft_sensor_model.pkl")
print("Model saved as soft_sensor_model.pkl")

# ==========================================================
# 8️⃣ REAL-TIME CONCENTRATION PREDICTION
# ==========================================================

def predict_concentration(temperature, pressure, flow_rate, residence_time):

    temp_pressure_interaction = temperature * pressure
    temp_squared = temperature ** 2

    sample = np.array([[temperature,
                        pressure,
                        flow_rate,
                        residence_time,
                        temp_pressure_interaction,
                        temp_squared]])

    prediction = model.predict(sample)[0]

    print("\n=== SOFT SENSOR OUTPUT ===")
    print("Estimated Concentration:", round(prediction, 3))

    return prediction


# Example
predict_concentration(
    temperature=360,
    pressure=9,
    flow_rate=95,
    residence_time=5.2
)
