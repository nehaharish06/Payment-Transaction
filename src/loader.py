import pandas as pd

def load_merchants(file_path):
    return pd.read_csv(file_path)

def load_transactions(file_path):
    df = pd.read_csv(file_path)
    df["transaction_time"] = pd.to_datetime(df["transaction_time"], errors="coerce")
    return df

