import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def run():

    st.title("🔥 Nonlinear CSTR Temperature Control")

    # ===============================
    # Process Parameters
    # ===============================
    st.subheader("Process Parameters")

    F = st.number_input("Flow rate (m3/min)", value=1.0)
    V = st.number_input("Reactor volume (m3)", value=1.0)
    CA0 = st.number_input("Feed concentration (mol/m3)", value=1.0)
    T0 = st.number_input("Feed temperature (K)", value=350.0)

    k0 = 7.2e10
    E = 8750
    R = 1.987
    dH = -50000
    rho = 1000
    Cp = 0.239
    UA = 5e4

    # ===============================
    # PID Parameters
    # ===============================
    st.subheader("PID Controller")

    T_set = st.number_input("Setpoint Temperature (K)", value=365.0)

    col1, col2, col3 = st.columns(3)
    with col1:
        Kp = st.number_input("Kp", value=10.0)
    with col2:
        Ki = st.number_input("Ki", value=1.0)
    with col3:
        Kd = st.number_input("Kd", value=0.5)

    sim_time = 10
    t = np.linspace(0, sim_time, 1000)

    # ===============================
    # Initial Conditions
    # ===============================
    CA_init = 0.5
    T_init = 350
    integral = 0
    prev_error = 0

    Tc_history = []

    def model(y, t):

        nonlocal integral, prev_error

        CA, T = y

        # Reaction rate
        k = k0 * np.exp(-E/(R*T))
        r = k * CA

        # PID control
        error = T_set - T
        dt = t[1] - t[0] if len(t) > 1 else 0.01
        integral += error * dt
        derivative = (error - prev_error) / dt

        Tc = 300 + Kp*error + Ki*integral + Kd*derivative
        Tc_history.append(Tc)

        prev_error = error

        dCA_dt = (F/V)*(CA0 - CA) - r

        dT_dt = (F/V)*(T0 - T) \
                + (-dH/(rho*Cp))*r \
                - (UA/(rho*Cp*V))*(T - Tc)

        return [dCA_dt, dT_dt]

    sol = odeint(model, [CA_init, T_init], t)

    CA = sol[:,0]
    T = sol[:,1]

    # ===============================
    # Plot Results
    # ===============================
    st.subheader("Temperature Response")

    fig, ax = plt.subplots()
    ax.plot(t, T, label="Reactor Temp")
    ax.axhline(T_set, linestyle="--", label="Setpoint")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (K)")
    ax.legend()
    st.pyplot(fig)

    st.subheader("Coolant Temperature")
    fig2, ax2 = plt.subplots()
    ax2.plot(Tc_history)
    ax2.set_ylabel("Coolant Temp (K)")
    st.pyplot(fig2)

if __name__ == "__main__":
    run()
