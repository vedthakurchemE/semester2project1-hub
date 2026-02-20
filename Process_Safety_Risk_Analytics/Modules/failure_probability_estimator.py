# ==========================================================
# FAILURE PROBABILITY ESTIMATOR
# Reliability Engineering Tool (Exponential & Weibull)
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------
# Reliability Models
# ----------------------------------------------------------

def exponential_reliability(lmbda, t):
    return np.exp(-lmbda * t)


def weibull_reliability(beta, eta, t):
    return np.exp(-(t / eta) ** beta)


def exponential_mttf(lmbda):
    return 1 / lmbda


def weibull_mttf(beta, eta):
    return eta * np.gamma(1 + 1 / beta)


# ----------------------------------------------------------
# Hazard Functions
# ----------------------------------------------------------

def exponential_hazard(lmbda):
    return lmbda


def weibull_hazard(beta, eta, t):
    return (beta / eta) * (t / eta) ** (beta - 1)


# ----------------------------------------------------------
# Monte Carlo Simulation
# ----------------------------------------------------------

def monte_carlo_weibull(beta, eta, simulations=50000):
    samples = np.random.weibull(beta, simulations) * eta
    return samples


# ----------------------------------------------------------
# Main Function
# ----------------------------------------------------------

def run():

    print("\n=========================================")
    print("       FAILURE PROBABILITY ESTIMATOR")
    print("=========================================")

    print("\nChoose Reliability Model:")
    print("1 - Exponential (Constant Failure Rate)")
    print("2 - Weibull (Generalized Life Model)")

    choice = input("Select option: ")

    try:
        time_horizon = float(input("Evaluate up to time (hours): "))
    except ValueError:
        print("Invalid time.")
        return

    t = np.linspace(0, time_horizon, 300)

    # ------------------------------------------------------
    # Exponential Model
    # ------------------------------------------------------

    if choice == "1":

        try:
            lmbda = float(input("Failure Rate λ (failures/hour): "))
        except ValueError:
            print("Invalid input.")
            return

        R = exponential_reliability(lmbda, t)
        F = 1 - R
        hazard = exponential_hazard(lmbda)
        mttf = exponential_mttf(lmbda)

        print("\n------------- RESULTS ----------------")
        print(f"MTTF                     : {mttf:.2f} hours")
        print(f"Hazard Rate              : {hazard:.6f}")
        print(f"Failure Probability at t : {F[-1]:.4f}")
        print("--------------------------------------")

    # ------------------------------------------------------
    # Weibull Model
    # ------------------------------------------------------

    elif choice == "2":

        try:
            beta = float(input("Shape Parameter β: "))
            eta = float(input("Scale Parameter η (hours): "))
        except ValueError:
            print("Invalid input.")
            return

        R = weibull_reliability(beta, eta, t)
        F = 1 - R
        hazard = weibull_hazard(beta, eta, t)
        mttf = weibull_mttf(beta, eta)

        print("\n------------- RESULTS ----------------")
        print(f"MTTF                     : {mttf:.2f} hours")
        print(f"Failure Probability at t : {F[-1]:.4f}")
        print("--------------------------------------")

        # Monte Carlo
        simulate = input("\nRun Monte Carlo life simulation? (y/n): ").lower()

        if simulate == "y":
            samples = monte_carlo_weibull(beta, eta)

            plt.figure()
            plt.hist(samples, bins=50, density=True)
            plt.title("Simulated Failure Time Distribution")
            plt.xlabel("Time to Failure (hours)")
            plt.ylabel("Probability Density")
            plt.show()

    else:
        print("Invalid choice.")
        return

    # ------------------------------------------------------
    # Plot Reliability & Failure Curves
    # ------------------------------------------------------

    plt.figure()
    plt.plot(t, R)
    plt.plot(t, F)
    plt.title("Reliability & Failure Probability")
    plt.xlabel("Time (hours)")
    plt.ylabel("Probability")
    plt.legend(["Reliability R(t)", "Failure Probability F(t)"])
    plt.grid(True)
    plt.show()

    print("\nEstimation complete.\n")
