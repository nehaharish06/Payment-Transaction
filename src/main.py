from loader import load_merchants, load_transactions
from validator import validate_transactions
from fraud_engine import detect_fraud, detect_rapid_transactions, generate_fraud_summary, generate_fraud_alerts, calculate_risk_score
from settlement_engine import generate_settlement
from reporter import save_processed, save_settlement, save_summary
import pandas as pd
import matplotlib.pyplot as plt
def main():

    merchants = load_merchants("data/merchants.csv")
    transactions = load_transactions("data/transactions.csv")

    transactions = validate_transactions(transactions, merchants)

    transactions = detect_fraud(transactions, merchants)

    transactions = transactions.merge(
        merchants[["merchant_id","country"]],
        on="merchant_id",
        how="left",
        suffixes=("","_merchant")
    )

    transactions.rename(columns={"country_merchant":"merchant_country"}, inplace=True)

    transactions = calculate_risk_score(transactions)

    transactions = detect_rapid_transactions(transactions)

    alerts = generate_fraud_alerts(transactions)

    alerts.to_csv("outputs/fraud_alerts.csv", index=False)
    settlement = generate_settlement(transactions, merchants)

    save_processed(transactions)
    save_settlement(settlement)
    save_summary(transactions)
    

    fraud_counts = transactions["transaction_status"].value_counts()


    # Create pie chart
    plt.figure()
    plt.pie(
        fraud_counts,
        labels=fraud_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=["lightcoral", "lightblue"]
    )

    plt.title("Transaction Status Distribution")
    plt.axis('equal')  
    plt.savefig("outputs/transaction_status_distribution.png")

if __name__ == "__main__":
    main()