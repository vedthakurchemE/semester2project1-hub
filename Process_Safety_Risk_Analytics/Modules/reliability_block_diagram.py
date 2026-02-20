# ==========================================================
# RELIABILITY BLOCK DIAGRAM (RBD) SIMULATOR
# Series / Parallel / Mixed Systems
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------
# Component Reliability Models
# ----------------------------------------------------------

def exponential_reliability(lmbda, t):
    return np.exp(-lmbda * t)


def weibull_reliability(beta, eta, t):
    return np.exp(-(t / eta) ** beta)


# ----------------------------------------------------------
# System Configurations
# ----------------------------------------------------------

def series_system(reliabilities):
    """
    Series system reliability:
    R_sys = Π R_i
    """
    return np.prod(reliabilities, axis=0)


def parallel_system(reliabilities):
    """
    Parallel system reliability:
    R_sys = 1 - Π (1 - R_i)
    """
    return 1 - np.prod([1 - r for r in reliabilities], axis=0)


# ----------------------------------------------------------
# Monte Carlo Simulation
# ----------------------------------------------------------

def monte_carlo_series(lambdas, simulations=50000):
    lifetimes = []
    for lmbda in lambdas:
        lifetimes.append(np.random.exponential(1/lmbda, simulations))
    lifetimes = np.array(lifetimes)
    return np.min(lifetimes, axis=0)


def monte_carlo_parallel(lambdas, simulations=50000):
    lifetimes = []
    for lmbda in lambdas:
        lifetimes.append(np.random.exponential(1/lmbda, simulations))
    lifetimes = np.array(lifetimes)
    return np.max(lifetimes, axis=0)


# ----------------------------------------------------------
# Main Interface
# ----------------------------------------------------------

def run():

    print("\n=========================================")
    print("     RELIABILITY BLOCK DIAGRAM TOOL")
    print("=========================================")

    print("\nChoose Configuration:")
    print("1 - Series")
    print("2 - Parallel")

    choice = input("Select option: ")

    n = int(input("Number of components: "))

    model_type = input("Use Exponential model? (y/n for Weibull): ").lower()

    time_horizon = float(input("Evaluate up to time (hours): "))
    t = np.linspace(0, time_horizon, 400)

    reliabilities = []

    # ------------------------------------------------------
    # Component Definition
    # ------------------------------------------------------

    for i in range(n):

        print(f"\nComponent {i+1}")

        if model_type == "y":
            lmbda = float(input("Failure rate λ (failures/hour): "))
            R = exponential_reliability(lmbda, t)
        else:
            beta = float(input("Shape β: "))
            eta = float(input("Scale η (hours): "))
            R = weibull_reliability(beta, eta, t)

        reliabilities.append(R)

    # ------------------------------------------------------
    # System Calculation
    # ------------------------------------------------------

    if choice == "1":
        R_sys = series_system(reliabilities)
        print("\nConfiguration: SERIES")

    elif choice == "2":
        R_sys = parallel_system(reliabilities)
        print("\nConfiguration: PARALLEL")

    else:
        print("Invalid selection.")
        return

    F_sys = 1 - R_sys

    print("\nSystem Reliability at final time:", R_sys[-1])
    print("System Failure Probability:", F_sys[-1])

    # ------------------------------------------------------
    # Plot Results
    # ------------------------------------------------------

    plt.figure()
    plt.plot(t, R_sys)
    plt.title("System Reliability Curve")
    plt.xlabel("Time (hours)")
    plt.ylabel("Reliability R(t)")
    plt.grid(True)
    plt.show()

    # ------------------------------------------------------
    # Optional Monte Carlo
    # ------------------------------------------------------

    simulate = input("\nRun Monte Carlo simulation (Exponential only)? (y/n): ").lower()

    if simulate == "y" and model_type == "y":

        lambdas = []

        for i in range(n):
            lmbda = float(input(f"Enter λ for Component {i+1}: "))
            lambdas.append(lmbda)

        if choice == "1":
            samples = monte_carlo_series(lambdas)
        else:
            samples = monte_carlo_parallel(lambdas)

        print("Estimated MTTF (Monte Carlo):", np.mean(samples))

        plt.figure()
        plt.hist(samples, bins=50, density=True)
        plt.title("Simulated System Lifetime Distribution")
        plt.xlabel("Time to Failure (hours)")
        plt.ylabel("Density")
        plt.show()

    print("\nSimulation Complete.\n")
