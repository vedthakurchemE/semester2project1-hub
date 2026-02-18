# ==========================================================
# Multi-objective Optimization (Yield vs Cost)
# Weighted Sum Approach
# ==========================================================

import numpy as np
from scipy.optimize import minimize


def run():

    print("Multi-objective Optimization: Yield vs Cost")
    print("-------------------------------------------")

    # ------------------------------------------------------
    # Constants
    # ------------------------------------------------------

    R = 8.314
    k0 = 1e6
    E = 80000

    tau = 5
    FA0 = 10
    CA0 = 2

    a = 0.05      # energy cost coefficient
    b = 2.0       # reactor volume cost factor

    # Weights (change to explore Pareto behavior)
    w_yield = 0.7
    w_cost = 0.3

    # ------------------------------------------------------
    # Models
    # ------------------------------------------------------

    def rate_constant(T):
        return k0 * np.exp(-E / (R * T))

    def yield_model(T):
        k = rate_constant(T)
        return 1 - np.exp(-k * tau)

    def reactor_volume(T):
        k = rate_constant(T)
        X = yield_model(T)

        if X >= 1:
            X = 0.999

        return (FA0 * X) / (k * CA0 * (1 - X))

    def cost_model(T):
        energy_cost = a * T
        volume_cost = b * reactor_volume(T)
        return energy_cost + volume_cost

    # ------------------------------------------------------
    # Weighted Objective
    # ------------------------------------------------------

    def objective(T):

        T = T[0]

        Y = yield_model(T)
        C = cost_model(T)

        # normalize (optional but recommended)
        Y_norm = Y
        C_norm = C / 100

        return w_yield * (-Y_norm) + w_cost * C_norm

    # ------------------------------------------------------
    # Optimization
    # ------------------------------------------------------

    bounds = [(300, 900)]
    x0 = np.array([500])

    result = minimize(
        objective,
        x0,
        bounds=bounds,
        method="L-BFGS-B"
    )

    # ------------------------------------------------------
    # Results
    # ------------------------------------------------------

    if result.success:

        T_opt = result.x[0]
        Y_opt = yield_model(T_opt)
        C_opt = cost_model(T_opt)

        print(f"\nOptimal Temperature: {T_opt:.2f} K")
        print(f"Yield: {Y_opt:.4f}")
        print(f"Cost: {C_opt:.4f}")

    else:
        print("Optimization failed.")
        print(result.message)
