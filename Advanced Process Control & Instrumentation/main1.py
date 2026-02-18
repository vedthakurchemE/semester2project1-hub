import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm


def run(uploaded_data=None):

    st.title("📊 Statistical Inference & DOE Suite")

    tool = st.selectbox("Select Tool", [
        "ANOVA – Reactor Yield Comparison",
        "Confidence Interval Estimator",
        "Hypothesis Testing for Process Improvement",
        "Regression – Heat Transfer Coefficient",
        "Residual Analysis Tool",
        "Multicollinearity Detection",
        "Monte Carlo Simulation – Process Variability",
        "Control Chart (SPC) Dashboard",
        "Response Surface Optimization",
        "Taguchi Method Optimization"
    ])

    # ==========================================================
    # 1️⃣ ANOVA
    # ==========================================================
    if tool == "ANOVA – Reactor Yield Comparison":

        group1 = np.random.normal(80, 3, 20)
        group2 = np.random.normal(85, 4, 20)
        group3 = np.random.normal(82, 5, 20)

        F, p = stats.f_oneway(group1, group2, group3)

        st.write(f"F-statistic: {round(F,3)}")
        st.write(f"p-value: {round(p,5)}")

        if p < 0.05:
            st.success("Significant difference between reactor yields")
        else:
            st.warning("No significant difference detected")

        return {}, {"F": F, "p_value": p}

    # ==========================================================
    # 2️⃣ CONFIDENCE INTERVAL
    # ==========================================================
    elif tool == "Confidence Interval Estimator":

        mean = st.number_input("Sample Mean", value=100.0)
        std = st.number_input("Sample Std Dev", value=5.0)
        n = st.number_input("Sample Size", value=20)

        alpha = 0.05
        t_crit = stats.t.ppf(1 - alpha/2, df=n-1)
        margin = t_crit * std / np.sqrt(n)

        lower = mean - margin
        upper = mean + margin

        st.write(f"95% CI: ({round(lower,3)}, {round(upper,3)})")

        return {}, {"Lower": lower, "Upper": upper}

    # ==========================================================
    # 3️⃣ HYPOTHESIS TESTING
    # ==========================================================
    elif tool == "Hypothesis Testing for Process Improvement":

        before = np.random.normal(75, 4, 25)
        after = np.random.normal(80, 4, 25)

        t_stat, p = stats.ttest_ind(before, after)

        st.write(f"T-statistic: {round(t_stat,3)}")
        st.write(f"p-value: {round(p,5)}")

        if p < 0.05:
            st.success("Improvement statistically significant")
        else:
            st.warning("No significant improvement")

        return {}, {"t_stat": t_stat, "p_value": p}

    # ==========================================================
    # 4️⃣ REGRESSION MODEL
    # ==========================================================
    elif tool == "Regression – Heat Transfer Coefficient":

        X = np.linspace(1, 10, 50)
        Y = 5*X + np.random.normal(0, 5, 50)

        model = LinearRegression()
        model.fit(X.reshape(-1,1), Y)
        Y_pred = model.predict(X.reshape(-1,1))

        fig, ax = plt.subplots()
        ax.scatter(X, Y)
        ax.plot(X, Y_pred)
        st.pyplot(fig)

        return {}, {"Slope": model.coef_[0]}

    # ==========================================================
    # 5️⃣ RESIDUAL ANALYSIS
    # ==========================================================
    elif tool == "Residual Analysis Tool":

        X = np.linspace(0, 10, 50)
        Y = 3*X + np.random.normal(0, 2, 50)

        model = LinearRegression()
        model.fit(X.reshape(-1,1), Y)
        Y_pred = model.predict(X.reshape(-1,1))

        residuals = Y - Y_pred

        fig, ax = plt.subplots()
        ax.scatter(Y_pred, residuals)
        ax.axhline(0)
        st.pyplot(fig)

        return {}, {"Residual Mean": np.mean(residuals)}

    # ==========================================================
    # 6️⃣ MULTICOLLINEARITY (VIF)
    # ==========================================================
    elif tool == "Multicollinearity Detection":

        df = pd.DataFrame({
            "X1": np.random.rand(100),
            "X2": np.random.rand(100)*0.8,
            "X3": np.random.rand(100)*1.2
        })

        vif_data = pd.DataFrame()
        vif_data["Variable"] = df.columns
        vif_data["VIF"] = [
            variance_inflation_factor(df.values, i)
            for i in range(df.shape[1])
        ]

        st.dataframe(vif_data)

        return {}, {"VIF": vif_data.to_dict()}

    # ==========================================================
    # 7️⃣ MONTE CARLO
    # ==========================================================
    elif tool == "Monte Carlo Simulation – Process Variability":

        samples = np.random.normal(100, 10, 10000)

        fig, ax = plt.subplots()
        ax.hist(samples, bins=50)
        st.pyplot(fig)

        return {}, {"Mean": np.mean(samples)}

    # ==========================================================
    # 8️⃣ CONTROL CHART
    # ==========================================================
    elif tool == "Control Chart (SPC) Dashboard":

        data = np.random.normal(50, 2, 100)

        mean = np.mean(data)
        std = np.std(data)

        UCL = mean + 3*std
        LCL = mean - 3*std

        fig, ax = plt.subplots()
        ax.plot(data)
        ax.axhline(UCL)
        ax.axhline(LCL)
        ax.axhline(mean)
        st.pyplot(fig)

        return {}, {"UCL": UCL, "LCL": LCL}

    # ==========================================================
    # 9️⃣ RESPONSE SURFACE
    # ==========================================================
    elif tool == "Response Surface Optimization":

        x = np.linspace(-5,5,50)
        y = np.linspace(-5,5,50)
        X, Y = np.meshgrid(x,y)
        Z = -X**2 - Y**2 + 10

        fig, ax = plt.subplots()
        contour = ax.contourf(X, Y, Z)
        st.pyplot(fig)

        return {}, {"Max Response": np.max(Z)}

    # ==========================================================
    # 🔟 TAGUCHI
    # ==========================================================
    elif tool == "Taguchi Method Optimization":

        levels = np.array([10, 20, 30])
        sn_ratio = -10 * np.log10(np.var(levels))

        st.write(f"Signal-to-Noise Ratio: {round(sn_ratio,3)}")

        return {}, {"SNR": sn_ratio}
