import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run():

    st.title("📈 Statistical Process Control (SPC) Dashboard")

    st.write("Monitor process stability using Individuals Control Chart.")

    # ==========================================
    # Data Input
    # ==========================================

    st.sidebar.header("Data Source")

    input_method = st.sidebar.radio(
        "Select Data Type",
        ["Simulated Data", "Manual Entry"]
    )

    if input_method == "Simulated Data":

        np.random.seed(42)

        data = np.random.normal(100, 2, 50)

        # Inject special cause
        data[35] += 8

    else:

        user_input = st.text_input(
            "Enter comma-separated values",
            "100,102,101,99,98,100,101"
        )

        data = np.array(list(map(float, user_input.split(","))))

    # ==========================================
    # SPC Calculations
    # ==========================================

    mean = np.mean(data)

    moving_range = np.abs(np.diff(data))
    MR_bar = np.mean(moving_range)

    sigma = MR_bar / 1.128

    UCL = mean + 3*sigma
    LCL = mean - 3*sigma

    # ==========================================
    # Plot Control Chart
    # ==========================================

    st.subheader("📊 Individuals Control Chart")

    fig, ax = plt.subplots()
    ax.plot(data, marker='o')
    ax.axhline(mean, linestyle='--')
    ax.axhline(UCL, linestyle='--')
    ax.axhline(LCL, linestyle='--')
    ax.set_xlabel("Sample")
    ax.set_ylabel("Process Value")
    st.pyplot(fig)

    # ==========================================
    # Out-of-Control Detection
    # ==========================================

    st.subheader("🚨 SPC Rule Violations")

    violations = []

    # Rule 1: Point beyond 3 sigma
    out_of_control = np.where((data > UCL) | (data < LCL))[0]

    if len(out_of_control) > 0:
        violations.append("Point beyond control limits")

    # Rule 2: 7 consecutive points on one side of mean
    above_mean = data > mean
    run_length = 0

    for val in above_mean:
        if val:
            run_length += 1
        else:
            run_length = 0
        if run_length >= 7:
            violations.append("7 consecutive points above mean")
            break

    if violations:
        for v in violations:
            st.error(v)
    else:
        st.success("Process is statistically in control")

    # ==========================================
    # Summary Statistics
    # ==========================================

    st.subheader("📋 Process Statistics")

    st.write(f"Mean: {mean:.4f}")
    st.write(f"Estimated Sigma: {sigma:.4f}")
    st.write(f"UCL: {UCL:.4f}")
    st.write(f"LCL: {LCL:.4f}")

if __name__ == "__main__":
    run()
