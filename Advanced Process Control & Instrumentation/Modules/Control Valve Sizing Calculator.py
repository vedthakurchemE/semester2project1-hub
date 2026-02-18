import streamlit as st
import numpy as np

def run():

    st.title("⚙️ Control Valve Sizing Calculator (ISA-Based)")

    fluid_type = st.selectbox("Fluid Type", ["Liquid", "Gas"])

    st.subheader("Process Conditions")

    Q = st.number_input("Flow Rate (m3/hr)", min_value=0.01, value=10.0)
    P1 = st.number_input("Upstream Pressure (bar)", min_value=0.1, value=5.0)
    P2 = st.number_input("Downstream Pressure (bar)", min_value=0.0, value=3.0)

    dP = P1 - P2

    if dP <= 0:
        st.error("Pressure drop must be positive.")
        return

    SG = st.number_input("Specific Gravity", min_value=0.01, value=1.0)

    # ========================================
    # LIQUID VALVE SIZING
    # ========================================
    if fluid_type == "Liquid":

        Cv = Q / np.sqrt(dP / SG)

        st.subheader("Results (Liquid Valve)")

        st.write(f"Required Cv: {round(Cv,2)}")

        # Valve selection guidance
        if Cv < 5:
            valve_size = "1-inch"
        elif Cv < 20:
            valve_size = "2-inch"
        elif Cv < 50:
            valve_size = "3-inch"
        else:
            valve_size = "Larger than 3-inch"

        st.write(f"Suggested Valve Size: {valve_size}")

    # ========================================
    # GAS VALVE SIZING
    # ========================================
    else:

        T = st.number_input("Temperature (K)", min_value=200.0, value=350.0)

        Cv = Q / (P1 * np.sqrt(dP / (SG * T)))

        st.subheader("Results (Gas Valve)")

        st.write(f"Required Cv: {round(Cv,2)}")

        # Choked flow check (simplified)
        critical_ratio = 0.5
        if (P2/P1) < critical_ratio:
            st.warning("Choked flow condition likely.")
        else:
            st.success("Non-choked flow region.")

    # ========================================
    # Engineering Checks
    # ========================================
    st.divider()
    st.subheader("Engineering Validation")

    if dP > 0.5*P1:
        st.warning("High pressure drop — cavitation or flashing may occur (liquid case).")

    if dP < 0.1:
        st.warning("Very low pressure drop — poor control authority possible.")

if __name__ == "__main__":
    run()
