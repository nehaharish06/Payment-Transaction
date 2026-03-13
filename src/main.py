from loader import load_merchants, load_transactions
from validator import validate_transactions
from fraud_engine import detect_fraud, detect_rapid_transactions
from settlement_engine import generate_settlement
from reporter import save_processed, save_settlement, save_summary

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

if __name__ == "__main__":
    main()