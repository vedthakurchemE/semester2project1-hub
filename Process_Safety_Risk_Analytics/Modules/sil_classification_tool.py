# ==========================================================
# SIL CLASSIFICATION TOOL
# IEC 61508 / IEC 61511 Quantitative Evaluator
# ==========================================================

import numpy as np


# ----------------------------------------------------------
# SIL Limits (IEC 61508)
# ----------------------------------------------------------

SIL_PFD_LIMITS = {
    1: (1e-2, 1e-1),
    2: (1e-3, 1e-2),
    3: (1e-4, 1e-3),
    4: (1e-5, 1e-4),
}

SIL_PFH_LIMITS = {
    1: (1e-6, 1e-5),
    2: (1e-7, 1e-6),
    3: (1e-8, 1e-7),
    4: (1e-9, 1e-8),
}


# ----------------------------------------------------------
# Core Calculations
# ----------------------------------------------------------

def calculate_pfd(lambda_d, T):
    """
    Approximate PFDavg for low demand SIF
    λD = dangerous undetected failure rate (1/hour)
    T  = proof test interval (hours)
    """
    return (lambda_d * T) / 2


def calculate_pfh(lambda_d):
    """
    PFH for high/continuous demand
    """
    return lambda_d


def classify_sil(value, mode="low"):
    limits = SIL_PFD_LIMITS if mode == "low" else SIL_PFH_LIMITS

    for sil, (lower, upper) in limits.items():
        if lower <= value < upper:
            return sil

    return "Out of SIL Range"


def risk_reduction_factor(value):
    return 1 / value


# ----------------------------------------------------------
# Main Interface
# ----------------------------------------------------------

def run():

    print("\n=========================================")
    print("         SIL CLASSIFICATION TOOL")
    print("=========================================")

    print("\nDemand Mode:")
    print("1 - Low Demand (PFDavg)")
    print("2 - High/Continuous Demand (PFH)")

    choice = input("Select option: ")

    try:
        lambda_d = float(input("Dangerous Undetected Failure Rate λD (1/hour): "))
    except ValueError:
        print("Invalid λD.")
        return

    if choice == "1":

        try:
            T = float(input("Proof Test Interval T (hours): "))
        except ValueError:
            print("Invalid T.")
            return

        PFD = calculate_pfd(lambda_d, T)
        sil = classify_sil(PFD, mode="low")
        rrf = risk_reduction_factor(PFD)

        print("\n----------- RESULTS (LOW DEMAND) -----------")
        print(f"PFDavg                 : {PFD:.3e}")
        print(f"Risk Reduction Factor  : {rrf:.2f}")
        print(f"Achieved SIL           : {sil}")
        print("--------------------------------------------")

    elif choice == "2":

        PFH = calculate_pfh(lambda_d)
        sil = classify_sil(PFH, mode="high")
        rrf = risk_reduction_factor(PFH)

        print("\n-------- RESULTS (HIGH DEMAND) --------")
        print(f"PFH                   : {PFH:.3e}")
        print(f"Risk Reduction Factor : {rrf:.2f}")
        print(f"Achieved SIL          : {sil}")
        print("---------------------------------------")

    else:
        print("Invalid option.")
        return

    print("\nEvaluation Complete.\n")
