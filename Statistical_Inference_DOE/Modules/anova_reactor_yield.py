import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

def run():

    st.title("🧪 ANOVA: Reactor Yield Comparison")

    st.write("Compare mean yields across multiple reactors.")

    # ==========================================
    # Data Input
    # ==========================================

    st.sidebar.header("Input Method")
    input_method = st.sidebar.radio(
        "Select Data Source",
        ["Simulated Data", "Manual Entry"]
    )

    if input_method == "Simulated Data":

        np.random.seed(42)

        reactor_A = np.random.normal(85, 2, 20)
        reactor_B = np.random.normal(88, 2, 20)
        reactor_C = np.random.normal(86, 2, 20)

    else:

        st.write("Enter comma-separated yield values")

        A_input = st.text_input("Reactor A", "85,84,86,87,83")
        B_input = st.text_input("Reactor B", "88,87,89,90,86")
        C_input = st.text_input("Reactor C", "86,85,87,84,88")

        reactor_A = np.array(list(map(float, A_input.split(","))))
        reactor_B = np.array(list(map(float, B_input.split(","))))
        reactor_C = np.array(list(map(float, C_input.split(","))))

    # ==========================================
    # Combine Data
    # ==========================================

    df = pd.DataFrame({
        "Yield": np.concatenate([reactor_A, reactor_B, reactor_C]),
        "Reactor": (["A"]*len(reactor_A) +
                    ["B"]*len(reactor_B) +
                    ["C"]*len(reactor_C))
    })

    # ==========================================
    # Descriptive Statistics
    # ==========================================

    st.subheader("📊 Descriptive Statistics")
    st.write(df.groupby("Reactor").describe())

    # ==========================================
    # Boxplot
    # ==========================================

    st.subheader("📦 Yield Distribution")

    fig, ax = plt.subplots()
    df.boxplot(column="Yield", by="Reactor", ax=ax)
    plt.suptitle("")
    st.pyplot(fig)

    # ==========================================
    # One-Way ANOVA
    # ==========================================

    st.subheader("📈 One-Way ANOVA Results")

    f_stat, p_value = stats.f_oneway(reactor_A, reactor_B, reactor_C)

    st.write(f"F-statistic: {f_stat:.4f}")
    st.write(f"P-value: {p_value:.6f}")

    alpha = 0.05

    if p_value < alpha:
        st.error("Reject Null Hypothesis: Significant difference detected")
    else:
        st.success("Fail to Reject Null Hypothesis: No significant difference")

    # ==========================================
    # ANOVA Table (Detailed)
    # ==========================================

    model = ols('Yield ~ C(Reactor)', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    st.subheader("📋 ANOVA Table")
    st.write(anova_table)

if __name__ == "__main__":
    run()
