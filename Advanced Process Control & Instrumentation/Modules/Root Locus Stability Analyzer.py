import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

def run():

    st.title("📈 Root Locus Stability Analyzer")

    st.sidebar.header("Transfer Function Input")

    num_input = st.sidebar.text_input(
        "Numerator Coefficients (highest power first)",
        "1"
    )

    den_input = st.sidebar.text_input(
        "Denominator Coefficients (highest power first)",
        "1 3 2"
    )

    try:
        num = list(map(float, num_input.split()))
        den = list(map(float, den_input.split()))

        G = ctrl.TransferFunction(num, den)

        st.subheader("Transfer Function")
        st.write(G)

        # ==========================================
        # Root Locus Plot
        # ==========================================
        st.subheader("Root Locus Plot")

        fig, ax = plt.subplots()
        ctrl.root_locus(G, ax=ax, grid=True)
        st.pyplot(fig)

        # ==========================================
        # Poles and Zeros
        # ==========================================
        st.subheader("Open Loop Poles & Zeros")

        poles = ctrl.pole(G)
        zeros = ctrl.zero(G)

        st.write("Poles:", poles)
        st.write("Zeros:", zeros)

        # ==========================================
        # Gain Selection
        # ==========================================
        st.subheader("Closed Loop Analysis")

        K = st.slider("Select Gain K", 0.0, 100.0, 1.0)

        T = ctrl.feedback(K*G, 1)
        cl_poles = ctrl.pole(T)

        st.write("Closed Loop Poles:", cl_poles)

        if np.all(np.real(cl_poles) < 0):
            st.success("System is Stable for this Gain")
        else:
            st.error("System is Unstable for this Gain")

        # ==========================================
        # Step Response
        # ==========================================
        st.subheader("Step Response")

        t, y = ctrl.step_response(T)

        fig2, ax2 = plt.subplots()
        ax2.plot(t, y)
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Output")
        ax2.set_title("Closed Loop Step Response")
        st.pyplot(fig2)

    except:
        st.error("Invalid transfer function coefficients")

if __name__ == "__main__":
    run()
