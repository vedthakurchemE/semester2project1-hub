# ==========================================================
# Nonlinear Optimization - Reactor Volume Minimization
# CSTR with First Order Reaction
# ==========================================================

import numpy as np
from scipy.optimize import minimize


def run():

    print("Nonlinear Optimization for Reactor Volume")
    print("------------------------------------------")

    # ------------------------------------------------------
    # Process Parameters
    # ------------------------------------------------------

    FA0 = 10        # mol/s
    CA0 = 2         # mol/L
    k = 0.5         # 1/s

    X_min = 0.70    # Minimum required conversion

    # ------------------------------------------------------
    # Volume function (Nonlinear)
    # ------------------------------------------------------

    def reactor_volume(X):

        # Prevent division by zero
        if X <= 0 or X >= 1:
            return 1e6

        V = (FA0 * X) / (k * CA0 * (1 - X))
        return V

    # Initial guess
    x0 = np.array([0.75])

    # Bounds for conversion
    bounds = [(X_min, 0.99)]

    # Solve nonlinear optimization
    result = minimize(
        reactor_volume,
        x0,
        bounds=bounds,
        method="L-BFGS-B"
    )

    # ------------------------------------------------------
    # Results
    # ------------------------------------------------------

    if result.success:

        optimal_X = result.x[0]
        optimal_V = reactor_volume(optimal_X)

        print(f"\nOptimal Conversion: {optimal_X:.4f}")
        print(f"Minimum Reactor Volume: {optimal_V:.4f} L")

    else:
        print("Optimization failed.")
        print(result.message)
