import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

# ==========================================================
# 1️⃣ SYNTHETIC PROCESS DATA GENERATION
# ==========================================================

def generate_quality_dataset(n_samples=5000):

    np.random.seed(42)

    temperature = np.random.normal(200, 15, n_samples)
    pressure = np.random.normal(5, 0.5, n_samples)
    flow_rate = np.random.normal(100, 10, n_samples)
    humidity = np.random.normal(40, 5, n_samples)
    vibration = np.random.normal(5, 1, n_samples)

    # True quality formula (non-linear + noise)
    quality = (
        0.3 * temperature
        + 10 * pressure
        + 0.5 * flow_rate
        - 0.2 * humidity
        - 5 * vibration
        + 0.01 * temperature * pressure
        + np.random.normal(0, 5, n_samples)
    )

    df = pd.DataFrame({
        "temperature": temperature,
        "pressure": pressure,
        "flow_rate": flow_rate,
        "humidity": humidity,
        "vibration": vibration,
        "quality_score": quality
    })

    return df


# ==========================================================
# 2️⃣ DATA PREPARATION
# ==========================================================

print("Generating dataset...")
df = generate_quality_dataset()

X = df.drop("quality_score", axis=1)
y = df["quality_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==========================================================
# 3️⃣ TRAIN XGBOOST REGRESSION MODEL
# ==========================================================

print("Training XGBoost Quality Model...")

model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================================================
# 4️⃣ MODEL EVALUATION
# ==========================================================

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n=== MODEL PERFORMANCE ===")
print("RMSE:", round(rmse, 3))
print("R² Score:", round(r2, 4))

# ==========================================================
# 5️⃣ FEATURE IMPORTANCE
# ==========================================================

importance = model.feature_importances_
features = X.columns

plt.figure()
sns.barplot(x=importance, y=features)
plt.title("Feature Importance")
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.tight_layout()
plt.show()

# ==========================================================
# 6️⃣ SAVE MODEL
# ==========================================================

joblib.dump(model, "xgboost_quality_model.pkl")
print("Model saved as xgboost_quality_model.pkl")

# ==========================================================
# 7️⃣ REAL-TIME QUALITY PREDICTION FUNCTION
# ==========================================================

def predict_quality(temperature, pressure, flow_rate, humidity, vibration):

    sample = np.array([[temperature, pressure, flow_rate, humidity, vibration]])

    prediction = model.predict(sample)[0]

    print("\n=== QUALITY PREDICTION ===")
    print("Predicted Quality Score:", round(prediction, 2))


# Example test
predict_quality(
    temperature=210,
    pressure=5.5,
    flow_rate=110,
    humidity=38,
    vibration=4
)
