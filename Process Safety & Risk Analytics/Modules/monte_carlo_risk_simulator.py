# ==========================================================
# MONTE CARLO RISK SIMULATOR
# Generic Engineering Risk Model
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------
# Sampling Functions
# ----------------------------------------------------------

def sample_distribution(dist_type, params, size):

    if dist_type == "normal":
        mean, std = params
        return np.random.normal(mean, std, size)

    elif dist_type == "uniform":
        low, high = params
        return np.random.uniform(low, high, size)

    elif dist_type == "lognormal":
        mean, sigma = params
        return np.random.lognormal(mean, sigma, size)

    else:
        raise ValueError("Unsupported distribution type")


# ----------------------------------------------------------
# Risk Model Function
# Example: Risk = Frequency × Consequence
# ----------------------------------------------------------

def risk_model(frequency, consequence):
    return frequency * consequence


# ----------------------------------------------------------
# Main Run Function
# ----------------------------------------------------------

def run():

    print("\n=========================================")
    print("        MONTE CARLO RISK SIMULATOR")
    print("=========================================")

    try:
        simulations = int(input("Number of simulations (e.g., 50000): "))
    except ValueError:
        print("Invalid number.")
        return

    print("\n--- Define Frequency Distribution ---")
    print("1 - Normal")
    print("2 - Uniform")
    print("3 - Lognormal")

    freq_choice = input("Select distribution: ")

    if freq_choice == "1":
        mean = float(input("Mean frequency: "))
        std = float(input("Std deviation: "))
        frequency = sample_distribution("normal", (mean, std), simulations)

    elif freq_choice == "2":
        low = float(input("Min frequency: "))
        high = float(input("Max frequency: "))
        frequency = sample_distribution("uniform", (low, high), simulations)

    elif freq_choice == "3":
        mean = float(input("Log-mean: "))
        sigma = float(input("Log-sigma: "))
        frequency = sample_distribution("lognormal", (mean, sigma), simulations)

    else:
        print("Invalid choice.")
        return

    print("\n--- Define Consequence Distribution ---")
    print("1 - Normal")
    print("2 - Uniform")
    print("3 - Lognormal")

    cons_choice = input("Select distribution: ")

    if cons_choice == "1":
        mean = float(input("Mean consequence: "))
        std = float(input("Std deviation: "))
        consequence = sample_distribution("normal", (mean, std), simulations)

    elif cons_choice == "2":
        low = float(input("Min consequence: "))
        high = float(input("Max consequence: "))
        consequence = sample_distribution("uniform", (low, high), simulations)

    elif cons_choice == "3":
        mean = float(input("Log-mean: "))
        sigma = float(input("Log-sigma: "))
        consequence = sample_distribution("lognormal", (mean, sigma), simulations)

    else:
        print("Invalid choice.")
        return

    # Ensure no negative values
    frequency = np.clip(frequency, 0, None)
    consequence = np.clip(consequence, 0, None)

    # ------------------------------------------------------
    # Risk Calculation
    # ------------------------------------------------------

    risk = risk_model(frequency, consequence)

    mean_risk = np.mean(risk)
    percentile_95 = np.percentile(risk, 95)
    percentile_99 = np.percentile(risk, 99)

    # Define failure threshold
    threshold = float(input("\nDefine failure threshold for risk: "))
    probability_failure = np.mean(risk > threshold)

    # ------------------------------------------------------
    # Output
    # ------------------------------------------------------

    print("\n-------------- RESULTS ----------------")
    print(f"Mean Risk                 : {mean_risk:.4f}")
    print(f"95th Percentile Risk      : {percentile_95:.4f}")
    print(f"99th Percentile Risk      : {percentile_99:.4f}")
    print(f"Probability of Exceedance : {probability_failure:.4f}")
    print("---------------------------------------")

    # ------------------------------------------------------
    # Plot Histogram
    # ------------------------------------------------------

    plt.figure(figsize=(8, 5))
    plt.hist(risk, bins=50, density=True)
    plt.axvline(threshold, linestyle="--")
    plt.title("Monte Carlo Risk Distribution")
    plt.xlabel("Risk")
    plt.ylabel("Probability Density")
    plt.show()

    print("\nSimulation complete.\n")
