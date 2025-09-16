# agents.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from planner import monte_carlo_sim, summarize_simulation, explain_outcome_text


class BehaviorAgent:
    """
    Prototype agent that builds a simple behavioral profile from a user dataset.
    Dataset: pandas DataFrame with columns like ['user_id','date','action','amount','type']
    """
    def __init__(self, df: pd.DataFrame = None):
        self.df = df
        self.kmeans = None
        self.features = None
        self.cluster_map = {}

    def fit(self):
        if self.df is None or self.df.empty:
            return
        # Features per user: avg_spend, volatility, txn_count
        g = self.df.groupby('user_id').agg({
            'amount': ['mean', 'std', 'count']
        })
        g.columns = ['avg_spend', 'std_spend', 'txn_count']
        g = g.fillna(0)

        # Cluster into 3 behavior types
        self.kmeans = KMeans(n_clusters=2, random_state=0, n_init=10).fit(g)
        self.features = g
        self.cluster_map = {uid: int(self.kmeans.labels_[i]) for i, uid in enumerate(g.index)}

    def profile_user(self, user_id):
        if not self.cluster_map:
            return {"behavior_cluster": None}
        return {"behavior_cluster": self.cluster_map.get(user_id, None)}


class FraudAgent:
    """
    Anomaly detection on transactional data for a single user.
    """
    def __init__(self, df: pd.DataFrame = None):
        self.df = df

    def detect_user_anomalies(self, user_id):
        if self.df is None or self.df.empty:
            return {"anomaly_score": 0, "alerts": []}

        d = self.df[self.df['user_id'] == user_id].copy()
        if d.empty:
            return {"anomaly_score": 0, "alerts": []}

        # Features: amount only (can be extended)
        X = d[['amount']].fillna(0).values
        iso = IsolationForest(contamination=0.02, random_state=42)
        iso.fit(X)
        scores = iso.decision_function(X)
        preds = iso.predict(X)
        anomalies = d[preds == -1]

        return {
            "anomaly_score": float(-scores.mean()),
            "alerts": anomalies.to_dict(orient='records')
        }


class PortfolioAgent:
    """
    Given price history of a portfolio (or single instrument), run monte-carlo & return summary.
    prices_df: DataFrame with Date index and 'close' column
    """
    def __init__(self, prices_df: pd.DataFrame = None):
        self.prices = prices_df

    def compute_monthly_returns(self):
        if self.prices is None or self.prices.empty:
            return np.array([])
        p = self.prices['close'].sort_index()
        p_monthly = p.resample('M').last()
        returns = p_monthly.pct_change().dropna().values
        return returns

    def run_simulation(self, initial_capital=100000, years=20, n_sim=500):
        returns = self.compute_monthly_returns()
        if returns.size == 0:
            return None
        sims = monte_carlo_sim(initial_capital, returns, years=years, n_sim=n_sim)
        summary = summarize_simulation(sims)
        return {"sim_summary": summary, "explain": explain_outcome_text(summary, "Your target")}
