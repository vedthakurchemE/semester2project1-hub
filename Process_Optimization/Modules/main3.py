import sys
import streamlit as st

from Process_Optimization.Modules import blending_lp
from Process_Optimization.Modules import constrained_optimization_pyomo
from Process_Optimization.Modules import dynamic_batch_reactor_optimization
from Process_Optimization.Modules import hen_energy_minimization
from Process_Optimization.Modules import multi_objective_yield_cost
from Process_Optimization.Modules import nonlinear_reactor_volume
from Process_Optimization.Modules import optimal_pipe_diameter
from Process_Optimization.Modules import production_scheduling_optimizer
from Process_Optimization.Modules import refinery_profit_optimization
from Process_Optimization.Modules import supply_chain_optimization

# ── Project registry ──────────────────────────────────────────
PROJECTS = {
    "1":  ("Linear Programming: Blending Problem",        blending_lp),
    "2":  ("Constrained Optimization (Pyomo)",            constrained_optimization_pyomo),
    "3":  ("Dynamic Optimization: Batch Reactor",         dynamic_batch_reactor_optimization),
    "4":  ("Energy Minimization (HEN)",                   hen_energy_minimization),
    "5":  ("Multi-objective (Yield vs Cost)",              multi_objective_yield_cost),
    "6":  ("Nonlinear Optimization (Reactor Volume)",      nonlinear_reactor_volume),
    "7":  ("Optimal Pipe Diameter",                        optimal_pipe_diameter),
    "8":  ("Production Scheduling Optimizer",              production_scheduling_optimizer),
    "9":  ("Refinery Profit Optimization",                 refinery_profit_optimization),
    "10": ("Supply Chain Optimization",                    supply_chain_optimization),
}


# ── Streamlit run() — called by master_main.py ───────────────
def run():
    """
    Entry point for master_main.py launcher.
    Renders a Streamlit UI to select and run any sub-module.
    Returns a dict of results for CSV/PDF export.
    """
    st.markdown("### 📐 Process Optimization")
    st.caption("Select a sub-module to run:")

    options = {f"{k}. {v[0]}": v[1] for k, v in PROJECTS.items()}
    selected_label = st.selectbox("Choose an optimization model:", list(options.keys()))
    selected_mod = options[selected_label]

    results = {}

    if st.button("▶ Run Selected Model", use_container_width=True):
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
    print("\n========================================")
    print("        PROCESS OPTIMIZATION MENU       ")
    print("========================================")
    for key, (name, _) in PROJECTS.items():
        print(f"  {key}  - {name}")
    print("  0  - Exit")


def main():
    while True:
        show_menu()
        choice = input("\nSelect an option: ").strip()

        if choice == "0":
            print("Exiting Program.")
            break
        elif choice in PROJECTS:
            print(f"\nRunning: {PROJECTS[choice][0]}")
            print("-" * 50)
            PROJECTS[choice][1].run()
        else:
            print("❌ Invalid selection. Try again.")


if __name__ == "__main__":
    main()