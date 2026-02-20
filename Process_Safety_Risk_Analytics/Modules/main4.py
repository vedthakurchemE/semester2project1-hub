
import sys
import streamlit as st

from Process_Safety_Risk_Analytics.Modules import bow_tie_risk_tool
from Process_Safety_Risk_Analytics.Modules import explosion_risk_prediction
from Process_Safety_Risk_Analytics.Modules import failure_probability_estimator
from Process_Safety_Risk_Analytics.Modules import fault_tree_analysis_simulator
from Process_Safety_Risk_Analytics.Modules import gas_leak_dispersion_simulation
from Process_Safety_Risk_Analytics.Modules import hazop_risk_ranking
from Process_Safety_Risk_Analytics.Modules import monte_carlo_risk_simulator
from Process_Safety_Risk_Analytics.Modules import reliability_block_diagram
from Process_Safety_Risk_Analytics.Modules import safety_kpi_dashboard
from Process_Safety_Risk_Analytics.Modules import sil_classification_tool

# ── Project registry ──────────────────────────────────────────
PROJECTS = {
    "1":  ("Bow-Tie Risk Tool",               bow_tie_risk_tool),
    "2":  ("Explosion Risk Prediction",        explosion_risk_prediction),
    "3":  ("Failure Probability Estimator",    failure_probability_estimator),
    "4":  ("Fault Tree Analysis Simulator",    fault_tree_analysis_simulator),
    "5":  ("Gas Leak Dispersion Simulation",   gas_leak_dispersion_simulation),
    "6":  ("HAZOP Risk Ranking",               hazop_risk_ranking),
    "7":  ("Monte Carlo Risk Simulator",       monte_carlo_risk_simulator),
    "8":  ("Reliability Block Diagram",        reliability_block_diagram),
    "9":  ("Safety KPI Dashboard",             safety_kpi_dashboard),
    "10": ("SIL Classification Tool",          sil_classification_tool),
}


# ── Streamlit run() — called by master_main.py ───────────────
def run():
    """
    Entry point for master_main.py launcher.
    Renders a Streamlit UI to select and run any sub-module.
    Returns a dict of results for CSV/PDF export.
    """
    st.markdown("### 🛡️ Process Safety & Risk Analytics")
    st.caption("Select a sub-module to run:")

    options = {f"{k}. {v[0]}": v[1] for k, v in PROJECTS.items()}
    selected_label = st.selectbox("Choose a risk analysis tool:", list(options.keys()))
    selected_mod = options[selected_label]

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


# ── CLI entry point (local terminal use) ─────────────────────
def show_menu():
    print("\n=== Industrial Risk Analysis Suite ===")
    print("Select a module to run:")
    for key, (name, _) in PROJECTS.items():
        print(f"  {key}. {name}")
    print("  0. Exit")


def main():
    while True:
        show_menu()
        choice = input("\nEnter your choice (0-10): ").strip()

        if choice == "0":
            print("Exiting program...")
            break
        elif choice in PROJECTS:
            print(f"\nRunning: {PROJECTS[choice][0]}")
            print("-" * 50)
            PROJECTS[choice][1].run()
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()