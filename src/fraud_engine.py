import pandas as pd
from datetime import datetime
def detect_fraud(transactions, merchants):

    merchants_map = merchants.set_index("merchant_id")

    transactions["fraud_flag"] = False
    transactions["fraud_reason"] = ""
    transactions["transaction_status"] = "VALID"

    # Rule 1: High value
    mask = transactions["transaction_amount"] > 100000
    transactions.loc[mask, ["fraud_flag","fraud_reason","transaction_status"]] = \
        [True, "HIGH_VALUE_TRANSACTION", "SUSPICIOUS"]

    # Rule 2: Cross border
    for i, row in transactions.iterrows():
        merchant_country = merchants_map.loc[row["merchant_id"]]["country"]
        if row["country"] != merchant_country:
            transactions.at[i,"fraud_flag"] = True
            transactions.at[i,"fraud_reason"] = "CROSS_BORDER_TRANSACTION"
            transactions.at[i,"transaction_status"] = "SUSPICIOUS"

    # Rule 4: Crypto high value
    mask = (transactions["payment_method"] == "CRYPTO") & \
           (transactions["transaction_amount"] > 50000)

    transactions.loc[mask,["fraud_flag","fraud_reason","transaction_status"]] = \
        [True,"CRYPTO_HIGH_VALUE","SUSPICIOUS"]

    return transactions
# Rule 3: Rapid transactions
def detect_rapid_transactions(df):

    df = df.sort_values("transaction_time")

    for customer_id, group in df.groupby("customer_id"):

        times = group["transaction_time"]

        for i in range(len(times)-3):

            window = times.iloc[i:i+4]

            if (window.max() - window.min()).seconds <= 120:

                idx = group.index[i:i+4]

                df.loc[idx,"fraud_flag"] = True
                df.loc[idx,"fraud_reason"] = "RAPID_TRANSACTIONS"
                df.loc[idx,"transaction_status"] = "SUSPICIOUS"

    return df


def calculate_risk_score(df):

    df["risk_score"] = 0

    # High value transaction
    df.loc[df["transaction_amount"] > 100000, "risk_score"] += 40

    # Crypto high value
    df.loc[(df["payment_method"] == "CRYPTO") & 
           (df["transaction_amount"] > 50000), "risk_score"] += 30

    # Cross border transaction
    df.loc[df["country"] != df["merchant_country"], "risk_score"] += 30

    return df

def detect_duplicate_transactions(df):

    df = df.sort_values("transaction_time")

    df["duplicate_flag"] = False

    for customer_id, group in df.groupby("customer_id"):

        for i in range(len(group)-1):

            t1 = group.iloc[i]
            t2 = group.iloc[i+1]

            if (
                t1["transaction_amount"] == t2["transaction_amount"] and
                t1["merchant_id"] == t2["merchant_id"] and
                (t2["transaction_time"] - t1["transaction_time"]).seconds <= 10
            ):

                df.loc[group.index[i+1], "duplicate_flag"] = True

    return df

def generate_fraud_summary(df):

    total_transactions = len(df)

    suspicious_transactions = len(
        df[df["transaction_status"] == "SUSPICIOUS"]
    )

    fraud_rate = (suspicious_transactions / total_transactions) * 100

    summary = {
        "total_transactions": total_transactions,
        "suspicious_transactions": suspicious_transactions,
        "fraud_rate_percent": round(fraud_rate, 2)
    }

    return summary


def generate_fraud_alerts(df):

    alerts = df[df["transaction_status"] == "SUSPICIOUS"].copy()

    if alerts.empty:
        return pd.DataFrame()

    alerts["alert_time"] = datetime.now()

    alert_columns = [
        "transaction_id",
        "customer_id",
        "fraud_reason",
        "risk_score",
        "alert_time"
    ]

    alerts = alerts[alert_columns]

    return alerts