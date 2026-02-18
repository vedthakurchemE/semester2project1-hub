import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

# ==========================================================
# 1️⃣ SIMULATE CATALYST DEACTIVATION DATA
# ==========================================================

def generate_catalyst_data(n_runs=40, time_steps=200):

    np.random.seed(42)
    data = []

    for run in range(n_runs):

        kd = np.random.uniform(0.005, 0.02)  # deactivation constant
        base_temp = np.random.normal(500, 10)
        base_pressure = np.random.normal(20, 1)
        base_feed = np.random.normal(100, 5)

        for t in range(time_steps):

            activity = np.exp(-kd * t)
            temperature = base_temp + 0.2 * t + np.random.normal(0, 2)
            pressure = base_pressure + np.random.normal(0, 0.5)
            feed_rate = base_feed + np.random.normal(0, 3)

            conversion = activity * 0.8 + np.random.normal(0, 0.02)

            data.append([
                run,
                t,
                temperature,
                pressure,
                feed_rate,
                conversion,
                activity
            ])

    columns = [
        "run",
        "time",
        "temperature",
        "pressure",
        "feed_rate",
        "conversion",
        "activity"
    ]

    return pd.DataFrame(data, columns=columns)


print("Generating catalyst dataset...")
df = generate_catalyst_data()

# ==========================================================
# 2️⃣ FEATURE ENGINEERING
# ==========================================================

df["temp_time_interaction"] = df["temperature"] * df["time"]
df["conversion_roll"] = df.groupby("run")["conversion"].rolling(5).mean().reset_index(0,drop=True)

df.dropna(inplace=True)

features = [
    "time",
    "temperature",
    "pressure",
    "feed_rate",
    "conversion",
    "temp_time_interaction",
    "conversion_roll"
]

X = df[features]
y = df["activity"]

# ==========================================================
# 3️⃣ TIME-AWARE SPLIT
# ==========================================================

split = int(0.8 * len(df))
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

# ==========================================================
# 4️⃣ TRAIN XGBOOST MODEL
# ==========================================================

model = XGBRegressor(
    n_estimators=600,
    learning_rate=0.03,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

print("Training Catalyst Deactivation Model...")
model.fit(X_train, y_train)

# ==========================================================
# 5️⃣ EVALUATION
# ==========================================================

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n=== CATALYST MODEL PERFORMANCE ===")
print("RMSE:", round(rmse, 4))
print("R² Score:", round(r2, 4))

# ==========================================================
# 6️⃣ PLOT ACTIVITY DECAY (ACTUAL VS PREDICTED)
# ==========================================================

plt.figure(figsize=(8,5))
plt.plot(y_test.values[:300], label="Actual Activity")
plt.plot(y_pred[:300], label="Predicted Activity")
plt.title("Catalyst Activity Prediction")
plt.legend()
plt.show()

# ==========================================================
# 7️⃣ SAVE MODEL
# ==========================================================

joblib.dump(model, "catalyst_deactivation_model.pkl")
print("Model saved as catalyst_deactivation_model.pkl")

# ==========================================================
# 8️⃣ REGENERATION THRESHOLD CHECK
# ==========================================================

def check_regeneration(activity_value, threshold=0.6):

    print("\n=== REGENERATION CHECK ===")
    print("Current Activity:", round(activity_value, 3))

    if activity_value < threshold:
        print("⚠ Regeneration Recommended")
    else:
        print("Catalyst Operating Normally")


# Example prediction
sample = X_test.iloc[0:1]
predicted_activity = model.predict(sample)[0]

check_regeneration(predicted_activity)
