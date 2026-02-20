# ==========================================================
# Constrained Optimization using Pyomo
# Nonlinear Programming Example
# ==========================================================

from pyomo.environ import *
from pyomo.opt import SolverFactory


def run():

    print("Constrained Optimization using Pyomo")
    print("------------------------------------")

    # ------------------------------------------------------
    # Create Model
    # ------------------------------------------------------

    model = ConcreteModel()

    # ------------------------------------------------------
    # Decision Variables
    # ------------------------------------------------------

    model.x = Var(within=NonNegativeReals)
    model.y = Var(within=NonNegativeReals)

    # ------------------------------------------------------
    # Objective Function
    # ------------------------------------------------------

    def objective_rule(m):
        return (m.x - 2)**2 + (m.y - 3)**2

    model.objective = Objective(rule=objective_rule, sense=minimize)

    # ------------------------------------------------------
    # Constraints
    # ------------------------------------------------------

    # Nonlinear constraint: circle
    def circle_constraint(m):
        return m.x**2 + m.y**2 <= 25

    model.circle = Constraint(rule=circle_constraint)

    # Linear constraint
    def linear_constraint(m):
        return m.x + m.y >= 2

    model.linear = Constraint(rule=linear_constraint)

    # ------------------------------------------------------
    # Solve
    # ------------------------------------------------------

    solver = SolverFactory("ipopt")

    results = solver.solve(model, tee=False)

    # ------------------------------------------------------
    # Results
    # ------------------------------------------------------

    print("\nStatus:", results.solver.status)
    print("Termination Condition:", results.solver.termination_condition)

    print("\nOptimal Solution:")
    print(f"x = {value(model.x):.4f}")
    print(f"y = {value(model.y):.4f}")
    print(f"Objective Value = {value(model.objective):.4f}")
