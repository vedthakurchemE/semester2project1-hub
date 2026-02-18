# main.py

from Modules import (
    bow_tie_risk_tool,
    explosion_risk_prediction,
    failure_probability_estimator,
    fault_tree_analysis_simulator,
    gas_leak_dispersion_simulation,
    hazop_risk_ranking,
    monte_carlo_risk_simulator,
    reliability_block_diagram,
    safety_kpi_dashboard,
    sil_classification_tool
)

def main():
    print("=== Industrial Risk Analysis Suite ===")
    print("Select a module to run:")
    print("1. Bow-Tie Risk Tool")
    print("2. Explosion Risk Prediction")
    print("3. Failure Probability Estimator")
    print("4. Fault Tree Analysis Simulator")
    print("5. Gas Leak Dispersion Simulation")
    print("6. HAZOP Risk Ranking")
    print("7. Monte Carlo Risk Simulator")
    print("8. Reliability Block Diagram")
    print("9. Safety KPI Dashboard")
    print("10. SIL Classification Tool")
    print("0. Exit")

    while True:
        choice = input("Enter your choice (0-10): ")
        if choice == '1':
            bow_tie_risk_tool.run()
        elif choice == '2':
            explosion_risk_prediction.run()
        elif choice == '3':
            failure_probability_estimator.run()
        elif choice == '4':
            fault_tree_analysis_simulator.run()
        elif choice == '5':
            gas_leak_dispersion_simulation.run()
        elif choice == '6':
            hazop_risk_ranking.run()
        elif choice == '7':
            monte_carlo_risk_simulator.run()
        elif choice == '8':
            reliability_block_diagram.run()
        elif choice == '9':
            safety_kpi_dashboard.run()
        elif choice == '10':
            sil_classification_tool.run()
        elif choice == '0':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
