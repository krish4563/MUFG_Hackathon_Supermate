# agents.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans

# We'll use an internal monte carlo that supports monthly contributions
def _monte_carlo_with_contributions(initial: float, monthly_contribution: float, monthly_returns: np.ndarray, months: int, n_sim: int = 1000):
    sims = np.zeros((n_sim, months))
    for i in range(n_sim):
        capital = initial
        for m in range(months):
            r = np.random.choice(monthly_returns) if monthly_returns.size > 0 else np.random.normal(0, 0.01)
            capital = capital * (1 + r) + monthly_contribution
            sims[i, m] = capital
    return sims

def _summarize_sims(sims: np.ndarray):
    final = sims[:, -1]
    return {
        "median": float(np.percentile(final, 50)),
        "p10": float(np.percentile(final, 10)),
        "p90": float(np.percentile(final, 90)),
        "mean": float(final.mean())
    }

class BehaviorAgent:
    def __init__(self, df: pd.DataFrame = None):
        self.df = df
        self.kmeans = None
        self.features = None
        self.cluster_map = {}

    def fit(self):
        if self.df is None or self.df.empty:
            return
        g = self.df.groupby('user_id').agg({'amount': ['mean', 'std', 'count']})
        g.columns = ['avg_spend', 'std_spend', 'txn_count']
        g = g.fillna(0)
        # 2 clusters is fine for prototype: lower-spend vs higher-spend
        self.kmeans = KMeans(n_clusters=2, random_state=0, n_init=10).fit(g)
        self.features = g
        self.cluster_map = {uid: int(self.kmeans.labels_[i]) for i, uid in enumerate(g.index)}

    def profile_user(self, user_id):
        if not self.cluster_map:
            return {"behavior_cluster": None}
        return {"behavior_cluster": self.cluster_map.get(user_id, None)}

class FraudAgent:
    def __init__(self, df: pd.DataFrame = None):
        self.df = df

    def detect_user_anomalies(self, user_id):
        if self.df is None or self.df.empty:
            return {"anomaly_score": 0, "alerts": []}
        d = self.df[self.df['user_id'] == user_id].copy()
        if d.empty:
            return {"anomaly_score": 0, "alerts": []}
        X = d[['amount']].fillna(0).values
        iso = IsolationForest(contamination=0.02, random_state=42)
        iso.fit(X)
        scores = iso.decision_function(X)
        preds = iso.predict(X)
        anomalies = d[preds == -1]
        return {"anomaly_score": float(-scores.mean()), "alerts": anomalies.to_dict(orient='records')}

class PortfolioAgent:
    """
    PortfolioAgent now supports:
    - using provided prices_df to compute empirical monthly returns, OR
    - fall back to three strategy profiles (Conservative / Balanced / Growth)
      using assumed annual mu/sigma.
    It simulates growth including monthly contributions and returns per strategy.
    """
    STRATEGY_PROFILES = {
        "Conservative": {"mu": 0.04, "sigma": 0.06},   # annual
        "Balanced":     {"mu": 0.07, "sigma": 0.12},
        "Growth":       {"mu": 0.10, "sigma": 0.18}
    }

    def __init__(self, prices_df: pd.DataFrame = None):
        self.prices = prices_df

    def compute_monthly_returns_from_prices(self):
        if self.prices is None or self.prices.empty:
            return np.array([])
        p = self.prices['close'].sort_index()
        p_monthly = p.resample('M').last()
        returns = p_monthly.pct_change().dropna().values
        # monthly returns array
        return returns

    def run_superannuation_simulation(self, initial_balance: float, monthly_contribution: float, years: int = 20, n_sim: int = 1000):
        months = years * 12
        results = {}
        # If price data exists, use its empirical monthly return distribution
        empirical = self.compute_monthly_returns_from_prices()
        for name, prof in self.STRATEGY_PROFILES.items():
            if empirical.size > 0:
                monthly_returns = empirical  # empirical sampling
            else:
                mu = prof['mu']
                sigma = prof['sigma']
                # approximate monthly mean and std: divide mu by 12, sigma by sqrt(12)
                monthly_mean = mu / 12.0
                monthly_std = sigma / (12**0.5)
                # create synthetic monthly-return distribution to sample from
                monthly_returns = np.random.normal(loc=monthly_mean, scale=monthly_std, size=1200)  # pool
            sims = _monte_carlo_with_contributions(initial_balance, monthly_contribution, monthly_returns, months, n_sim=n_sim)
            summary = _summarize_sims(sims)
            results[name] = {
                "sim_summary": summary,
                "raw_sims_sample": [float(x) for x in sims[:5, -1]]  # small sample for debugging
            }
        return results
