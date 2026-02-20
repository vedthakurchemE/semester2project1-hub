# ==========================================================
# FAULT TREE ANALYSIS (FTA) SIMULATOR
# Supports AND / OR gates + Monte Carlo Simulation
# ==========================================================

import numpy as np


# ----------------------------------------------------------
# Gate Calculations
# ----------------------------------------------------------

def and_gate(probabilities):
    """
    AND gate:
    All events must occur.
    P = product of probabilities
    """
    result = 1.0
    for p in probabilities:
        result *= p
    return result


def or_gate(probabilities):
    """
    OR gate:
    At least one event occurs.
    P = 1 - product(1 - p)
    """
    result = 1.0
    for p in probabilities:
        result *= (1 - p)
    return 1 - result


# ----------------------------------------------------------
# Monte Carlo Simulation
# ----------------------------------------------------------

def monte_carlo_simulation(probabilities, gate_type, iterations=100000):

    count = 0

    for _ in range(iterations):

        events = np.random.rand(len(probabilities)) < probabilities

        if gate_type == "AND":
            if all(events):
                count += 1

        elif gate_type == "OR":
            if any(events):
                count += 1

    return count / iterations


# ----------------------------------------------------------
# Main Run Function
# ----------------------------------------------------------

def run():

    print("\n=======================================")
    print("       FAULT TREE ANALYSIS TOOL")
    print("=======================================")

    print("\nChoose Gate Type for Top Event:")
    print("1 - AND Gate")
    print("2 - OR Gate")

    choice = input("Select option: ")

    if choice == "1":
        gate_type = "AND"
    elif choice == "2":
        gate_type = "OR"
    else:
        print("Invalid selection.")
        return

    try:
        n = int(input("Number of Basic Events: "))
    except ValueError:
        print("Invalid number.")
        return

    probabilities = []

    for i in range(n):
        try:
            p = float(input(f"Probability of Event {i+1} (0-1): "))
        except ValueError:
            print("Invalid input.")
            return

        if not (0 <= p <= 1):
            print("Probability must be between 0 and 1.")
            return

        probabilities.append(p)

    # ------------------------------------------------------
    # Analytical Calculation
    # ------------------------------------------------------

    if gate_type == "AND":
        top_event_prob = and_gate(probabilities)
    else:
        top_event_prob = or_gate(probabilities)

    print("\n------------ RESULTS ------------------")
    print(f"Gate Type           : {gate_type}")
    print(f"Top Event Probability (Analytical): {top_event_prob:.6f}")

    # ------------------------------------------------------
    # Monte Carlo Option
    # ------------------------------------------------------

    simulate = input("\nRun Monte Carlo Simulation? (y/n): ").lower()

    if simulate == "y":
        mc_prob = monte_carlo_simulation(probabilities, gate_type)
        print(f"Top Event Probability (Monte Carlo): {mc_prob:.6f}")

    print("---------------------------------------\n")
