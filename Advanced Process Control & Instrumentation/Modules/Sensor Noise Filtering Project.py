import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq

def run():

    st.title("📡 Sensor Noise Filtering Simulator")

    # ==================================
    # Signal Generation
    # ==================================
    st.subheader("Signal Configuration")

    sim_time = 20
    dt = 0.05
    t = np.arange(0, sim_time, dt)

    true_signal = 50 + 10*np.sin(0.5*t)

    noise_std = st.slider("Noise Standard Deviation", 0.1, 10.0, 3.0)
    noise = np.random.normal(0, noise_std, len(t))

    measured = true_signal + noise

    # ==================================
    # Moving Average Filter
    # ==================================
    window = st.slider("Moving Average Window", 1, 50, 10)
    ma_filtered = np.convolve(measured, np.ones(window)/window, mode='same')

    # ==================================
    # Exponential Filter
    # ==================================
    alpha = st.slider("Exponential Alpha", 0.01, 1.0, 0.2)

    exp_filtered = np.zeros(len(measured))
    exp_filtered[0] = measured[0]

    for i in range(1, len(measured)):
        exp_filtered[i] = alpha*measured[i] + (1-alpha)*exp_filtered[i-1]

    # ==================================
    # Kalman Filter
    # ==================================
    Q = st.slider("Kalman Process Noise (Q)", 0.0001, 5.0, 0.01)
    R = noise_std**2

    x_est = 0
    P = 1
    kalman_filtered = []

    for z in measured:
        # Prediction
        P = P + Q

        # Update
        K = P / (P + R)
        x_est = x_est + K*(z - x_est)
        P = (1 - K)*P

        kalman_filtered.append(x_est)

    kalman_filtered = np.array(kalman_filtered)

    # ==================================
    # Plot Time Domain
    # ==================================
    st.subheader("Time Domain Comparison")

    fig, ax = plt.subplots()
    ax.plot(t, measured, alpha=0.4, label="Measured")
    ax.plot(t, true_signal, label="True Signal")
    ax.plot(t, ma_filtered, label="Moving Average")
    ax.plot(t, exp_filtered, label="Exponential")
    ax.plot(t, kalman_filtered, label="Kalman")
    ax.legend()
    st.pyplot(fig)

    # ==================================
    # Frequency Domain
    # ==================================
    st.subheader("Frequency Spectrum (Measured Signal)")

    yf = np.abs(fft(measured))
    xf = fftfreq(len(t), dt)

    fig2, ax2 = plt.subplots()
    ax2.plot(xf[:len(xf)//2], yf[:len(yf)//2])
    ax2.set_xlabel("Frequency")
    ax2.set_ylabel("Amplitude")
    st.pyplot(fig2)

    # ==================================
    # Performance Metrics
    # ==================================
    def rmse(a, b):
        return np.sqrt(np.mean((a-b)**2))

    st.subheader("Performance Metrics (RMSE vs True Signal)")

    st.write(f"Measured RMSE: {round(rmse(true_signal, measured),3)}")
    st.write(f"Moving Avg RMSE: {round(rmse(true_signal, ma_filtered),3)}")
    st.write(f"Exponential RMSE: {round(rmse(true_signal, exp_filtered),3)}")
    st.write(f"Kalman RMSE: {round(rmse(true_signal, kalman_filtered),3)}")

if __name__ == "__main__":
    run()
