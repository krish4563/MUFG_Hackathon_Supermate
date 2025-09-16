# planner.py
import numpy as np
import pandas as pd

def monte_carlo_sim(initial_capital: float, returns: np.ndarray, years: int = 30, n_sim: int = 1000):
    """
    returns: historical returns series (daily or monthly). We'll assume monthly returns in decimals.
    """
    # Convert historical returns to monthly mean/std
    mu = np.nanmean(returns)
    sigma = np.nanstd(returns)

    steps = years * 12
    sims = np.zeros((n_sim, steps))
    for i in range(n_sim):
        monthly = np.random.normal(mu/12, sigma/np.sqrt(12), steps)
        price = initial_capital * np.cumprod(1 + monthly)
        sims[i, :] = price
    return sims

def summarize_simulation(sims: np.ndarray):
    final_vals = sims[:, -1]
    median = np.percentile(final_vals, 50)
    p10 = np.percentile(final_vals, 10)
    p90 = np.percentile(final_vals, 90)
    return {"median": float(median), "p10": float(p10), "p90": float(p90), "mean": float(final_vals.mean())}

def explain_outcome_text(summary: dict, user_goal_text: str):
    # Simple explainability mapping numbers to plain language
    median = summary['median']
    p10 = summary['p10']
    p90 = summary['p90']
    return (f"Given your inputs and the simulated market variability, the median outcome in {median:,.0f}. "
            f"There is a 10% risk your capital ends around {p10:,.0f} and a 10% chance it could reach {p90:,.0f}. "
            f"In simple terms: {user_goal_text} — the simulations say median outcome aligns with that level of target with the confidence bands above.")
