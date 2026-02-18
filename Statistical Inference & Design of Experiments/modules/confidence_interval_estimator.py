import streamlit as st
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

def run():

    st.title("📊 Confidence Interval Estimator for Plant Data")

    st.write("Estimate Confidence Intervals for Process Parameters")

    # ==========================================
    # Data Input
    # ==========================================

    st.subheader("Enter Sample Data")

    sample_size = st.number_input("Sample Size (n)", min_value=2, value=20)
    sample_mean = st.number_input("Sample Mean", value=100.0)
    sample_std = st.number_input("Sample Standard Deviation (s)", value=5.0)

    confidence_level = st.selectbox(
        "Confidence Level",
        [0.90, 0.95, 0.99],
        index=1
    )

    alpha = 1 - confidence_level

    # ==========================================
    # t-Distribution CI
    # ==========================================

    t_critical = stats.t.ppf(1 - alpha/2, df=sample_size-1)

    margin_error = t_critical * sample_std / np.sqrt(sample_size)

    lower = sample_mean - margin_error
    upper = sample_mean + margin_error

    st.subheader("📈 Confidence Interval Result")

    st.write(f"{confidence_level*100:.0f}% CI:")
    st.write(f"Lower Bound: {lower:.4f}")
    st.write(f"Upper Bound: {upper:.4f}")

    st.write(f"Margin of Error: ±{margin_error:.4f}")

    # ==========================================
    # Visualization
    # ==========================================

    fig, ax = plt.subplots()

    ax.axvline(sample_mean)
    ax.axvline(lower)
    ax.axvline(upper)

    ax.set_title("Confidence Interval")
    ax.set_yticks([])
    ax.set_xlabel("Process Mean")

    st.pyplot(fig)

    # ==========================================
    # Interpretation
    # ==========================================

    st.subheader("Interpretation")

    st.write(f"""
    We are {confidence_level*100:.0f}% confident that the true process mean
    lies between {lower:.4f} and {upper:.4f}.
    """)

if __name__ == "__main__":
    run()
