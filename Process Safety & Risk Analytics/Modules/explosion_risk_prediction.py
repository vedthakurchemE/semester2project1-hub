# ==========================================================
# EXPLOSION RISK PREDICTION MODEL - FULL VERSION
# Includes TNT equivalency + Overpressure + Monte Carlo
# ==========================================================

import math
import csv
import datetime
import numpy as np


# ----------------------------------------------------------
# Gas Database (Simplified)
# ----------------------------------------------------------

GAS_DATABASE = {
    "Methane": {"LEL": 5.0, "UEL": 15.0, "heat_of_combustion": 50000},  # kJ/kg
    "Propane": {"LEL": 2.1, "UEL": 9.5, "heat_of_combustion": 46000},
    "Hydrogen": {"LEL": 4.0, "UEL": 75.0, "heat_of_combustion": 120000},
    "Ethylene": {"LEL": 2.7, "UEL": 36.0, "heat_of_combustion": 47000}
}

TNT_ENERGY = 4184  # kJ/kg


# ----------------------------------------------------------
# Risk Classification
# ----------------------------------------------------------

def classify_risk(score):
    if score < 0.2:
        return "Low"
    elif score < 0.5:
        return "Moderate"
    elif score < 0.8:
        return "High"
    else:
        return "Critical"


# ----------------------------------------------------------
# TNT Equivalent Calculation
# ----------------------------------------------------------

def tnt_equivalent(mass_gas, heat_combustion):
    """
    Converts released gas energy to TNT equivalent (kg)
    """
    explosion_efficiency = 0.1  # typical 10%
    energy = mass_gas * heat_combustion * explosion_efficiency
    return energy / TNT_ENERGY


# ----------------------------------------------------------
# Overpressure Estimation (Scaled Distance)
# ----------------------------------------------------------

def estimate_overpressure(tnt_mass, distance):
    """
    Simplified scaled distance method
    """
    if tnt_mass <= 0:
        return 0

    Z = distance / (tnt_mass ** (1/3))

    # Empirical approximation (kPa)
    overpressure = 1772 / (Z ** 3 + 6)

    return overpressure


# ----------------------------------------------------------
# Monte Carlo Risk Simulation
# ----------------------------------------------------------

def monte_carlo(concentration, LEL, UEL,
                temperature, ignition_prob,
                confinement, simulations=50000):

    results = []

    for _ in range(simulations):

        conc = np.random.normal(concentration, 0.05 * concentration)
        temp = np.random.normal(temperature, 5)

        if conc < LEL or conc > UEL:
            results.append(0)
            continue

        flammability_factor = (conc - LEL) / (UEL - LEL)
        temperature_factor = temp / 298

        ERI = flammability_factor * temperature_factor \
              * ignition_prob * confinement

        results.append(ERI)

    return np.mean(results)


# ----------------------------------------------------------
# CSV Export
# ----------------------------------------------------------

def export_to_csv(data):

    filename = "explosion_risk_register.csv"

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
                "Date", "Gas", "Concentration (%)",
                "Temperature (K)", "Explosion Risk Index",
                "Risk Level", "TNT Equivalent (kg)",
                "Estimated Overpressure (kPa)"
            ])

        writer.writerow(data)

    print(f"\nData exported to {filename}")


# ----------------------------------------------------------
# Main Function
# ----------------------------------------------------------

def run():

    print("\n=========================================")
    print("      EXPLOSION RISK PREDICTION MODEL")
    print("=========================================")

    print("\nAvailable Gases:")
    for i, gas in enumerate(GAS_DATABASE.keys(), 1):
        print(f"{i} - {gas}")

    try:
        gas_choice = int(input("Select Gas: "))
        gas_name = list(GAS_DATABASE.keys())[gas_choice - 1]
    except:
        print("Invalid selection.")
        return

    gas_data = GAS_DATABASE[gas_name]
    LEL = gas_data["LEL"]
    UEL = gas_data["UEL"]
    heat_comb = gas_data["heat_of_combustion"]

    try:
        concentration = float(input("Gas Concentration (% volume): "))
        temperature = float(input("Temperature (K): "))
        ignition_probability = float(input("Ignition Probability (0-1): "))
        confinement_factor = float(input("Confinement Factor (0-1): "))
        mass_release = float(input("Estimated Gas Mass Released (kg): "))
        distance = float(input("Distance from Explosion (m): "))
    except ValueError:
        print("Invalid numeric input.")
        return

    if concentration < LEL or concentration > UEL:
        print("\nMixture outside flammable range.")
        print("Explosion Risk: Negligible")
        return

    flammability_factor = (concentration - LEL) / (UEL - LEL)
    temperature_factor = temperature / 298.0

    ERI = flammability_factor * temperature_factor \
          * ignition_probability * confinement_factor

    risk_level = classify_risk(ERI)

    # TNT Equivalent
    tnt_mass = tnt_equivalent(mass_release, heat_comb)

    # Overpressure
    overpressure = estimate_overpressure(tnt_mass, distance)

    print("\n------------- RESULTS ------------------")
    print(f"Gas                     : {gas_name}")
    print(f"Explosion Risk Index    : {ERI:.3f}")
    print(f"Risk Classification     : {risk_level}")
    print(f"TNT Equivalent (kg)     : {tnt_mass:.2f}")
    print(f"Estimated Overpressure  : {overpressure:.2f} kPa")

    if overpressure > 50:
        print("Severe structural damage likely.")
    elif overpressure > 20:
        print("Window breakage / light damage possible.")
    elif overpressure > 5:
        print("Minor structural damage possible.")
    else:
        print("Minimal structural damage expected.")

    # Monte Carlo Option
    simulate = input("\nRun Monte Carlo simulation? (y/n): ").lower()

    if simulate == "y":
        mc_risk = monte_carlo(concentration, LEL, UEL,
                              temperature, ignition_probability,
                              confinement_factor)
        print(f"Average ERI (Monte Carlo): {mc_risk:.3f}")

    # Export Option
    export = input("Export to CSV risk register? (y/n): ").lower()

    if export == "y":
        today = datetime.date.today()
        export_to_csv([
            today, gas_name, concentration,
            temperature, ERI, risk_level,
            tnt_mass, overpressure
        ])

    print("\nExplosion risk analysis complete.\n")
