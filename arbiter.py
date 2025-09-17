# arbiter.py
def merge_agent_outputs(behavior_out: dict, fraud_out: dict, portfolio_out: dict):
    """
    Combines behavior, fraud and portfolio sims into a small human-friendly verdict.
    portfolio_out is expected to be a dict with strategy keys ("Conservative", "Balanced", "Growth")
    and each contains sim_summary with median/p10/p90.
    """
    # base score
    score = 0.0
    # behavior: prefer conservative behaviour
    bcluster = behavior_out.get("behavior_cluster")
    if bcluster is None:
        score += 0.0
    else:
        # cluster mapping: 0 -> conservative, 1 -> risky (example)
        score += {0: 0.1, 1: -0.05}.get(bcluster, 0.0)

    # fraud risk reduces score
    anomaly = fraud_out.get("anomaly_score", 0)
    score -= max(0.0, anomaly) * 0.5

    # portfolio contribution: take best median among strategies and scale
    best_median = 0.0
    if portfolio_out:
        medians = []
        for k, v in portfolio_out.items():
            s = v.get("sim_summary", {})
            med = s.get("median", 0)
            medians.append(med)
        if medians:
            best_median = max(medians)
            # relative boost if best_median > initial (assume initial positive)
            score += 0.2 if best_median > 0 else 0.0

    # compute human recommendation
    if score >= 0.25:
        decision = "On Track"
    elif score >= 0.0:
        decision = "Review & Adjust"
    else:
        decision = "At Risk - Action Required"

    # simple message
    message = {
        "score": float(score),
        "decision": decision,
        "notes": {
            "behavior_summary": f"cluster={bcluster}",
            "fraud_anomaly_score": float(anomaly),
            "best_strategy_median": float(best_median)
        }
    }
    return message
