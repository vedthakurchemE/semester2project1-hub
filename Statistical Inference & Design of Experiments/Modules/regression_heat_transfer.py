import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import shapiro

def run():

    st.title("🔥 Regression Model for Heat Transfer Coefficient")

    st.write("Model convective heat transfer coefficient using dimensionless correlation.")

    # ==========================================
    # Generate Simulated Experimental Data
    # ==========================================

    np.random.seed(42)

    Re = np.random.uniform(1e4, 1e5, 50)
    Pr = np.random.uniform(0.7, 5, 50)

    # True underlying model (Dittus-Boelter style)
    Nu = 0.023 * (Re**0.8) * (Pr**0.4)

    # Add measurement noise
    Nu = Nu + np.random.normal(0, 0.05*np.mean(Nu), 50)

    # Log transformation
    log_Re = np.log(Re)
    log_Pr = np.log(Pr)
    log_Nu = np.log(Nu)

    df = pd.DataFrame({
        "log_Re": log_Re,
        "log_Pr": log_Pr,
        "log_Nu": log_Nu
    })

    # ==========================================
    # Linear Regression in Log Space
    # ==========================================

    X = df[["log_Re", "log_Pr"]]
    X = sm.add_constant(X)
    y = df["log_Nu"]

    model = sm.OLS(y, X).fit()

    st.subheader("📋 Regression Summary")
    st.text(model.summary())

    # ==========================================
    # Extract Physical Parameters
    # ==========================================

    C = np.exp(model.params[0])
    m = model.params[1]
    n = model.params[2]

    st.subheader("📐 Fitted Correlation")

    st.write(f"Nu = {C:.4f} * Re^{m:.4f} * Pr^{n:.4f}")

    # ==========================================
    # Residual Analysis
    # ==========================================

    residuals = model.resid

    st.subheader("📊 Residual Analysis")

    fig, ax = plt.subplots()
    ax.scatter(model.fittedvalues, residuals)
    ax.axhline(0, linestyle="--")
    ax.set_xlabel("Fitted Values")
    ax.set_ylabel("Residuals")
    st.pyplot(fig)

    # Normality test
    stat, p_value = shapiro(residuals)

    st.write(f"Shapiro-Wilk p-value: {p_value:.4f}")

    if p_value > 0.05:
        st.success("Residuals approximately normal")
    else:
        st.warning("Residuals not normally distributed")

    # ==========================================
    # R² Display
    # ==========================================

    st.subheader("📈 Model Performance")
    st.write(f"R-squared: {model.rsquared:.4f}")
    st.write(f"Adjusted R-squared: {model.rsquared_adj:.4f}")

if __name__ == "__main__":
    run()
