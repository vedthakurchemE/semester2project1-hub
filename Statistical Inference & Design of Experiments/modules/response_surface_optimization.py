import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from statsmodels.formula.api import ols
import statsmodels.api as sm
from scipy.optimize import minimize

def run():

    st.title("📊 Response Surface Optimization")

    st.write("Optimize Reactor Yield using RSM")

    # ==========================================
    # Generate Design of Experiments (DOE)
    # ==========================================

    np.random.seed(1)

    temperature = np.linspace(150, 250, 10)
    pressure = np.linspace(5, 15, 10)

    T, P = np.meshgrid(temperature, pressure)

    # True underlying model (unknown in real life)
    Y = (
        80
        + 0.2*T
        + 0.5*P
        - 0.001*T**2
        - 0.02*P**2
        + 0.01*T*P
        + np.random.normal(0, 2, T.shape)
    )

    df = pd.DataFrame({
        "Temperature": T.flatten(),
        "Pressure": P.flatten(),
        "Yield": Y.flatten()
    })

    # ==========================================
    # Fit Quadratic Model
    # ==========================================

    model = ols(
        "Yield ~ Temperature + Pressure + I(Temperature**2) + I(Pressure**2) + Temperature:Pressure",
        data=df
    ).fit()

    st.subheader("📋 Regression Summary")
    st.text(model.summary())

    # ==========================================
    # 3D Surface Plot
    # ==========================================

    st.subheader("📈 Response Surface")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(T, P, Y, alpha=0.7)
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Pressure")
    ax.set_zlabel("Yield")
    st.pyplot(fig)

    # ==========================================
    # Optimization
    # ==========================================

    st.subheader("🎯 Optimal Operating Conditions")

    def objective(x):
        temp, pres = x
        pred = model.predict(pd.DataFrame({
            "Temperature": [temp],
            "Pressure": [pres]
        }))
        return -pred[0]  # maximize yield

    bounds = [(150, 250), (5, 15)]
    result = minimize(objective, x0=[200, 10], bounds=bounds)

    opt_temp, opt_pres = result.x
    max_yield = -result.fun

    st.write(f"Optimal Temperature: {opt_temp:.2f} °C")
    st.write(f"Optimal Pressure: {opt_pres:.2f} bar")
    st.write(f"Predicted Maximum Yield: {max_yield:.2f}")

    # ==========================================
    # ANOVA Table
    # ==========================================

    st.subheader("📊 ANOVA Table")
    anova_table = sm.stats.anova_lm(model, typ=2)
    st.write(anova_table)

if __name__ == "__main__":
    run()
