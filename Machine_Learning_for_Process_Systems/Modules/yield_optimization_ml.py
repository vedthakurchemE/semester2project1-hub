import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
from scipy.optimize import minimize

# ==========================================================
# 1️⃣ SIMULATE PROCESS DATA
# ==========================================================

def generate_yield_data(n_samples=6000):

    np.random.seed(42)

    temperature = np.random.uniform(400, 600, n_samples)
    pressure = np.random.uniform(10, 30, n_samples)
    feed_rate = np.random.uniform(80, 150, n_samples)
    catalyst_age = np.random.uniform(0, 100, n_samples)

    # Nonlinear yield function
    yield_percent = (
        80
        + 0.08 * temperature
        + 1.5 * pressure
        - 0.0001 * temperature**2
        - 0.05 * catalyst_age
        + 0.002 * temperature * pressure
        - 0.01 * feed_rate
        + np.random.normal(0, 2, n_samples)
    )

    df = pd.DataFrame({
        "temperature": temperature,
        "pressure": pressure,
        "feed_rate": feed_rate,
        "catalyst_age": catalyst_age,
        "yield": yield_percent
    })

    return df


print("Generating yield dataset...")
df = generate_yield_data()

# ==========================================================
# 2️⃣ TRAIN ML MODEL
# ==========================================================

X = df.drop("yield", axis=1)
y = df["yield"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

print("Training Yield Model...")
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n=== YIELD MODEL PERFORMANCE ===")
print("RMSE:", round(rmse, 2))
print("R² Score:", round(r2, 4))

# ==========================================================
# 3️⃣ OPTIMIZATION FUNCTION
# ==========================================================

def objective(x):
    temperature, pressure, feed_rate, catalyst_age = x
    sample = np.array([[temperature, pressure, feed_rate, catalyst_age]])
    predicted_yield = model.predict(sample)[0]
    return -predicted_yield  # negative for maximization


# Bounds (process constraints)
bounds = [
    (400, 600),   # temperature
    (10, 30),     # pressure
    (80, 150),    # feed rate
    (0, 100)      # catalyst age
]

# Initial guess
initial_guess = [500, 20, 100, 20]

print("\nRunning Yield Optimization...")

result = minimize(
    objective,
    initial_guess,
    bounds=bounds,
    method="L-BFGS-B"
)

optimal_conditions = result.x
max_yield = -result.fun

print("\n=== OPTIMAL OPERATING CONDITIONS ===")
print("Temperature:", round(optimal_conditions[0], 2))
print("Pressure:", round(optimal_conditions[1], 2))
print("Feed Rate:", round(optimal_conditions[2], 2))
print("Catalyst Age:", round(optimal_conditions[3], 2))
print("Predicted Maximum Yield:", round(max_yield, 2))

# ==========================================================
# 4️⃣ SAVE MODEL
# ==========================================================

joblib.dump(model, "yield_model.pkl")
print("\nModel saved as yield_model.pkl")
