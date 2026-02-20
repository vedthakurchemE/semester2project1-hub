import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def run():

    st.title("🎲 Monte Carlo Simulation for Process Variability")

    st.write("Quantify uncertainty in reactor conversion.")

    # ==========================================
    # Input Parameters
    # ==========================================

    st.sidebar.header("Uncertain Parameters")

    mu_k = st.sidebar.slider("Mean Rate Constant (k)", 0.1, 2.0, 1.0)
    sigma_k = st.sidebar.slider("Std Dev of k", 0.01, 0.5, 0.1)

    mu_tau = st.sidebar.slider("Mean Residence Time (τ)", 0.5, 5.0, 2.0)
    sigma_tau = st.sidebar.slider("Std Dev of τ", 0.01, 0.5, 0.2)

    N = st.sidebar.slider("Number of Simulations", 1000, 50000, 10000)

    # ==========================================
    # Monte Carlo Simulation
    # ==========================================

    np.random.seed(42)

    k_samples = np.random.normal(mu_k, sigma_k, N)
    tau_samples = np.random.normal(mu_tau, sigma_tau, N)

    # Avoid negative physical values
    k_samples = np.clip(k_samples, 0, None)
    tau_samples = np.clip(tau_samples, 0, None)

    conversion = (k_samples * tau_samples) / (1 + k_samples * tau_samples)

    # ==========================================
    # Statistical Results
    # ==========================================

    mean_conv = np.mean(conversion)
    std_conv = np.std(conversion)

    st.subheader("📊 Statistical Results")

    st.write(f"Mean Conversion: {mean_conv:.4f}")
    st.write(f"Std Deviation: {std_conv:.4f}")

    # Probability of low conversion
    threshold = 0.7
    prob_failure = np.mean(conversion < threshold)

    st.write(f"Probability Conversion < {threshold}: {prob_failure:.4f}")

    # ==========================================
    # Visualization
    # ==========================================

    st.subheader("📈 Conversion Distribution")

    fig, ax = plt.subplots()
    ax.hist(conversion, bins=50, density=True)
    ax.set_xlabel("Conversion")
    ax.set_ylabel("Probability Density")
    st.pyplot(fig)

    # ==========================================
    # Confidence Interval
    # ==========================================

    ci_low = np.percentile(conversion, 2.5)
    ci_high = np.percentile(conversion, 97.5)

    st.subheader("📐 95% Confidence Interval")
    st.write(f"({ci_low:.4f}, {ci_high:.4f})")

if __name__ == "__main__":
    run()
