import pandas as pd
from src.settlement_engine import generate_settlement

class TestSettlementEngine(unittest.TestCase):
    def test_settlement_only_valid_transactions(self):
        transactions = pd.DataFrame({
            "merchant_id":[1,1],
            "transaction_amount":[100,200],
            "transaction_status":["VALID","SUSPICIOUS"]
        })

        result = generate_settlement(transactions,None)

        self.assertEqual(result.iloc[0]["settlement_amount"],100)

    def test_settlement_amount_calculation(self):

        transactions = pd.DataFrame({
            "merchant_id":[1,1],
            "transaction_amount":[100,200],
            "transaction_status":["VALID","VALID"]
        })

        result = generate_settlement(transactions,None)

        self.assertEqual(result.iloc[0]["settlement_amount"],300)