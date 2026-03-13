def generate_settlement(transactions, merchants):

    valid = transactions[transactions["transaction_status"] == "VALID"]

    settlement = valid.groupby("merchant_id")["transaction_amount"].sum().reset_index()

    settlement.rename(columns={
        "transaction_amount":"settlement_amount"
    }, inplace=True)

    return settlement