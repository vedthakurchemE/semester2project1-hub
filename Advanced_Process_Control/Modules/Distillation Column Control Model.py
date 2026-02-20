import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():

    st.title("🏭 Distillation Column Composition Control")

    # ============================
    # Process Parameters
    # ============================
    st.subheader("Column Dynamics (FOPDT Model)")

    K = st.number_input("Process Gain (K)", value=0.8)
    tau = st.number_input("Time Constant (τ)", value=10.0)
    L = st.number_input("Dead Time (L)", value=3.0)

    x_set = st.number_input("Top Composition Setpoint", value=0.95)

    disturbance = st.checkbox("Enable Feed Disturbance")

    # ============================
    # PID Controller
    # ============================
    st.subheader("PID Controller")

    col1, col2, col3 = st.columns(3)
    with col1:
        Kp = st.number_input("Kp", value=2.0)
    with col2:
        Ki = st.number_input("Ki", value=0.3)
    with col3:
        Kd = st.number_input("Kd", value=0.1)

    # ============================
    # Simulation Setup
    # ============================
    sim_time = 200
    dt = 0.5
    t = np.arange(0, sim_time, dt)

    x = np.zeros(len(t))
    R = np.zeros(len(t))

    x[0] = 0.9
    integral = 0
    prev_error = 0

    delay_steps = int(L/dt)
    R_buffer = [1.5]*delay_steps

    for i in range(1, len(t)):

        # Disturbance
        feed_dist = 0
        if disturbance and t[i] > sim_time/2:
            feed_dist = -0.05

        # PID
        error = x_set - x[i-1]
        integral += error*dt
        derivative = (error - prev_error)/dt

        R_unbounded = Kp*error + Ki*integral + Kd*derivative + 1.5

        # Reflux ratio limits
        R[i] = max(0.5, min(5.0, R_unbounded))

        # Dead time handling
        R_buffer.append(R[i])
        R_delayed = R_buffer.pop(0)

        # FOPDT dynamic update
        dxdt = ( -x[i-1] + K*(R_delayed) )/tau + feed_dist
        x[i] = x[i-1] + dxdt*dt

        prev_error = error

    # ============================
    # Plot Composition
    # ============================
    st.subheader("Top Composition Response")

    fig, ax = plt.subplots()
    ax.plot(t, x, label="x_D")
    ax.axhline(x_set, linestyle='--', label="Setpoint")
    ax.set_xlabel("Time")
    ax.set_ylabel("Distillate Composition")
    ax.legend()
    st.pyplot(fig)

    # ============================
    # Reflux Ratio
    # ============================
    st.subheader("Reflux Ratio Control Action")

    fig2, ax2 = plt.subplots()
    ax2.plot(t, R)
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Reflux Ratio")
    st.pyplot(fig2)

    # ============================
    # Performance Metrics
    # ============================
    overshoot = max(x) - x_set
    steady_state_error = abs(x[-1] - x_set)

    st.subheader("Performance Metrics")
    st.write(f"Overshoot: {round(overshoot,4)}")
    st.write(f"Steady-State Error: {round(steady_state_error,4)}")

if __name__ == "__main__":
    run()
