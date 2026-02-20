import sys
import streamlit as st

# Import run functions from each module
from Machine_Learning_for_Process_Systems.Modules.catalyst_deactivation_prediction import run as run_catalyst
from Machine_Learning_for_Process_Systems.Modules.energy_consumption_prediction import run as run_energy
from Machine_Learning_for_Process_Systems.Modules.fault_classification_model import run as run_fault
from Machine_Learning_for_Process_Systems.Modules.plant_anomaly_detection import run as run_anomaly
from Machine_Learning_for_Process_Systems.Modules.predictive_maintenance_model import run as run_predictive
from Machine_Learning_for_Process_Systems.Modules.quality_prediction_xgboost import run as run_quality
from Machine_Learning_for_Process_Systems.Modules.reactor_temperature_forecast import run as run_reactor
from Machine_Learning_for_Process_Systems.Modules.rul_estimator import run as run_rul
from Machine_Learning_for_Process_Systems.Modules.soft_sensor_concentration import run as run_soft_sensor
from Machine_Learning_for_Process_Systems.Modules.yield_optimization_ml import run as run_yield

# ── Project registry ──────────────────────────────────────────
PROJECTS = {
    "1":  ("Catalyst Deactivation Prediction",    run_catalyst),
    "2":  ("Energy Consumption Prediction",        run_energy),
    "3":  ("Fault Classification Model",           run_fault),
    "4":  ("Plant Anomaly Detection",              run_anomaly),
    "5":  ("Predictive Maintenance Model",         run_predictive),
    "6":  ("Quality Prediction using XGBoost",     run_quality),
    "7":  ("Reactor Temperature Forecast",         run_reactor),
    "8":  ("Remaining Useful Life (RUL) Estimator", run_rul),
    "9":  ("Soft Sensor Concentration Model",      run_soft_sensor),
    "10": ("Yield Optimization using ML",          run_yield),
}


# ── Streamlit run() — called by master_main.py ───────────────
def run():
    """
    Entry point for the master_main.py launcher.
    Renders a Streamlit UI to select and run any sub-module.
    Returns a dict of results for CSV/PDF export.
    """
    st.markdown("### 🤖 Machine Learning for Process Systems")
    st.caption("Select a sub-module to run:")

    options = {f"{k}. {v[0]}": v[1] for k, v in PROJECTS.items()}
    selected_label = st.selectbox("Choose a model:", list(options.keys()))
    selected_fn = options[selected_label]

    results = {}

    if st.button("▶ Run Selected Model", use_container_width=True):
        with st.spinner(f"Running {selected_label}..."):
            try:
                output = selected_fn()
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
    print("\n===============================================")
    print(" MACHINE LEARNING FOR PROCESS SYSTEMS PLATFORM")
    print("===============================================")
    for key, (name, _) in PROJECTS.items():
        print(f"  {key}. {name}")
    print("  0. Exit")


def main():
    while True:
        show_menu()
        choice = input("\nSelect a project number: ").strip()

        if choice == "0":
            print("\nExiting system.")
            sys.exit()
        elif choice in PROJECTS:
            print(f"\nRunning: {PROJECTS[choice][0]}")
            print("-" * 50)
            PROJECTS[choice][1]()
        else:
            print("\n❌ Invalid selection. Try again.")


if __name__ == "__main__":
    main()
