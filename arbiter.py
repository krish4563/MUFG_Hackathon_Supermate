# arbiter.py
def merge_agent_outputs(behavior_out: dict, fraud_out: dict, portfolio_out: dict):
    # simple weighted scoring prototype
    score = 0.0
    weights = {"behavior": 0.2, "fraud": 0.4, "portfolio": 0.4}

    # behavior cluster: safer clusters -> add positive
    bcluster = behavior_out.get("behavior_cluster")
    if bcluster is None:
        score += 0
    else:
        # cluster 0 -> conservative (score +0.1), 2 -> risky (-0.1)
        score += {0: 0.1, 1: 0.0, 2: -0.1}.get(bcluster, 0)*weights['behavior']

    # fraud: higher anomaly_score reduces score
    anomaly = fraud_out.get("anomaly_score", 0)
    score += max(-1, -anomaly) * weights['fraud']  # anomaly ∈ [0..], negative contribution

    # portfolio: if median outcome > initial -> boost
    port_summary = portfolio_out.get("sim_summary", {})
    median = port_summary.get("median", 0)
    # We assume initial capital normalized e.g. 100k
    score += (median / (1 + median)) * weights['portfolio'] if median else 0

    # normalized final decision
    decision = "Hold"
    if score > 0.5:
        decision = "Aggressive increase"
    elif score < -0.2:
        decision = "Defensive reduce risk"
    else:
        decision = "Hold / Monitor"

    return {"score": float(score), "decision": decision}
