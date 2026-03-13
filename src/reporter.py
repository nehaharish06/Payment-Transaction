import json

def save_processed(transactions):
    transactions.to_csv("outputs/processed_transactions.csv", index=False)

def save_settlement(report):
    report.to_csv("outputs/merchant_settlement_report.csv", index=False)

def save_summary(transactions):

    summary = {
        "total_transactions": len(transactions),
        "valid_transactions": (transactions["transaction_status"]=="VALID").sum(),
        "fraud_transactions": (transactions["transaction_status"]=="SUSPICIOUS").sum(),
        "high_value_frauds": (transactions["fraud_reason"]=="HIGH_VALUE_TRANSACTION").sum(),
        "cross_border_frauds": (transactions["fraud_reason"]=="CROSS_BORDER_TRANSACTION").sum(),
        "rapid_transaction_frauds": (transactions["fraud_reason"]=="RAPID_TRANSACTIONS").sum()
    }

    with open("outputs/fraud_summary.json","w") as f:
        json.dump(summary,f,indent=4)