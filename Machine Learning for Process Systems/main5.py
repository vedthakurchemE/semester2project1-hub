# ==========================================================
# Machine Learning for Process Systems - Project Launcher
# ==========================================================

import sys

# Import run functions from each module
from Modules.catalyst_deactivation_prediction import run as run_catalyst
from Modules.energy_consumption_prediction import run as run_energy
from Modules.fault_classification_model import run as run_fault
from Modules.plant_anomaly_detection import run as run_anomaly
from Modules.predictive_maintenance_model import run as run_predictive
from Modules.quality_prediction_xgboost import run as run_quality
from Modules.reactor_temperature_forecast import run as run_reactor
from Modules.rul_estimator import run as run_rul
from Modules.soft_sensor_concentration import run as run_soft_sensor
from Modules.yield_optimization_ml import run as run_yield


PROJECTS = {
    "1": ("Catalyst Deactivation Prediction", run_catalyst),
    "2": ("Energy Consumption Prediction", run_energy),
    "3": ("Fault Classification Model", run_fault),
    "4": ("Plant Anomaly Detection", run_anomaly),
    "5": ("Predictive Maintenance Model", run_predictive),
    "6": ("Quality Prediction using XGBoost", run_quality),
    "7": ("Reactor Temperature Forecast", run_reactor),
    "8": ("Remaining Useful Life (RUL) Estimator", run_rul),
    "9": ("Soft Sensor Concentration Model", run_soft_sensor),
    "10": ("Yield Optimization using ML", run_yield),
}


def show_menu():
    print("\n===============================================")
    print(" MACHINE LEARNING FOR PROCESS SYSTEMS PLATFORM ")
    print("===============================================")

    for key, (name, _) in PROJECTS.items():
        print(f"{key}. {name}")

    print("0. Exit")


def main():

    while True:
        show_menu()
        choice = input("\nSelect a project number: ")

        if choice == "0":
            print("\nExiting system.")
            sys.exit()

        elif choice in PROJECTS:
            print(f"\nRunning: {PROJECTS[choice][0]}")
            print("-" * 50)
            PROJECTS[choice][1]()  # Call module run()

        else:
            print("\nInvalid selection. Try again.")


if __name__ == "__main__":
    main()
