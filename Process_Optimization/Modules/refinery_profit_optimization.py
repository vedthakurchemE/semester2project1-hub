# ==========================================================
# Refinery Profit Optimization Model
# Linear Programming Formulation
# ==========================================================

import numpy as np
from scipy.optimize import linprog


def run():

    print("Refinery Profit Optimization Model")
    print("-----------------------------------")

    # ------------------------------------------------------
    # Decision Variables
    # ------------------------------------------------------
    #
    # x1 = crude A processed (barrels)
    # x2 = crude B processed (barrels)
    #
    # Objective: Maximize profit
    #
    # linprog minimizes → so we minimize (-profit)
    # ------------------------------------------------------

    # Crude processing cost ($/barrel)
    crude_cost = np.array([45, 50])

    # Product prices ($/barrel)
    gasoline_price = 90
    diesel_price = 80
    fuel_oil_price = 60

    # Yields from crude A
    yield_A = {
        "gasoline": 0.5,
        "diesel": 0.3,
        "fuel_oil": 0.2
    }

    # Yields from crude B
    yield_B = {
        "gasoline": 0.4,
        "diesel": 0.4,
        "fuel_oil": 0.2
    }

    # ------------------------------------------------------
    # Profit per barrel processed
    # ------------------------------------------------------

    profit_A = (
        yield_A["gasoline"] * gasoline_price +
        yield_A["diesel"] * diesel_price +
        yield_A["fuel_oil"] * fuel_oil_price
        - crude_cost[0]
    )

    profit_B = (
        yield_B["gasoline"] * gasoline_price +
        yield_B["diesel"] * diesel_price +
        yield_B["fuel_oil"] * fuel_oil_price
        - crude_cost[1]
    )

    # Since linprog minimizes → use negative profit
    c = -np.array([profit_A, profit_B])

    # ------------------------------------------------------
    # Constraints
    # ------------------------------------------------------

    # Refinery capacity
    max_capacity = 100000  # barrels/day

    # Demand limits
    max_gasoline = 50000
    max_diesel = 40000
    max_fuel_oil = 30000

    A_ub = []
    b_ub = []

    # Capacity constraint
    A_ub.append([1, 1])
    b_ub.append(max_capacity)

    # Gasoline demand constraint
    A_ub.append([
        yield_A["gasoline"],
        yield_B["gasoline"]
    ])
    b_ub.append(max_gasoline)

    # Diesel demand constraint
    A_ub.append([
        yield_A["diesel"],
        yield_B["diesel"]
    ])
    b_ub.append(max_diesel)

    # Fuel oil demand constraint
    A_ub.append([
        yield_A["fuel_oil"],
        yield_B["fuel_oil"]
    ])
    b_ub.append(max_fuel_oil)

    A_ub = np.array(A_ub)
    b_ub = np.array(b_ub)

    # Non-negative bounds
    bounds = [(0, None), (0, None)]

    # ------------------------------------------------------
    # Solve LP
    # ------------------------------------------------------

    result = linprog(
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        bounds=bounds,
        method="highs"
    )

    # ------------------------------------------------------
    # Results
    # ------------------------------------------------------

    if result.success:

        xA, xB = result.x
        max_profit = -result.fun

        print("\nOptimal Crude Processing Plan\n")
        print(f"Crude A: {xA:.2f} barrels/day")
        print(f"Crude B: {xB:.2f} barrels/day")

        print(f"\nMaximum Daily Profit: ${max_profit:,.2f}")

        # Calculate product outputs
        gasoline = yield_A["gasoline"] * xA + yield_B["gasoline"] * xB
        diesel = yield_A["diesel"] * xA + yield_B["diesel"] * xB
        fuel_oil = yield_A["fuel_oil"] * xA + yield_B["fuel_oil"] * xB

        print("\nProduct Outputs:")
        print(f"Gasoline: {gasoline:.2f} barrels")
        print(f"Diesel: {diesel:.2f} barrels")
        print(f"Fuel Oil: {fuel_oil:.2f} barrels")

    else:
        print("Optimization failed.")
        print(result.message)
