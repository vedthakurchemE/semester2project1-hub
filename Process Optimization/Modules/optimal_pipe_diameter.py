# ==========================================================
# Optimal Pipe Diameter Calculator
# Economic + Hydraulic Optimization
# ==========================================================

import numpy as np
from scipy.optimize import minimize


def run():

    print("Optimal Pipe Diameter Optimization")
    print("-----------------------------------")

    # ------------------------------------------------------
    # Given Data
    # ------------------------------------------------------

    Q = 0.05              # m^3/s
    rho = 1000            # kg/m^3
    mu = 0.001            # Pa.s
    L = 500               # m
    eta = 0.75            # pump efficiency

    electricity_cost = 0.1      # $/kWh
    operating_hours = 8000      # hours/year

    pipe_cost_coeff = 300       # cost coefficient
    friction_factor = 0.02      # assumed turbulent constant f

    # ------------------------------------------------------
    # Objective Function
    # ------------------------------------------------------

    def total_cost(D):

        D = D[0]

        if D <= 0:
            return 1e9

        # Velocity
        v = (4 * Q) / (np.pi * D**2)

        # Pressure drop
        deltaP = friction_factor * (L / D) * (rho * v**2 / 2)

        # Pumping power (W)
        power = (deltaP * Q) / eta

        # Convert to kW
        power_kW = power / 1000

        # Annual energy cost
        energy_cost = power_kW * operating_hours * electricity_cost

        # Pipe capital cost (simple scaling law)
        capital_cost = pipe_cost_coeff * (D**1.2) * L

        return energy_cost + capital_cost

    # ------------------------------------------------------
    # Optimization
    # ------------------------------------------------------

    bounds = [(0.05, 1.0)]   # diameter range in meters
    x0 = np.array([0.2])

    result = minimize(
        total_cost,
        x0,
        bounds=bounds,
        method="L-BFGS-B"
    )

    # ------------------------------------------------------
    # Results
    # ------------------------------------------------------

    if result.success:

        D_opt = result.x[0]
        cost_opt = total_cost([D_opt])

        print(f"\nOptimal Diameter: {D_opt:.4f} m")
        print(f"Minimum Annual Cost: ${cost_opt:,.2f}")

    else:
        print("Optimization failed.")
        print(result.message)
