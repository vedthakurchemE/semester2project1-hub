import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run():

    st.title("📊 Taguchi Method Optimization")

    st.write("Robust Design using L9 Orthogonal Array")

    # ==========================================
    # Define L9 Orthogonal Array
    # ==========================================

    L9 = np.array([
        [1,1,1],
        [1,2,2],
        [1,3,3],
        [2,1,2],
        [2,2,3],
        [2,3,1],
        [3,1,3],
        [3,2,1],
        [3,3,2]
    ])

    df = pd.DataFrame(L9, columns=["Temperature", "Pressure", "Catalyst"])

    # ==========================================
    # Simulated Yield (Example Model)
    # ==========================================

    np.random.seed(1)

    yield_values = (
        70
        + df["Temperature"]*5
        + df["Pressure"]*3
        + df["Catalyst"]*4
        + np.random.normal(0, 2, 9)
    )

    df["Yield"] = yield_values

    st.subheader("📋 Experimental Results")
    st.write(df)

    # ==========================================
    # S/N Ratio Calculation (Higher is Better)
    # ==========================================

    sn_ratio = -10 * np.log10(1 / (df["Yield"]**2))

    df["S/N Ratio"] = sn_ratio

    st.subheader("📈 S/N Ratios")
    st.write(df)

    # ==========================================
    # Factor Effect Analysis
    # ==========================================

    st.subheader("📊 Factor Effects on S/N Ratio")

    factor_effects = {}

    for factor in ["Temperature", "Pressure", "Catalyst"]:
        means = df.groupby(factor)["S/N Ratio"].mean()
        factor_effects[factor] = means

        fig, ax = plt.subplots()
        means.plot(marker='o', ax=ax)
        ax.set_title(f"{factor} Effect")
        ax.set_ylabel("Mean S/N Ratio")
        st.pyplot(fig)

    # ==========================================
    # Optimal Levels
    # ==========================================

    st.subheader("🎯 Optimal Parameter Levels")

    optimal_levels = {}

    for factor in factor_effects:
        optimal_levels[factor] = factor_effects[factor].idxmax()

    for factor, level in optimal_levels.items():
        st.write(f"Optimal {factor}: Level {level}")

if __name__ == "__main__":
    run()
