# ==========================================================
# Main File - Process Optimization Projects
# ==========================================================

from Modules import (
    blending_lp,
    constrained_optimization_pyomo,
    dynamic_batch_reactor_optimization,
    hen_energy_minimization,
    multi_objective_yield_cost,
    nonlinear_reactor_volume,
    optimal_pipe_diameter,
    production_scheduling_optimizer,
    refinery_profit_optimization,
    supply_chain_optimization
)


def main():

    while True:
        print("\n========================================")
        print("        PROCESS OPTIMIZATION MENU       ")
        print("========================================")
        print("1  - Linear Programming: Blending Problem")
        print("2  - Constrained Optimization (Pyomo)")
        print("3  - Dynamic Optimization: Batch Reactor")
        print("4  - Energy Minimization (HEN)")
        print("5  - Multi-objective (Yield vs Cost)")
        print("6  - Nonlinear Optimization (Reactor Volume)")
        print("7  - Optimal Pipe Diameter")
        print("8  - Production Scheduling Optimizer")
        print("9  - Refinery Profit Optimization")
        print("10 - Supply Chain Optimization")
        print("0  - Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            blending_lp.run()

        elif choice == "2":
            constrained_optimization_pyomo.run()

        elif choice == "3":
            dynamic_batch_reactor_optimization.run()

        elif choice == "4":
            hen_energy_minimization.run()

        elif choice == "5":
            multi_objective_yield_cost.run()

        elif choice == "6":
            nonlinear_reactor_volume.run()

        elif choice == "7":
            optimal_pipe_diameter.run()

        elif choice == "8":
            production_scheduling_optimizer.run()

        elif choice == "9":
            refinery_profit_optimization.run()

        elif choice == "10":
            supply_chain_optimization.run()

        elif choice == "0":
            print("Exiting Program.")
            break

        else:
            print("Invalid selection. Try again.")


if __name__ == "__main__":
    main()
