# ==========================================================
# GAS LEAK DISPERSION SIMULATION
# Gaussian Plume Model (2D Ground-Level Release)
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------
# Stability Class Dispersion Coefficients (Pasquill-Gifford)
# Simplified approximations
# ----------------------------------------------------------

def dispersion_coefficients(x, stability_class):

    # Coefficient constants for sigma_y and sigma_z
    stability_data = {
        "A": (0.22, 0.20),
        "B": (0.16, 0.12),
        "C": (0.11, 0.08),
        "D": (0.08, 0.06),
        "E": (0.06, 0.03),
        "F": (0.04, 0.016)
    }

    a, b = stability_data[stability_class]

    sigma_y = a * x
    sigma_z = b * x

    return sigma_y, sigma_z


# ----------------------------------------------------------
# Gaussian Plume Concentration
# ----------------------------------------------------------

def gaussian_plume(Q, u, x, y, stability_class):

    sigma_y, sigma_z = dispersion_coefficients(x, stability_class)

    if sigma_y == 0 or sigma_z == 0:
        return 0

    C = (Q / (2 * np.pi * u * sigma_y * sigma_z)) * \
        np.exp(-(y**2) / (2 * sigma_y**2))

    return C


# ----------------------------------------------------------
# Main Function
# ----------------------------------------------------------

def run():

    print("\n=========================================")
    print("        GAS LEAK DISPERSION MODEL")
    print("=========================================")

    try:
        Q = float(input("Leak Rate (kg/s): "))
        wind_speed = float(input("Wind Speed (m/s): "))
        LEL = float(input("Lower Explosive Limit (kg/m³): "))
    except ValueError:
        print("Invalid numeric input.")
        return

    print("\nAtmospheric Stability Class:")
    print("A (Very Unstable) to F (Very Stable)")
    stability_class = input("Select (A-F): ").upper()

    if stability_class not in ["A", "B", "C", "D", "E", "F"]:
        print("Invalid stability class.")
        return

    # ------------------------------------------------------
    # Create Grid
    # ------------------------------------------------------

    x = np.linspace(1, 500, 200)     # downwind distance (m)
    y = np.linspace(-200, 200, 200)  # crosswind distance (m)

    X, Y = np.meshgrid(x, y)

    C = np.zeros_like(X)

    for i in range(len(y)):
        for j in range(len(x)):
            C[i, j] = gaussian_plume(Q, wind_speed,
                                     X[i, j], Y[i, j],
                                     stability_class)

    # ------------------------------------------------------
    # Plot Concentration Contours
    # ------------------------------------------------------

    plt.figure(figsize=(10, 6))
    contour = plt.contourf(X, Y, C, levels=50)
    plt.colorbar(contour, label="Gas Concentration (kg/m³)")

    # Plot LEL contour
    plt.contour(X, Y, C, levels=[LEL], linestyles="dashed")

    plt.title("Gas Dispersion Contour (Gaussian Plume)")
    plt.xlabel("Downwind Distance (m)")
    plt.ylabel("Crosswind Distance (m)")

    plt.show()

    # ------------------------------------------------------
    # Estimate Hazard Distance
    # ------------------------------------------------------

    max_dist = 0

    for j in range(len(x)):
        centerline_conc = gaussian_plume(Q, wind_speed,
                                         x[j], 0,
                                         stability_class)
        if centerline_conc > LEL:
            max_dist = x[j]

    print("\n----------- RESULTS ------------------")
    print(f"Maximum Downwind Flammable Distance ≈ {max_dist:.1f} m")
    print("--------------------------------------\n")
