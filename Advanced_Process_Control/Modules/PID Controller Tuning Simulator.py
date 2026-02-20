import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def run():
    st.title("🎛️ PID Controller Tuning Simulator")
    st.markdown("""
    Simulate a **PID-controlled first-order process** and compare tuning methods.

    Process Model (FOPDT approximation without delay):

    dT/dt = (-T + K*u)/τ
    """)

    st.subheader("🏭 Process Parameters")

    col1, col2 = st.columns(2)

    with col1:
        K = st.number_input("Process Gain (K)", value=1.0)

    with col2:
        tau = st.number_input("Time Constant (τ)", min_value=0.1, value=5.0)

    setpoint = st.number_input("Setpoint", value=1.0)
    sim_time = st.slider("Simulation Time", 10, 200, 100)

    method = st.selectbox("Tuning Method", ["Manual", "Ziegler-Nichols"])

    if method == "Manual":
        st.subheader("🎛️ Manual PID Parameters")
        col3, col4, col5 = st.columns(3)
        with col3:
            Kp = st.number_input("Kp", value=2.0)
        with col4:
            Ki = st.number_input("Ki", value=0.5)
        with col5:
            Kd = st.number_input("Kd", value=0.1)

    else:
        # Ziegler-Nichols (Step response based approximation)
        Ku = 1.2 * tau / K
        Pu = 2 * tau

        Kp = 0.6 * Ku
        Ki = 2 * Kp / Pu
        Kd = Kp * Pu / 8

        st.info(f"Z-N Tuned Parameters → Kp={round(Kp, 2)}, Ki={round(Ki, 2)}, Kd={round(Kd, 2)}")

    # Simulation
    dt = 0.1
    t = np.arange(0, sim_time, dt)

    y = np.zeros(len(t))
    u = np.zeros(len(t))
    error = np.zeros(len(t))

    integral = 0
    prev_error = 0

    for i in range(1, len(t)):
        error[i] = setpoint - y[i - 1]
        integral += error[i] * dt
        derivative = (error[i] - prev_error) / dt

        u[i] = Kp * error[i] + Ki * integral + Kd * derivative

        dydt = (-y[i - 1] + K * u[i]) / tau
        y[i] = y[i - 1] + dydt * dt

        prev_error = error[i]

    # Performance Metrics
    overshoot = (max(y) - setpoint) * 100
    steady_state_error = abs(setpoint - y[-1])

    # Settling time (2% criteria)
    settling_time = 0
    for i in range(len(y)):
        if abs(y[i] - setpoint) < 0.02 * setpoint:
            settling_time = t[i]
            break

    st.divider()
    st.subheader("📈 Step Response")

    fig, ax = plt.subplots()
    ax.plot(t, y, label="Process Output")
    ax.axhline(setpoint, linestyle='--', label="Setpoint")
    ax.set_xlabel("Time")
    ax.set_ylabel("Output")
    ax.legend()
    st.pyplot(fig)

    st.subheader("📊 Performance Metrics")
    st.write(f"Overshoot: {round(overshoot, 2)} %")
    st.write(f"Settling Time: {round(settling_time, 2)} s")
    st.write(f"Steady-State Error: {round(steady_state_error, 4)}")

    st.markdown("### 🧠 Interpretation")

    if overshoot > 30:
        st.warning("System is too aggressive. Reduce Kp or Kd.")
    elif steady_state_error > 0.05:
        st.warning("Integral action may be insufficient.")
    else:
        st.success("Good tuning performance.")

    st.caption("Advanced Process Control Educational Tool")


if __name__ == "__main__":
    run()
