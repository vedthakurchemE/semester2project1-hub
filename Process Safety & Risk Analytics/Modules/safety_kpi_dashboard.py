# ==========================================================
# SAFETY KPI DASHBOARD
# Industrial Safety Performance Monitoring Tool
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------
# KPI Calculations
# ----------------------------------------------------------

def calculate_trir(recordable_cases, hours_worked):
    return (recordable_cases * 200000) / hours_worked


def calculate_ltifr(lost_time_cases, hours_worked):
    return (lost_time_cases * 1000000) / hours_worked


def calculate_severity_rate(lost_days, hours_worked):
    return (lost_days * 1000000) / hours_worked


def calculate_psir(ps_events, hours_worked):
    return (ps_events * 200000) / hours_worked


# ----------------------------------------------------------
# Performance Classification
# ----------------------------------------------------------

def classify(value, thresholds):
    if value <= thresholds[0]:
        return "Green"
    elif value <= thresholds[1]:
        return "Amber"
    else:
        return "Red"


# ----------------------------------------------------------
# Main Dashboard Function
# ----------------------------------------------------------

def run():

    print("\n=========================================")
    print("            SAFETY KPI DASHBOARD")
    print("=========================================")

    months = 12

    recordable_cases = []
    lost_time_cases = []
    lost_days = []
    near_miss = []
    ps_events = []
    hours_worked = []

    print("\nEnter monthly data for 12 months:\n")

    for i in range(months):
        print(f"\n--- Month {i+1} ---")
        recordable_cases.append(int(input("Recordable Cases: ")))
        lost_time_cases.append(int(input("Lost Time Cases: ")))
        lost_days.append(int(input("Lost Work Days: ")))
        near_miss.append(int(input("Near Miss Reports: ")))
        ps_events.append(int(input("Process Safety Events: ")))
        hours_worked.append(float(input("Hours Worked: ")))

    # Convert to numpy arrays
    recordable_cases = np.array(recordable_cases)
    lost_time_cases = np.array(lost_time_cases)
    lost_days = np.array(lost_days)
    near_miss = np.array(near_miss)
    ps_events = np.array(ps_events)
    hours_worked = np.array(hours_worked)

    # Calculate KPIs
    trir = calculate_trir(recordable_cases, hours_worked)
    ltifr = calculate_ltifr(lost_time_cases, hours_worked)
    severity_rate = calculate_severity_rate(lost_days, hours_worked)
    psir = calculate_psir(ps_events, hours_worked)
    near_miss_rate = (near_miss * 200000) / hours_worked

    # Annual averages
    avg_trir = np.mean(trir)
    avg_ltifr = np.mean(ltifr)
    avg_psir = np.mean(psir)

    print("\n------------ ANNUAL KPI SUMMARY ------------")
    print(f"Average TRIR     : {avg_trir:.2f}")
    print(f"Average LTIFR    : {avg_ltifr:.2f}")
    print(f"Average PSIR     : {avg_psir:.2f}")
    print("---------------------------------------------")

    # Performance Classification
    trir_status = classify(avg_trir, [1.0, 2.0])
    ltifr_status = classify(avg_ltifr, [0.5, 1.0])
    psir_status = classify(avg_psir, [0.5, 1.0])

    print("\nPerformance Status:")
    print(f"TRIR  : {trir_status}")
    print(f"LTIFR : {ltifr_status}")
    print(f"PSIR  : {psir_status}")

    # ------------------------------------------------------
    # Plot KPI Trends
    # ------------------------------------------------------

    months_axis = np.arange(1, 13)

    plt.figure(figsize=(10, 6))
    plt.plot(months_axis, trir)
    plt.plot(months_axis, ltifr)
    plt.plot(months_axis, psir)

    plt.title("Safety KPI Trends (Monthly)")
    plt.xlabel("Month")
    plt.ylabel("Rate")
    plt.legend(["TRIR", "LTIFR", "PSIR"])
    plt.grid(True)
    plt.show()

    # Near Miss Trend
    plt.figure(figsize=(10, 5))
    plt.bar(months_axis, near_miss)
    plt.title("Near Miss Reporting Trend")
    plt.xlabel("Month")
    plt.ylabel("Near Miss Reports")
    plt.show()

    print("\nDashboard analysis complete.\n")
