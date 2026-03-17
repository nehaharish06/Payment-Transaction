import logging
import os
import pandas as pd 
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/fraud_engine.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def validate_transactions(transactions, merchants):

    valid_merchants = merchants.set_index("merchant_id")

    valid_rows = []
    
    for _, row in transactions.iterrows():

        merchant_id = row["merchant_id"]

        if merchant_id not in valid_merchants.index:
            logging.error(f"Unknown merchant {merchant_id}")
            continue

        if valid_merchants.loc[merchant_id]["status"] == "BLOCKED":
            logging.error(f"Blocked merchant {merchant_id}")
            continue

        if row["transaction_amount"] <= 0:
            logging.error("Negative transaction amount")
            continue

        if row["transaction_time"] is None:
            logging.error("Invalid timestamp")
            continue

        if pd.isna(row["transaction_time"]):
            logging.error(f"Invalid timestamp for merchant {merchant_id}")
            continue

        valid_rows.append(row)

    return transactions.loc[[r.name for r in valid_rows]]