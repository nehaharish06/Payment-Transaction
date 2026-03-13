from loader import load_merchants, load_transactions
from validator import validate_transactions
from fraud_engine import detect_fraud, detect_rapid_transactions, generate_fraud_summary
from settlement_engine import generate_settlement
from reporter import save_processed, save_settlement, save_summary
import pandas as pd
def main():

    merchants = load_merchants("data/merchants.csv")
    transactions = load_transactions("data/transactions.csv")

    transactions = validate_transactions(transactions, merchants)

    transactions = detect_fraud(transactions, merchants)

    transactions = detect_rapid_transactions(transactions)

    settlement = generate_settlement(transactions, merchants)

    save_processed(transactions)
    save_settlement(settlement)
    save_summary(transactions)

    # Example transactions
    transactions = pd.DataFrame({
        "transaction_id":[1,2,3],
        "transaction_status":["VALID","SUSPICIOUS","SUSPICIOUS"]
    })

    summary = generate_fraud_summary(transactions)

    print("Fraud Summary Report")
    print("--------------------")
    print("Total Transactions:", summary["total_transactions"])
    print("Suspicious Transactions:", summary["suspicious_transactions"])
    print("Fraud Rate:", summary["fraud_rate_percent"], "%")

if __name__ == "__main__":
    main()