import pandas as pd

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