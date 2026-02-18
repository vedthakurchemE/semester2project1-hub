# ==========================================================
# Energy Minimization in Heat Exchanger Network (HEN)
# Linear Programming Formulation
# ==========================================================

import numpy as np
from scipy.optimize import linprog


def run():

    print("Heat Exchanger Network Energy Minimization")
    print("------------------------------------------")

    # ------------------------------------------------------
    # Example System
    # ------------------------------------------------------
    #
    # 2 Hot Streams
    # 2 Cold Streams
    #
    # Goal: Minimize external utilities
    #
    # Decision variables:
    # Q11 = heat from H1 to C1
    # Q12 = heat from H1 to C2
    # Q21 = heat from H2 to C1
    # Q22 = heat from H2 to C2
    #
    # QH = Hot utility
    # QC = Cold utility
    #
    # ------------------------------------------------------

    # Heat duties required (kW)
    hot_stream_supply = np.array([100, 80])     # H1, H2
    cold_stream_demand = np.array([90, 70])     # C1, C2

    # Objective: minimize utilities only
    # Internal heat exchange has zero cost
    # Penalize QH and QC

    cost = np.array([
        0, 0, 0, 0,   # Q11 Q12 Q21 Q22
        1,            # QH (hot utility cost weight)
        1             # QC (cold utility cost weight)
    ])

    # ------------------------------------------------------
    # Constraints
    # ------------------------------------------------------

    A_eq = []
    b_eq = []

    # Hot stream balances
    # H1: Q11 + Q12 + QC1 = supply
    A_eq.append([1, 1, 0, 0, 0, 1])
    b_eq.append(hot_stream_supply[0])

    # H2
    A_eq.append([0, 0, 1, 1, 0, 1])
    b_eq.append(hot_stream_supply[1])

    # Cold stream balances
    # C1: Q11 + Q21 + QH1 = demand
    A_eq.append([1, 0, 1, 0, 1, 0])
    b_eq.append(cold_stream_demand[0])

    # C2
    A_eq.append([0, 1, 0, 1, 1, 0])
    b_eq.append(cold_stream_demand[1])

    A_eq = np.array(A_eq)
    b_eq = np.array(b_eq)

    # Bounds: all heat flows >= 0
    bounds = [(0, None)] * 6

    # ------------------------------------------------------
    # Solve LP
    # ------------------------------------------------------

    result = linprog(
        c=cost,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method="highs"
    )

    # ------------------------------------------------------
    # Results
    # ------------------------------------------------------

    if result.success:

        Q11, Q12, Q21, Q22, QH, QC = result.x

        print("\nOptimal Heat Exchange Distribution\n")

        print(f"Q(H1 → C1): {Q11:.2f} kW")
        print(f"Q(H1 → C2): {Q12:.2f} kW")
        print(f"Q(H2 → C1): {Q21:.2f} kW")
        print(f"Q(H2 → C2): {Q22:.2f} kW")

        print("\nUtility Requirements:")
        print(f"Hot Utility Required: {QH:.2f} kW")
        print(f"Cold Utility Required: {QC:.2f} kW")

        print(f"\nTotal External Energy: {QH + QC:.2f} kW")

    else:
        print("Optimization failed.")
        print(result.message)
