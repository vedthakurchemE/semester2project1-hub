import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

def run():

    st.title("⚙️ Control Loop Fault Detection System")

    # ==========================================
    # Process & Controller Definition
    # ==========================================

    Gp = ctrl.TransferFunction([1], [5, 1])  # First-order plant

    Kp = st.sidebar.slider("Kp", 0.1, 10.0, 2.0)
    Ki = st.sidebar.slider("Ki", 0.1, 5.0, 1.0)

    Gc = ctrl.TransferFunction([Kp, Ki], [1, 0])  # PI Controller

    T = ctrl.feedback(Gc * Gp, 1)

    # ==========================================
    # Fault Injection
    # ==========================================

    fault_type = st.sidebar.selectbox(
        "Select Fault Type",
        ["No Fault", "Sensor Bias", "Sensor Drift", "Actuator Saturation"]
    )

    t = np.linspace(0, 50, 1000)
    t, y = ctrl.step_response(T, t)

    y_faulty = y.copy()

    if fault_type == "Sensor Bias":
        y_faulty += 0.5

    elif fault_type == "Sensor Drift":
        y_faulty += 0.01 * t

    elif fault_type == "Actuator Saturation":
        y_faulty = np.clip(y_faulty, 0, 0.8)

    # ==========================================
    # Residual Calculation
    # ==========================================

    residual = y_faulty - y

    threshold = 3 * np.std(residual[:100])

    fault_detected = np.any(np.abs(residual) > threshold)

    # ==========================================
    # Plot Results
    # ==========================================

    st.subheader("Output Response")

    fig1, ax1 = plt.subplots()
    ax1.plot(t, y, label="Nominal Output")
    ax1.plot(t, y_faulty, '--', label="Measured Output")
    ax1.legend()
    st.pyplot(fig1)

    st.subheader("Residual Signal")

    fig2, ax2 = plt.subplots()
    ax2.plot(t, residual)
    ax2.axhline(threshold, linestyle='--')
    ax2.axhline(-threshold, linestyle='--')
    ax2.set_title("Residual Monitoring")
    st.pyplot(fig2)

    # ==========================================
    # Detection Result
    # ==========================================

    if fault_detected:
        st.error("Fault Detected in Control Loop")
    else:
        st.success("System Operating Normally")

if __name__ == "__main__":
    run()
