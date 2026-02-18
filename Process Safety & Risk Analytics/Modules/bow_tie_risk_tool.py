# ==========================================================
# BOW-TIE RISK ANALYSIS TOOL
# Quantitative Barrier-Based Risk Evaluation
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


# ----------------------------------------------------------
# Core Probability Logic
# ----------------------------------------------------------

def top_event_probability(threats, barriers):
    """
    threats: list of threat probabilities
    barriers: list of barrier effectiveness (0–1)
    """

    # Combined threat probability (OR logic)
    P_threat = 1 - np.prod([1 - p for p in threats])

    # Combined prevention barrier failure probability
    P_barrier_fail = np.prod([1 - eff for eff in barriers])

    return P_threat * P_barrier_fail


def consequence_probability(top_event_prob, mitigation_effectiveness):
    """
    mitigation_effectiveness: list of mitigation barrier effectiveness (0–1)
    """

    P_mitigation_fail = np.prod([1 - eff for eff in mitigation_effectiveness])
    return top_event_prob * P_mitigation_fail


# ----------------------------------------------------------
# Visualization
# ----------------------------------------------------------

def plot_bow_tie(threats, top_event, consequences):

    G = nx.DiGraph()

    # Add nodes
    for t in threats:
        G.add_edge(t, top_event)

    for c in consequences:
        G.add_edge(top_event, c)

    pos = {}

    # Left side (threats)
    for i, t in enumerate(threats):
        pos[t] = (-2, i)

    pos[top_event] = (0, len(threats) / 2)

    # Right side (consequences)
    for i, c in enumerate(consequences):
        pos[c] = (2, i)

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=3000)
    plt.title("Bow-Tie Risk Diagram")
    plt.show()


# ----------------------------------------------------------
# Main Tool
# ----------------------------------------------------------

def run():

    print("\n=========================================")
    print("           BOW-TIE RISK TOOL")
    print("=========================================")

    hazard = input("Enter Hazard Name: ")
    top_event = input("Enter Top Event: ")

    # ---------------- Threats ----------------
    n_threats = int(input("Number of Threats: "))
    threats = []
    threat_probs = []

    for i in range(n_threats):
        name = input(f"Threat {i+1} Name: ")
        prob = float(input("Probability (0-1): "))
        threats.append(name)
        threat_probs.append(prob)

    # ---------------- Prevention Barriers ----------------
    n_barriers = int(input("Number of Prevention Barriers: "))
    prevention_eff = []

    for i in range(n_barriers):
        eff = float(input(f"Barrier {i+1} Effectiveness (0-1): "))
        prevention_eff.append(eff)

    # Calculate Top Event Probability
    P_top = top_event_probability(threat_probs, prevention_eff)

    print(f"\nTop Event Probability = {P_top:.6f}")

    # ---------------- Consequences ----------------
    n_cons = int(input("\nNumber of Consequences: "))
    consequences = []
    cons_probs = []

    for i in range(n_cons):
        name = input(f"Consequence {i+1} Name: ")
        mitigation_n = int(input("Number of Mitigation Barriers: "))

        mitigation_eff = []
        for j in range(mitigation_n):
            eff = float(input(f"Mitigation Barrier {j+1} Effectiveness (0-1): "))
            mitigation_eff.append(eff)

        P_cons = consequence_probability(P_top, mitigation_eff)

        consequences.append(name)
        cons_probs.append(P_cons)

        print(f"Probability of {name} = {P_cons:.6f}")

    # ---------------- Visualization ----------------
    plot_bow_tie(threats, top_event, consequences)

    print("\nRisk Analysis Complete.\n")
