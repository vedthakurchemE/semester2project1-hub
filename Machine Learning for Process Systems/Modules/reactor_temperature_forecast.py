import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# ==========================================================
# 1️⃣ SIMULATE REACTOR TIME-SERIES DATA
# ==========================================================

def generate_reactor_data(n_steps=2000):

    np.random.seed(42)

    time = np.arange(n_steps)

    # Control inputs
    coolant_flow = 50 + 5 * np.sin(0.02 * time)
    feed_rate = 100 + 10 * np.cos(0.015 * time)

    # Reactor temperature dynamics
    temperature = (
        250
        + 0.3 * feed_rate
        - 0.5 * coolant_flow
        + 10 * np.sin(0.01 * time)
        + np.random.normal(0, 2, n_steps)
    )

    df = pd.DataFrame({
        "temperature": temperature,
        "coolant_flow": coolant_flow,
        "feed_rate": feed_rate
    })

    return df


df = generate_reactor_data()

# ==========================================================
# 2️⃣ DATA NORMALIZATION
# ==========================================================

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df)

# ==========================================================
# 3️⃣ CREATE TIME WINDOWS (SEQUENCES)
# ==========================================================

def create_sequences(data, window_size=20):

    X = []
    y = []

    for i in range(len(data) - window_size):
        X.append(data[i:i+window_size])
        y.append(data[i+window_size][0])  # temperature target

    return np.array(X), np.array(y)


window_size = 20
X, y = create_sequences(scaled_data, window_size)

# Time-based split (NO random shuffle)
split = int(0.8 * len(X))

X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# ==========================================================
# 4️⃣ BUILD LSTM MODEL
# ==========================================================

model = Sequential()
model.add(LSTM(64, input_shape=(window_size, 3)))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))

model.compile(
    optimizer='adam',
    loss='mse'
)

print("Training LSTM model...")
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

# ==========================================================
# 5️⃣ EVALUATION
# ==========================================================

predictions = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, predictions))
print("\nTest RMSE:", rmse)

# Inverse scale temperature
temp_scaler = MinMaxScaler()
temp_scaler.fit(df[["temperature"]])

pred_rescaled = temp_scaler.inverse_transform(predictions)
y_test_rescaled = temp_scaler.inverse_transform(y_test.reshape(-1,1))

# ==========================================================
# 6️⃣ PLOT RESULTS
# ==========================================================

plt.figure(figsize=(10,5))
plt.plot(y_test_rescaled, label="Actual Temperature")
plt.plot(pred_rescaled, label="Predicted Temperature")
plt.title("Reactor Temperature Forecast")
plt.legend()
plt.show()

# ==========================================================
# 7️⃣ FUTURE FORECAST FUNCTION
# ==========================================================

def forecast_future(model, last_window, steps=10):

    predictions = []
    current_window = last_window.copy()

    for _ in range(steps):
        pred = model.predict(current_window.reshape(1, window_size, 3))
        predictions.append(pred[0][0])

        # Update window (shift left)
        next_input = np.append(current_window[1:],
                               [[pred[0][0], current_window[-1][1], current_window[-1][2]]],
                               axis=0)
        current_window = next_input

    return np.array(predictions)


last_window = X_test[-1]
future_preds = forecast_future(model, last_window, steps=20)

future_rescaled = temp_scaler.inverse_transform(future_preds.reshape(-1,1))

print("\nNext 20-step Forecast:")
print(future_rescaled.flatten())
