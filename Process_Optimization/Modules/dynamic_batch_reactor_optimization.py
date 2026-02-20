# ==========================================================
# Dynamic Optimization of Batch Reactor
# Piecewise Temperature Optimization
# ==========================================================

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize


def run():

    print("Dynamic Optimization of Batch Reactor")
    print("--------------------------------------")

    # ------------------------------------------------------
    # Constants
    # ------------------------------------------------------

    R = 8.314
    k0 = 1e6
    E = 80000

    CA0 = 2.0
    CB0 = 0.0

    tf = 10          # total batch time
    N = 5            # number of control intervals

    T_min = 300
    T_max = 900

    dt = tf / N

    # ------------------------------------------------------
    # Kinetics
    # ------------------------------------------------------

    def k(T):
        return k0 * np.exp(-E / (R * T))

    # ------------------------------------------------------
    # ODE system
    # ------------------------------------------------------

    def reactor_odes(t, y, T_profile):

        CA, CB = y

        # Determine which interval we are in
        index = min(int(t / dt), N - 1)
        T = T_profile[index]

        rate = k(T) * CA

        dCA_dt = -rate
        dCB_dt = rate

        return [dCA_dt, dCB_dt]

    # ------------------------------------------------------
    # Objective Function
    # ------------------------------------------------------

    def objective(T_profile):

        sol = solve_ivp(
            reactor_odes,
            [0, tf],
            [CA0, CB0],
            args=(T_profile,),
            t_eval=[tf]
        )

        CAf, CBf = sol.y[:, -1]

        # We maximize CB → minimize negative CB
        return -CBf

    # ------------------------------------------------------
    # Initial Guess
    # ------------------------------------------------------

    T0 = np.full(N, 500)

    bounds = [(T_min, T_max)] * N

    # ------------------------------------------------------
    # Optimization
    # ------------------------------------------------------

    result = minimize(
        objective,
        T0,
        bounds=bounds,
        method="L-BFGS-B"
    )

    # ------------------------------------------------------
    # Results
    # ------------------------------------------------------

    if result.success:

        T_opt = result.x

        sol = solve_ivp(
            reactor_odes,
            [0, tf],
            [CA0, CB0],
            args=(T_opt,),
            t_eval=np.linspace(0, tf, 100)
        )

        CA = sol.y[0]
        CB = sol.y[1]

        print("\nOptimal Temperature Profile (K):")
        for i, T in enumerate(T_opt):
            print(f"Interval {i+1}: {T:.2f}")

        print(f"\nFinal Product Concentration: {CB[-1]:.4f}")

    else:
        print("Optimization failed.")
        print(result.message)
