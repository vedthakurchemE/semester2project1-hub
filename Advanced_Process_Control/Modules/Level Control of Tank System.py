import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def run():

    st.title("💧 Tank Level Control System")

    # ==============================
    # Process Parameters
    # ==============================
    st.subheader("Tank Parameters")

    A = st.number_input("Tank Cross-Section Area (m2)", value=5.0)
    Cd = st.number_input("Discharge Coefficient", value=1.0)

    h_set = st.number_input("Level Setpoint (m)", value=2.0)

    disturbance = st.checkbox("Enable Inlet Disturbance")

    # ==============================
    # PID Parameters
    # ==============================
    st.subheader("PID Controller")

    col1, col2, col3 = st.columns(3)
    with col1:
        Kp = st.number_input("Kp", value=5.0)
    with col2:
        Ki = st.number_input("Ki", value=0.5)
    with col3:
        Kd = st.number_input("Kd", value=0.1)

    sim_time = 100
    t = np.linspace(0, sim_time, 1000)

    # ==============================
    # Initial Conditions
    # ==============================
    h0 = 0.5
    integral = 0
    prev_error = 0
    qin_history = []

    def model(h, t):

        nonlocal integral, prev_error

        h = max(h, 0.001)

        # Disturbance
        q_dist = 1.0
        if disturbance and t > sim_time/2:
            q_dist = 0.5

        # PID
        error = h_set - h
        dt = t[1] - t[0] if len(t) > 1 else 0.01

        integral += error * dt
        derivative = (error - prev_error) / dt

        q_in = Kp*error + Ki*integral + Kd*derivative + q_dist

        # Actuator saturation
        q_in = max(0, min(10, q_in))

        qin_history.append(q_in)

        dh_dt = (1/A)*(q_in - Cd*np.sqrt(h))

        prev_error = error

        return dh_dt

    h = odeint(model, h0, t)

    # ==============================
    # Plot Level Response
    # ==============================
    st.subheader("Level Response")

    fig, ax = plt.subplots()
    ax.plot(t, h, label="Tank Level")
    ax.axhline(h_set, linestyle='--', label="Setpoint")
    ax.set_xlabel("Time")
    ax.set_ylabel("Level (m)")
    ax.legend()
    st.pyplot(fig)

    # ==============================
    # Inlet Flow
    # ==============================
    st.subheader("Inlet Flow (Control Action)")

    fig2, ax2 = plt.subplots()
    ax2.plot(qin_history)
    ax2.set_ylabel("Inlet Flow")
    st.pyplot(fig2)

    # ==============================
    # Performance Metrics
    # ==============================
    overshoot = max(h)[0] - h_set
    steady_state_error = abs(h[-1][0] - h_set)

    st.subheader("Performance Metrics")
    st.write(f"Overshoot: {round(overshoot,3)} m")
    st.write(f"Steady-State Error: {round(steady_state_error,4)} m")

if __name__ == "__main__":
    run()
