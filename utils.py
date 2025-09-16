# utils.py
import pandas as pd

def load_user_transactions(path):
    # Load Excel or CSV
    if str(path).lower().endswith('.xlsx'):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Parse date if available
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    return df

def load_prices_csv(path):
    df = pd.read_csv(path, parse_dates=['date'])
    df = df.set_index('date').sort_index()
    return df
