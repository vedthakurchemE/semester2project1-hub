import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def run():

    st.title("📈 Hypothesis Testing for Process Improvement")

    st.write("Test whether process modification improved performance.")

    # ==========================================
    # Data Input
    # ==========================================

    st.sidebar.header("Data Source")
    input_method = st.sidebar.radio(
        "Select Data Type",
        ["Simulated Data", "Manual Entry"]
    )

    if input_method == "Simulated Data":

        np.random.seed(1)

        old_process = np.random.normal(85, 2, 30)
        new_process = np.random.normal(88, 2, 30)

    else:

        old_input = st.text_input("Old Process Data (comma-separated)", "85,84,86,87,83")
        new_input = st.text_input("New Process Data (comma-separated)", "88,87,89,90,86")

        old_process = np.array(list(map(float, old_input.split(","))))
        new_process = np.array(list(map(float, new_input.split(","))))

    # ==========================================
    # Descriptive Statistics
    # ==========================================

    st.subheader("📊 Summary Statistics")

    st.write(f"Old Mean: {np.mean(old_process):.2f}")
    st.write(f"New Mean: {np.mean(new_process):.2f}")

    # ==========================================
    # Normality Check
    # ==========================================

    st.subheader("🔍 Normality Test (Shapiro-Wilk)")

    p_old = stats.shapiro(old_process)[1]
    p_new = stats.shapiro(new_process)[1]

    st.write(f"Old Process p-value: {p_old:.4f}")
    st.write(f"New Process p-value: {p_new:.4f}")

    # ==========================================
    # Independent T-Test
    # ==========================================

    st.subheader("📈 Hypothesis Test Results")

    t_stat, p_value = stats.ttest_ind(new_process, old_process)

    # One-tailed adjustment
    p_value_one_tailed = p_value / 2

    st.write(f"T-statistic: {t_stat:.4f}")
    st.write(f"One-tailed P-value: {p_value_one_tailed:.6f}")

    alpha = 0.05

    if p_value_one_tailed < alpha and t_stat > 0:
        st.success("Statistically Significant Improvement Detected")
    else:
        st.warning("No Significant Improvement Detected")

    # ==========================================
    # Confidence Interval
    # ==========================================

    st.subheader("📐 95% Confidence Interval for Mean Difference")

    diff = np.mean(new_process) - np.mean(old_process)
    se = np.sqrt(
        np.var(new_process, ddof=1)/len(new_process) +
        np.var(old_process, ddof=1)/len(old_process)
    )

    ci_low = diff - 1.96*se
    ci_high = diff + 1.96*se

    st.write(f"Mean Difference: {diff:.4f}")
    st.write(f"95% CI: ({ci_low:.4f}, {ci_high:.4f})")

    # ==========================================
    # Visualization
    # ==========================================

    st.subheader("📦 Distribution Comparison")

    fig, ax = plt.subplots()
    ax.boxplot([old_process, new_process])
    ax.set_xticklabels(["Old", "New"])
    st.pyplot(fig)

if __name__ == "__main__":
    run()
