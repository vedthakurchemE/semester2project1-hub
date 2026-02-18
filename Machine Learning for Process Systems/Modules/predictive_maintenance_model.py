import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import random

# ==========================================================
# 1️⃣ SYNTHETIC INDUSTRIAL DATA GENERATION
# ==========================================================

def generate_dataset(n_samples=5000):

    data = []

    for _ in range(n_samples):

        temperature = np.random.normal(250, 10)
        vibration = np.random.normal(5, 1)
        pressure = np.random.normal(5, 0.5)
        runtime_hours = np.random.uniform(0, 5000)

        # Failure logic (simulate real degradation behavior)
        failure = 0

        if temperature > 270:
            failure = 1
        if vibration > 7:
            failure = 1
        if runtime_hours > 4500:
            failure = 1
        if pressure < 4:
            failure = 1

        data.append([
            temperature,
            vibration,
            pressure,
            runtime_hours,
            failure
        ])

    columns = [
        "temperature",
        "vibration",
        "pressure",
        "runtime_hours",
        "failure"
    ]

    return pd.DataFrame(data, columns=columns)

# ==========================================================
# 2️⃣ DATA PREPARATION
# ==========================================================

print("Generating dataset...")
df = generate_dataset()

X = df.drop("failure", axis=1)
y = df["failure"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==========================================================
# 3️⃣ TRAIN MODEL
# ==========================================================

print("Training Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================================================
# 4️⃣ MODEL EVALUATION
# ==========================================================

y_pred = model.predict(X_test)

print("\n=== MODEL PERFORMANCE ===")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ==========================================================
# 5️⃣ FEATURE IMPORTANCE
# ==========================================================

importance = model.feature_importances_
features = X.columns

plt.figure()
plt.bar(features, importance)
plt.title("Feature Importance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ==========================================================
# 6️⃣ PREDICT NEW EQUIPMENT CONDITION
# ==========================================================

def predict_equipment(temperature, vibration, pressure, runtime_hours):

    sample = np.array([[temperature, vibration, pressure, runtime_hours]])

    probability = model.predict_proba(sample)[0][1]
    prediction = model.predict(sample)[0]

    print("\n=== EQUIPMENT HEALTH PREDICTION ===")
    print(f"Failure Probability: {round(probability*100, 2)}%")

    if prediction == 1:
        print("⚠ Maintenance Required Soon")
    else:
        print("✓ Equipment Healthy")

# Example prediction
predict_equipment(
    temperature=275,
    vibration=6.5,
    pressure=4.8,
    runtime_hours=4600
)
