# utils.py
import pandas as pd
from io import BytesIO

def load_user_transactions(uploaded_file):
    if uploaded_file is None:
        return pd.DataFrame()

    content = uploaded_file.read()  # read binary
    uploaded_file.seek(0)  # reset pointer so it can be reused later

    if uploaded_file.name.lower().endswith('.xlsx'):
        df = pd.read_excel(BytesIO(content))
    else:
        df = pd.read_csv(BytesIO(content))

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Parse date if available
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    return df


def load_prices_csv(uploaded_file):
    if uploaded_file is None:
        return pd.DataFrame()

    content = uploaded_file.read()
    uploaded_file.seek(0)

    df = pd.read_csv(BytesIO(content), parse_dates=['date'])
    df = df.set_index('date').sort_index()
    return df
