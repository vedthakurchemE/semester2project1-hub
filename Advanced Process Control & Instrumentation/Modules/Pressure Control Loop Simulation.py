import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, bode
from scipy.integrate import odeint

def run():

    st.title("⚙️ Pressure Control Loop Simulation")

    # ==============================
    # Process Parameters
    # ==============================
    st.subheader("Process Parameters")

    V = st.number_input("Vessel Volume (m3)", value=5.0)
    R = 8.314
    T = st.number_input("Gas Temperature (K)", value=350.0)
    Cv = st.number_input("Valve Coefficient (Cv)", value=0.5)

    q_in = st.number_input("Inlet Flow (mol/s)", value=10.0)

    P_set = st.number_input("Pressure Setpoint (bar)", value=5.0)

    # ==============================
    # PID Parameters
    # ==============================
    st.subheader("PID Parameters")

    col1, col2, col3 = st.columns(3)
    with col1:
        Kp = st.number_input("Kp", value=2.0)
    with col2:
        Ki = st.number_input("Ki", value=0.5)
    with col3:
        Kd = st.number_input("Kd", value=0.1)

    sim_time = 50
    t = np.linspace(0, sim_time, 1000)

    # ==============================
    # Initial Conditions
    # ==============================
    P0 = 2.0
    integral = 0
    prev_error = 0
    valve_history = []

    def model(P, t):

        nonlocal integral, prev_error

        P = max(P, 0.1)  # avoid sqrt issues

        # PID
        error = P_set - P
        dt = t[1] - t[0] if len(t) > 1 else 0.01

        integral += error * dt
        derivative = (error - prev_error) / dt

        u = Kp*error + Ki*integral + Kd*derivative

        # Saturation
        u = max(0, min(1, u))

        valve_history.append(u)

        q_out = Cv * u * np.sqrt(P)

        dP_dt = (R*T/V)*(q_in - q_out)

        prev_error = error

        return dP_dt

    P = odeint(model, P0, t)

    # ==============================
    # Plot Pressure Response
    # ==============================
    st.subheader("Pressure Response")

    fig, ax = plt.subplots()
    ax.plot(t, P)
    ax.axhline(P_set, linestyle='--', label="Setpoint")
    ax.set_xlabel("Time")
    ax.set_ylabel("Pressure (bar)")
    ax.legend()
    st.pyplot(fig)

    # ==============================
    # Valve Position
    # ==============================
    st.subheader("Valve Opening")

    fig2, ax2 = plt.subplots()
    ax2.plot(valve_history)
    ax2.set_ylabel("Valve Opening (0–1)")
    st.pyplot(fig2)

    # ==============================
    # Linearized Bode Plot
    # ==============================
    st.subheader("Linearized Open-Loop Bode Plot")

    # Linearization around steady-state
    K_process = (R*T/V)*Cv*np.sqrt(P_set)
    tau = V/(R*T)

    num = [K_process]
    den = [tau, 1]

    system = TransferFunction(num, den)

    w, mag, phase = bode(system)

    fig3, ax3 = plt.subplots()
    ax3.semilogx(w, mag)
    ax3.set_title("Bode Magnitude")
    st.pyplot(fig3)

    fig4, ax4 = plt.subplots()
    ax4.semilogx(w, phase)
    ax4.set_title("Bode Phase")
    st.pyplot(fig4)

if __name__ == "__main__":
    run()
