import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

# ==========================================================
# 1️⃣ GENERATE SYNTHETIC ENERGY DATA
# ==========================================================

def generate_energy_data(n_hours=5000):

    np.random.seed(42)

    time_index = pd.date_range(start="2023-01-01", periods=n_hours, freq="H")

    temperature = 20 + 10 * np.sin(2 * np.pi * time_index.hour / 24)
    humidity = 50 + 10 * np.cos(2 * np.pi * time_index.hour / 24)
    occupancy = np.random.randint(10, 100, n_hours)

    # Energy consumption formula
    energy = (
        200
        + 5 * temperature
        + 0.8 * humidity
        + 1.5 * occupancy
        + 30 * np.sin(2 * np.pi * time_index.hour / 24)
        + np.random.normal(0, 10, n_hours)
    )

    df = pd.DataFrame({
        "timestamp": time_index,
        "temperature": temperature,
        "humidity": humidity,
        "occupancy": occupancy,
        "energy_consumption": energy
    })

    return df


df = generate_energy_data()

# ==========================================================
# 2️⃣ FEATURE ENGINEERING (TIME FEATURES + LAGS)
# ==========================================================

df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek

# Lag features
df["lag_1"] = df["energy_consumption"].shift(1)
df["lag_24"] = df["energy_consumption"].shift(24)

df.dropna(inplace=True)

# ==========================================================
# 3️⃣ TRAIN/TEST SPLIT (TIME-BASED)
# ==========================================================

split = int(0.8 * len(df))

train = df.iloc[:split]
test = df.iloc[split:]

features = [
    "temperature",
    "humidity",
    "occupancy",
    "hour",
    "day_of_week",
    "lag_1",
    "lag_24"
]

X_train = train[features]
y_train = train["energy_consumption"]

X_test = test[features]
y_test = test["energy_consumption"]

# ==========================================================
# 4️⃣ TRAIN XGBOOST MODEL
# ==========================================================

model = XGBRegressor(
    n_estimators=400,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

print("Training Energy Consumption Model...")
model.fit(X_train, y_train)

# ==========================================================
# 5️⃣ EVALUATION
# ==========================================================

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n=== MODEL PERFORMANCE ===")
print("RMSE:", round(rmse, 2))
print("R² Score:", round(r2, 4))

# ==========================================================
# 6️⃣ FEATURE IMPORTANCE
# ==========================================================

importance = model.feature_importances_

plt.figure(figsize=(8,5))
sns.barplot(x=importance, y=features)
plt.title("Feature Importance")
plt.tight_layout()
plt.show()

# ==========================================================
# 7️⃣ SAVE MODEL
# ==========================================================

joblib.dump(model, "energy_model_xgboost.pkl")
print("Model saved as energy_model_xgboost.pkl")

# ==========================================================
# 8️⃣ FUTURE FORECAST FUNCTION
# ==========================================================

def forecast_next_hour(last_row):

    prediction = model.predict(last_row[features])[0]

    print("\nPredicted Next Hour Energy Consumption:", round(prediction, 2))

    return prediction


# Example prediction
forecast_next_hour(test.tail(1))
