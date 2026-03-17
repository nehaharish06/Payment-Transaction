import json
import os
os.makedirs("outputs", exist_ok=True)

def save_processed(transactions):
    transactions.to_csv("outputs/processed_transactions.csv", index=False)

def save_settlement(report):
    report.to_csv("outputs/merchant_settlement_report.csv", index=False)

def save_summary(transactions):

    summary = {
        "total_transactions": int(len(transactions)),
        "valid_transactions": int((transactions["transaction_status"]=="VALID").sum()),
        "fraud_transactions": int((transactions["transaction_status"]=="SUSPICIOUS").sum()),
        "high_value_frauds": int((transactions["fraud_reason"]=="HIGH_VALUE_TRANSACTION").sum()),
        "cross_border_frauds": int((transactions["fraud_reason"]=="CROSS_BORDER_TRANSACTION").sum()),
        "rapid_transaction_frauds": int((transactions["fraud_reason"]=="RAPID_TRANSACTIONS").sum()),
        "crypto_high_value_frauds": int((transactions["fraud_reason"]=="CRYPTO_HIGH_VALUE").sum()),
    }

    with open("outputs/fraud_summary.json","w") as f:
        json.dump(summary,f,indent=4)
