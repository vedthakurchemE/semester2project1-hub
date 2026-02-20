# ==========================================================
# Main File - Statistical Inference & Design of Experiments
# main2.py
# ==========================================================

import streamlit as st

from Statistical_Inference_DOE.modules import anova_reactor_yield
from Statistical_Inference_DOE.modules import confidence_interval_estimator
from Statistical_Inference_DOE.modules import control_chart_spc
from Statistical_Inference_DOE.modules import hypothesis_testing_process
from Statistical_Inference_DOE.modules import monte_carlo_process
from Statistical_Inference_DOE.modules import multicollinearity_detection
from Statistical_Inference_DOE.modules import regression_heat_transfer
from Statistical_Inference_DOE.modules import residual_analysis_tool
from Statistical_Inference_DOE.modules import response_surface_optimization
from Statistical_Inference_DOE.modules import taguchi_optimization

# ── Tool registry ─────────────────────────────────────────────
TOOLS = {
    "ANOVA – Reactor Yield":           anova_reactor_yield,
    "Confidence Interval Estimator":   confidence_interval_estimator,
    "Control Chart (SPC)":             control_chart_spc,
    "Hypothesis Testing":              hypothesis_testing_process,
    "Monte Carlo Simulation":          monte_carlo_process,
    "Multicollinearity Detection":     multicollinearity_detection,
    "Regression – Heat Transfer":      regression_heat_transfer,
    "Residual Analysis":               residual_analysis_tool,
    "Response Surface Optimization":   response_surface_optimization,
    "Taguchi Optimization":            taguchi_optimization,
}


# ── Streamlit run() — called by master_main.py ───────────────
def run():
    """
    Entry point for master_main.py launcher.
    Renders a Streamlit UI to select and run any sub-module.
    Returns a dict of results for CSV/PDF export.
    """
    st.markdown("### 📊 Statistical Inference & Design of Experiments")
    st.caption("Select a sub-module to run:")

    selected_label = st.selectbox(
        "Choose an analysis tool:",
        list(TOOLS.keys())
    )
    selected_mod = TOOLS[selected_label]

    results = {}

    if st.button("▶ Run Selected Tool", use_container_width=True):
        with st.spinner(f"Running {selected_label}..."):
            try:
                output = selected_mod.run()
                if isinstance(output, dict):
                    results = output
                elif isinstance(output, tuple) and len(output) == 2:
                    _, results = output
                elif isinstance(output, tuple) and len(output) == 3:
                    _, results, _ = output
                else:
                    results = {"Status": "Completed", "Module": selected_label}
            except Exception as e:
                st.error(f"❌ Error running module: {e}")
                results = {"Error": str(e)}

    return results


# ── Standalone Streamlit entry point (direct run) ─────────────
def main():
    # NOTE: st.set_page_config is intentionally excluded here
    # because master_main.py already calls it.
    # Only include it if running this file directly:
    # st.set_page_config(page_title="Statistical Inference & DOE Suite", layout="wide")

    st.sidebar.title("📊 Statistical Tools")
    selected_label = st.sidebar.selectbox("Select Analysis Module", list(TOOLS.keys()))
    TOOLS[selected_label].run()


if __name__ == "__main__":
    # When run directly (not via master_main), re-enable page config
    import streamlit as st
    st.set_page_config(
        page_title="Statistical Inference & DOE Suite",
        layout="wide"
    )
    main()