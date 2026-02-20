# ==========================================================
# Linear Programming - Blending Problem
# Industrial Process Optimization Example
# ==========================================================

import numpy as np
from scipy.optimize import linprog


def run():
    print("Linear Programming - Blending Problem")
    print("--------------------------------------")

    # ------------------------------------------------------
    # Example: Fuel Blending Problem
    # ------------------------------------------------------
    #
    # We blend 3 raw materials to produce a final product.
    #
    # Goal: Minimize cost
    # Subject to:
    #   - Octane requirement
    #   - Sulfur limit
    #   - Total production = 100 units
    #
    # ------------------------------------------------------

    # Cost per unit of each component
    cost = np.array([40, 35, 50])  # $ per unit

    # ------------------------------------------------------
    # Constraints
    # ------------------------------------------------------

    # Component properties
    octane = np.array([90, 85, 95])
    sulfur = np.array([0.5, 0.8, 0.3])

    # Required specs
    min_octane = 88
    max_sulfur = 0.6
    total_production = 100

    # ------------------------------------------------------
    # Build Constraints
    # ------------------------------------------------------

    # Inequality constraints (A_ub x <= b_ub)

    A_ub = []

    # Octane constraint (convert >= to <= by multiplying -1)
    A_ub.append(-octane)
    b_ub = [-min_octane * total_production]

    # Sulfur constraint
    A_ub.append(sulfur)
    b_ub.append(max_sulfur * total_production)

    A_ub = np.array(A_ub)
    b_ub = np.array(b_ub)

    # Equality constraint (total blend must equal 100)
    A_eq = np.array([[1, 1, 1]])
    b_eq = np.array([total_production])

    # Bounds (non-negative)
    bounds = [(0, None), (0, None), (0, None)]

    # ------------------------------------------------------
    # Solve LP
    # ------------------------------------------------------

    result = linprog(
        c=cost,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method="highs"
    )

    # ------------------------------------------------------
    # Output Results
    # ------------------------------------------------------

    if result.success:
        print("\nOptimal Solution Found\n")
        for i, value in enumerate(result.x):
            print(f"Component {i+1}: {value:.2f} units")

        print(f"\nMinimum Cost: ${result.fun:.2f}")

        # Verify specs
        final_octane = np.dot(octane, result.x) / total_production
        final_sulfur = np.dot(sulfur, result.x) / total_production

        print(f"\nFinal Blend Properties:")
        print(f"Octane: {final_octane:.2f}")
        print(f"Sulfur: {final_sulfur:.3f}")

    else:
        print("Optimization failed.")
        print(result.message)
