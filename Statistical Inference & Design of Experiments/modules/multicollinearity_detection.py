import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from numpy.linalg import cond

def run():

    st.title("📊 Multicollinearity Detection in Process Variables")

    st.write("Detect correlation issues among process input variables.")

    # ==========================================
    # Generate Simulated Process Data
    # ==========================================

    np.random.seed(42)

    temperature = np.random.normal(200, 5, 100)
    pressure = temperature * 0.05 + np.random.normal(10, 0.5, 100)  # correlated
    flow = np.random.normal(50, 3, 100)
    feed_rate = flow * 1.2 + np.random.normal(5, 0.2, 100)  # correlated

    df = pd.DataFrame({
        "Temperature": temperature,
        "Pressure": pressure,
        "Flow": flow,
        "Feed_Rate": feed_rate
    })

    st.subheader("📋 Data Preview")
    st.write(df.head())

    # ==========================================
    # Correlation Matrix
    # ==========================================

    st.subheader("🔍 Correlation Matrix")

    corr = df.corr()

    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # ==========================================
    # VIF Calculation
    # ==========================================

    st.subheader("📈 Variance Inflation Factor (VIF)")

    X = sm.add_constant(df)

    vif_data = pd.DataFrame()
    vif_data["Variable"] = X.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X.values, i)
        for i in range(X.shape[1])
    ]

    st.write(vif_data)

    # ==========================================
    # Condition Number
    # ==========================================

    st.subheader("📐 Condition Number")

    condition_number = cond(X)
    st.write(f"Condition Number: {condition_number:.2f}")

    if condition_number > 100:
        st.error("Severe multicollinearity detected")
    elif condition_number > 30:
        st.warning("Moderate multicollinearity detected")
    else:
        st.success("No serious multicollinearity detected")

if __name__ == "__main__":
    run()
