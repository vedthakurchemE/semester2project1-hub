# ==========================================================
# Production Scheduling Optimizer (MILP)
# Single Machine - Multi Product
# ==========================================================

import pulp


def run():

    print("Production Scheduling Optimizer")
    print("--------------------------------")

    # ------------------------------------------------------
    # Sets
    # ------------------------------------------------------

    products = ["A", "B", "C"]
    periods = range(6)

    # ------------------------------------------------------
    # Parameters
    # ------------------------------------------------------

    demand = {
        "A": 80,
        "B": 60,
        "C": 40
    }

    production_cost = {
        "A": 10,
        "B": 8,
        "C": 6
    }

    setup_cost = {
        "A": 100,
        "B": 120,
        "C": 90
    }

    capacity_per_period = 50

    big_M = 1000

    # ------------------------------------------------------
    # Model
    # ------------------------------------------------------

    model = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

    # Decision Variables
    x = pulp.LpVariable.dicts(
        "Production",
        (products, periods),
        lowBound=0,
        cat="Continuous"
    )

    y = pulp.LpVariable.dicts(
        "Setup",
        (products, periods),
        cat="Binary"
    )

    # ------------------------------------------------------
    # Objective Function
    # ------------------------------------------------------

    model += (
        pulp.lpSum(production_cost[i] * x[i][t]
                   for i in products for t in periods)
        +
        pulp.lpSum(setup_cost[i] * y[i][t]
                   for i in products for t in periods)
    )

    # ------------------------------------------------------
    # Constraints
    # ------------------------------------------------------

    # Demand satisfaction
    for i in products:
        model += pulp.lpSum(x[i][t] for t in periods) >= demand[i]

    # Capacity constraint (one machine)
    for t in periods:
        model += pulp.lpSum(x[i][t] for i in products) <= capacity_per_period

    # Linking constraint
    for i in products:
        for t in periods:
            model += x[i][t] <= big_M * y[i][t]

    # Only one product per period
    for t in periods:
        model += pulp.lpSum(y[i][t] for i in products) <= 1

    # ------------------------------------------------------
    # Solve
    # ------------------------------------------------------

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    # ------------------------------------------------------
    # Results
    # ------------------------------------------------------

    print(f"\nStatus: {pulp.LpStatus[model.status]}")

    if model.status == 1:

        print("\nProduction Schedule:\n")

        for t in periods:
            for i in products:
                if y[i][t].varValue > 0.5:
                    print(f"Period {t}: Produce {i} "
                          f"({x[i][t].varValue:.2f} units)")

        print(f"\nTotal Cost: {pulp.value(model.objective):.2f}")

    else:
        print("No feasible solution found.")
