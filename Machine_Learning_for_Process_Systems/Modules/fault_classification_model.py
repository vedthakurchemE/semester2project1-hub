import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# ==========================================================
# 1️⃣ SYNTHETIC MULTI-FAULT DATA GENERATION
# ==========================================================

def generate_fault_dataset(n_samples=6000):

    data = []

    for _ in range(n_samples):

        temperature = np.random.normal(250, 10)
        vibration = np.random.normal(5, 1)
        pressure = np.random.normal(5, 0.5)
        flow_rate = np.random.normal(100, 10)

        # Fault labeling logic
        # 0 = Normal
        # 1 = Overheating
        # 2 = Bearing Fault
        # 3 = Pressure Leak
        # 4 = Flow Blockage

        fault = 0

        if temperature > 270:
            fault = 1
        elif vibration > 7:
            fault = 2
        elif pressure < 4:
            fault = 3
        elif flow_rate < 80:
            fault = 4

        data.append([
            temperature,
            vibration,
            pressure,
            flow_rate,
            fault
        ])

    columns = [
        "temperature",
        "vibration",
        "pressure",
        "flow_rate",
        "fault_type"
    ]

    return pd.DataFrame(data, columns=columns)

# ==========================================================
# 2️⃣ DATA PREPARATION
# ==========================================================

print("Generating fault dataset...")
df = generate_fault_dataset()

X = df.drop("fault_type", axis=1)
y = df["fault_type"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==========================================================
# 3️⃣ TRAIN MULTI-CLASS MODEL
# ==========================================================

print("Training Fault Classification Model...")

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================================================
# 4️⃣ MODEL EVALUATION
# ==========================================================

y_pred = model.predict(X_test)

print("\n=== MODEL PERFORMANCE ===")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure()
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

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
# 6️⃣ REAL-TIME FAULT PREDICTION FUNCTION
# ==========================================================

fault_labels = {
    0: "Normal Operation",
    1: "Overheating Fault",
    2: "Bearing Fault",
    3: "Pressure Leak",
    4: "Flow Blockage"
}

def predict_fault(temperature, vibration, pressure, flow_rate):

    sample = np.array([[temperature, vibration, pressure, flow_rate]])

    prediction = model.predict(sample)[0]
    probabilities = model.predict_proba(sample)[0]

    print("\n=== FAULT DIAGNOSIS RESULT ===")
    print("Predicted Fault:", fault_labels[prediction])
    print("Confidence:", round(max(probabilities) * 100, 2), "%")

# Example test case
predict_fault(
    temperature=280,
    vibration=5,
    pressure=5,
    flow_rate=100
)
