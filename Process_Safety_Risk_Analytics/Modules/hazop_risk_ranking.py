# ==========================================================
# HAZOP RISK RANKING TOOL
# Professional Version with Heatmap + CSV Export
# ==========================================================

import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np


# ----------------------------------------------------------
# Risk Classification Based on 5x5 Matrix
# ----------------------------------------------------------

def classify_risk(score):
    if score <= 5:
        return "Low"
    elif 6 <= score <= 10:
        return "Medium"
    elif 11 <= score <= 15:
        return "High"
    else:
        return "Extreme"


# ----------------------------------------------------------
# Generate Risk Matrix (5x5)
# ----------------------------------------------------------

def generate_risk_matrix():
    matrix = np.zeros((5, 5))

    for severity in range(1, 6):
        for likelihood in range(1, 6):
            matrix[5 - likelihood][severity - 1] = severity * likelihood

    return matrix


# ----------------------------------------------------------
# Plot Heatmap
# ----------------------------------------------------------

def plot_heatmap(selected_severity, selected_likelihood):

    matrix = generate_risk_matrix()

    plt.figure(figsize=(7, 6))
    plt.imshow(matrix, cmap="YlOrRd")

    plt.colorbar(label="Risk Score")

    plt.xticks(range(5), [1, 2, 3, 4, 5])
    plt.yticks(range(5), [5, 4, 3, 2, 1])

    plt.xlabel("Severity")
    plt.ylabel("Likelihood")
    plt.title("HAZOP Risk Matrix (5x5)")

    # Highlight selected point
    plt.scatter(selected_severity - 1,
                5 - selected_likelihood,
                color="blue",
                s=200,
                marker="o")

    plt.show()


# ----------------------------------------------------------
# Export to CSV (Risk Register)
# ----------------------------------------------------------

def export_to_csv(data):

    filename = "hazop_risk_register.csv"

    file_exists = False
    try:
        with open(filename, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date",
                "Deviation",
                "Cause",
                "Consequence",
                "Severity",
                "Likelihood",
                "Initial Risk",
                "Initial Category",
                "Safeguard Credit",
                "Residual Risk",
                "Residual Category"
            ])

        writer.writerow(data)

    print(f"\nData exported to {filename}")


# ----------------------------------------------------------
# Main Run Function
# ----------------------------------------------------------

def run():

    print("\n=========================================")
    print("        HAZOP RISK RANKING TOOL")
    print("=========================================")

    deviation = input("Deviation (e.g., High Pressure): ")
    cause = input("Cause: ")
    consequence = input("Consequence: ")

    try:
        severity = int(input("Severity (1-5): "))
        likelihood = int(input("Likelihood (1-5): "))
        safeguard_credit = int(input("Safeguard Reduction (0-5): "))
    except ValueError:
        print("Invalid input. Use integers only.")
        return

    # ---------------- Validation ----------------

    if not (1 <= severity <= 5):
        print("Severity must be between 1 and 5.")
        return

    if not (1 <= likelihood <= 5):
        print("Likelihood must be between 1 and 5.")
        return

    if not (0 <= safeguard_credit <= 5):
        print("Safeguard credit must be between 0 and 5.")
        return

    # ---------------- Risk Calculations ----------------

    initial_risk = severity * likelihood
    residual_risk = max(initial_risk - safeguard_credit, 0)

    initial_category = classify_risk(initial_risk)
    residual_category = classify_risk(residual_risk)

    # ---------------- Output ----------------

    print("\n----------- RESULTS ----------------")
    print(f"Deviation         : {deviation}")
    print(f"Cause             : {cause}")
    print(f"Consequence       : {consequence}")
    print(f"Initial Risk      : {initial_risk} ({initial_category})")
    print(f"Residual Risk     : {residual_risk} ({residual_category})")
    print("------------------------------------")

    # ---------------- Heatmap ----------------

    show_matrix = input("\nShow Risk Matrix Heatmap? (y/n): ").lower()
    if show_matrix == "y":
        plot_heatmap(severity, likelihood)

    # ---------------- Export ----------------

    export_choice = input("Export to CSV risk register? (y/n): ").lower()

    if export_choice == "y":

        today = datetime.date.today()

        data = [
            today,
            deviation,
            cause,
            consequence,
            severity,
            likelihood,
            initial_risk,
            initial_category,
            safeguard_credit,
            residual_risk,
            residual_category
        ]

        export_to_csv(data)

    print("\nHAZOP analysis complete.\n")
