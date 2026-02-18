# ==========================================================
# Supply Chain Optimization Model
# Multi-Echelon Network Flow MILP
# ==========================================================

import pulp


def run():

    print("Supply Chain Optimization Model")
    print("--------------------------------")

    # ------------------------------------------------------
    # Sets
    # ------------------------------------------------------

    plants = ["P1", "P2"]
    warehouses = ["W1", "W2"]
    customers = ["C1", "C2", "C3"]

    # ------------------------------------------------------
    # Parameters
    # ------------------------------------------------------

    plant_capacity = {
        "P1": 150,
        "P2": 200
    }

    warehouse_capacity = {
        "W1": 180,
        "W2": 170
    }

    demand = {
        "C1": 80,
        "C2": 120,
        "C3": 100
    }

    production_cost = {
        "P1": 10,
        "P2": 12
    }

    transport_cost_pw = {   # Plant → Warehouse
        ("P1", "W1"): 4,
        ("P1", "W2"): 6,
        ("P2", "W1"): 5,
        ("P2", "W2"): 4
    }

    transport_cost_wc = {   # Warehouse → Customer
        ("W1", "C1"): 3,
        ("W1", "C2"): 5,
        ("W1", "C3"): 6,
        ("W2", "C1"): 4,
        ("W2", "C2"): 3,
        ("W2", "C3"): 5
    }

    # ------------------------------------------------------
    # Model
    # ------------------------------------------------------

    model = pulp.LpProblem("Supply_Chain_Optimization", pulp.LpMinimize)

    # Decision Variables
    x = pulp.LpVariable.dicts(
        "Ship_PW",
        (plants, warehouses),
        lowBound=0,
        cat="Continuous"
    )

    y = pulp.LpVariable.dicts(
        "Ship_WC",
        (warehouses, customers),
        lowBound=0,
        cat="Continuous"
    )

    # ------------------------------------------------------
    # Objective Function
    # ------------------------------------------------------

    model += (
        pulp.lpSum(
            production_cost[i] * x[i][j]
            for i in plants for j in warehouses
        )
        +
        pulp.lpSum(
            transport_cost_pw[(i, j)] * x[i][j]
            for i in plants for j in warehouses
        )
        +
        pulp.lpSum(
            transport_cost_wc[(j, k)] * y[j][k]
            for j in warehouses for k in customers
        )
    )

    # ------------------------------------------------------
    # Constraints
    # ------------------------------------------------------

    # Plant capacity
    for i in plants:
        model += (
            pulp.lpSum(x[i][j] for j in warehouses)
            <= plant_capacity[i]
        )

    # Warehouse capacity
    for j in warehouses:
        model += (
            pulp.lpSum(y[j][k] for k in customers)
            <= warehouse_capacity[j]
        )

    # Flow balance at warehouse
    for j in warehouses:
        model += (
            pulp.lpSum(x[i][j] for i in plants)
            == pulp.lpSum(y[j][k] for k in customers)
        )

    # Demand satisfaction
    for k in customers:
        model += (
            pulp.lpSum(y[j][k] for j in warehouses)
            >= demand[k]
        )

    # ------------------------------------------------------
    # Solve
    # ------------------------------------------------------

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    # ------------------------------------------------------
    # Results
    # ------------------------------------------------------

    print(f"\nStatus: {pulp.LpStatus[model.status]}")

    if model.status == 1:

        print("\nOptimal Shipment Plan:\n")

        print("Plant → Warehouse:")
        for i in plants:
            for j in warehouses:
                if x[i][j].varValue > 0:
                    print(f"{i} → {j}: {x[i][j].varValue:.2f}")

        print("\nWarehouse → Customer:")
        for j in warehouses:
            for k in customers:
                if y[j][k].varValue > 0:
                    print(f"{j} → {k}: {y[j][k].varValue:.2f}")

        print(f"\nTotal Cost: {pulp.value(model.objective):.2f}")

    else:
        print("No feasible solution found.")
