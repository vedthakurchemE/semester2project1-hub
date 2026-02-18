import streamlit as st

# Import modules from folder
from modules import anova_reactor_yield
from modules import confidence_interval_estimator
from modules import control_chart_spc
from modules import hypothesis_testing_process
from modules import monte_carlo_process
from modules import multicollinearity_detection
from modules import regression_heat_transfer
from modules import residual_analysis_tool
from modules import response_surface_optimization
from modules import taguchi_optimization


def main():

    st.set_page_config(
        page_title="Statistical Inference & DOE Suite",
        layout="wide"
    )

    st.sidebar.title("📊 Statistical Tools")

    tool = st.sidebar.selectbox(
        "Select Analysis Module",
        [
            "ANOVA – Reactor Yield",
            "Confidence Interval Estimator",
            "Control Chart (SPC)",
            "Hypothesis Testing",
            "Monte Carlo Simulation",
            "Multicollinearity Detection",
            "Regression – Heat Transfer",
            "Residual Analysis",
            "Response Surface Optimization",
            "Taguchi Optimization"
        ]
    )

    if tool == "ANOVA – Reactor Yield":
        anova_reactor_yield.run()

    elif tool == "Confidence Interval Estimator":
        confidence_interval_estimator.run()

    elif tool == "Control Chart (SPC)":
        control_chart_spc.run()

    elif tool == "Hypothesis Testing":
        hypothesis_testing_process.run()

    elif tool == "Monte Carlo Simulation":
        monte_carlo_process.run()

    elif tool == "Multicollinearity Detection":
        multicollinearity_detection.run()

    elif tool == "Regression – Heat Transfer":
        regression_heat_transfer.run()

    elif tool == "Residual Analysis":
        residual_analysis_tool.run()

    elif tool == "Response Surface Optimization":
        response_surface_optimization.run()

    elif tool == "Taguchi Optimization":
        taguchi_optimization.run()


if __name__ == "__main__":
    main()
