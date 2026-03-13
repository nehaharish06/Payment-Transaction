import unittest
import pandas as pd
from src.validator import validate_transactions

class TestValidator(unittest.TestCase):

    def test_invalid_merchant_rejected(self):

        merchants = pd.DataFrame({
            "merchant_id": [1],
            "status": ["ACTIVE"]
        })

        transactions = pd.DataFrame({
            "transaction_id":[101],
            "merchant_id":[99],
            "transaction_amount":[500],
            "transaction_time":["2025-01-01"]
        })

        result = validate_transactions(transactions, merchants)

        self.assertEqual(len(result), 0)
    def test_blocked_merchant_rejected(self):

        merchants = pd.DataFrame({
            "merchant_id":[1],
            "status":["BLOCKED"]
        })

        transactions = pd.DataFrame({
            "transaction_id":[1],
            "merchant_id":[1],
            "transaction_amount":[500],
            "transaction_time":["2025-01-01"]
        })

        result = validate_transactions(transactions, merchants)

        self.assertEqual(len(result), 0)

    def test_valid_transaction_accepted(self):

        merchants = pd.DataFrame({
            "merchant_id":[1],
            "status":["ACTIVE"]
        })

        transactions = pd.DataFrame({
            "transaction_id":[1],
            "merchant_id":[1],
            "transaction_amount":[500],
            "transaction_time":["2025-01-01"]
        })

        result = validate_transactions(transactions, merchants)

        self.assertEqual(len(result), 1)

    def test_negative_amount_rejected(self):

        merchants = pd.DataFrame({
            "merchant_id":[1],
            "status":["ACTIVE"]
        })

        transactions = pd.DataFrame({
            "transaction_id":[1],
            "merchant_id":[1],
            "transaction_amount":[-200],
            "transaction_time":["2025-01-01"]
        })

        result = validate_transactions(transactions, merchants)

        self.assertEqual(len(result),0)

    def test_invalid_timestamp_handling(self):

        merchants = pd.DataFrame({
            "merchant_id":[1],
            "status":["ACTIVE"]
        })

        transactions = pd.DataFrame({
            "transaction_id":[1],
            "merchant_id":[1],
            "transaction_amount":[200],
            "transaction_time":[None]
        })

        result = validate_transactions(transactions, merchants)

        self.assertEqual(len(result),0)

    