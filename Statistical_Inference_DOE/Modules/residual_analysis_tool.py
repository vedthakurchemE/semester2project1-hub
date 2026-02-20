import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

def run():

    st.title("📊 Residual Analysis Tool")

    st.write("Regression Assumption Diagnostics")

    # ==========================================
    # Generate Sample Data (Replace with real)
    # ==========================================

    np.random.seed(42)

    X = np.linspace(0, 10, 50)
    noise = np.random.normal(0, 2, 50)
    Y = 3*X + 5 + noise

    df = pd.DataFrame({"X": X, "Y": Y})

    # ==========================================
    # Fit Regression Model
    # ==========================================

    model = LinearRegression()
    model.fit(df[["X"]], df["Y"])

    Y_pred = model.predict(df[["X"]])
    residuals = df["Y"] - Y_pred

    df["Predicted"] = Y_pred
    df["Residuals"] = residuals

    st.subheader("📋 Model Results")
    st.write(f"Intercept: {model.intercept_:.3f}")
    st.write(f"Slope: {model.coef_[0]:.3f}")

    # ==========================================
    # 1️⃣ Residuals vs Fitted
    # ==========================================

    st.subheader("Residuals vs Fitted")

    fig1, ax1 = plt.subplots()
    ax1.scatter(Y_pred, residuals)
    ax1.axhline(0)
    ax1.set_xlabel("Fitted Values")
    ax1.set_ylabel("Residuals")
    st.pyplot(fig1)

    # ==========================================
    # 2️⃣ Histogram
    # ==========================================

    st.subheader("Residual Histogram")

    fig2, ax2 = plt.subplots()
    ax2.hist(residuals, bins=10)
    ax2.set_title("Residual Distribution")
    st.pyplot(fig2)

    # ==========================================
    # 3️⃣ Q-Q Plot
    # ==========================================

    st.subheader("Q-Q Plot")

    fig3 = sm.qqplot(residuals, line='s')
    st.pyplot(fig3)

    # ==========================================
    # 4️⃣ Residuals vs Order
    # ==========================================

    st.subheader("Residuals vs Observation Order")

    fig4, ax4 = plt.subplots()
    ax4.plot(residuals, marker='o')
    ax4.axhline(0)
    ax4.set_xlabel("Observation Index")
    ax4.set_ylabel("Residual")
    st.pyplot(fig4)

    # ==========================================
    # Statistical Tests
    # ==========================================

    st.subheader("Statistical Tests")

    # Shapiro-Wilk
    shapiro_stat, shapiro_p = stats.shapiro(residuals)
    st.write(f"Shapiro-Wilk p-value: {shapiro_p:.4f}")

    # Durbin-Watson
    dw = sm.stats.stattools.durbin_watson(residuals)
    st.write(f"Durbin-Watson statistic: {dw:.3f}")

    # Interpretation
    st.subheader("Interpretation Guide")

    st.write("""
    • Residuals vs Fitted: Should show random scatter  
    • Histogram/Q-Q: Should be approximately normal  
    • Durbin-Watson ≈ 2 → No autocorrelation  
    • Shapiro p > 0.05 → Normality not rejected  
    """)

if __name__ == "__main__":
    run()
