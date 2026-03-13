import unittest
import pandas as pd
from src.fraud_engine import detect_fraud
from src.fraud_engine import detect_rapid_transactions


class TestFraudEngine(unittest.TestCase):

    def test_high_value_transaction_flag(self):

        merchants = pd.DataFrame({
            "merchant_id": [1],
            "country": ["US"]
        })

        transactions = pd.DataFrame({
            "transaction_id": [1],
            "merchant_id": [1],
            "customer_id": [10],
            "transaction_amount": [200000],
            "transaction_time": ["2025-01-01"],
            "payment_method": ["CARD"],
            "country": ["US"]
        })

        result = detect_fraud(transactions, merchants)

        self.assertEqual(result.iloc[0]["transaction_status"], "SUSPICIOUS")



    def test_cross_border_transaction_flag(self):

        merchants = pd.DataFrame({
            "merchant_id": [1],
            "country": ["US"]
        })

        transactions = pd.DataFrame({
            "transaction_id": [1],
            "merchant_id": [1],
            "customer_id": [10],
            "transaction_amount": [1000],
            "transaction_time": ["2025-01-01"],
            "payment_method": ["CARD"],
            "country": ["UK"]
        })

        result = detect_fraud(transactions, merchants)

        self.assertEqual(result.iloc[0]["transaction_status"], "SUSPICIOUS")



    def test_crypto_high_value_flag(self):

        merchants = pd.DataFrame({
            "merchant_id": [1],
            "country": ["US"]
        })

        transactions = pd.DataFrame({
            "transaction_id": [1],
            "merchant_id": [1],
            "customer_id": [10],
            "transaction_amount": [60000],
            "transaction_time": ["2025-01-01"],
            "payment_method": ["CRYPTO"],
            "country": ["US"]
        })

        result = detect_fraud(transactions, merchants)

        self.assertEqual(result.iloc[0]["transaction_status"], "SUSPICIOUS")



    def test_multiple_fraud_rules_trigger(self):

        merchants = pd.DataFrame({
            "merchant_id": [1],
            "country": ["US"]
        })

        transactions = pd.DataFrame({
            "transaction_id": [1],
            "merchant_id": [1],
            "customer_id": [10],
            "transaction_amount": [120000],
            "transaction_time": ["2025-01-01"],
            "payment_method": ["CRYPTO"],
            "country": ["UK"]
        })

        result = detect_fraud(transactions, merchants)

        self.assertTrue(result.iloc[0]["fraud_flag"])



    def test_rapid_transactions_flagged(self):

        transactions = pd.DataFrame({
            "customer_id": [1,1,1,1],
            "transaction_time": pd.to_datetime([
                "2025-01-01 10:00:00",
                "2025-01-01 10:00:30",
                "2025-01-01 10:01:00",
                "2025-01-01 10:01:30"
            ])
        })

        # Ensure fraud columns exist
        transactions["fraud_flag"] = False
        transactions["fraud_reason"] = ""
        transactions["transaction_status"] = "VALID"

        result = detect_rapid_transactions(transactions)

        self.assertTrue(result["fraud_flag"].any())



    def test_transactions_outside_window_not_flagged(self):

        transactions = pd.DataFrame({
            "customer_id": [1,1,1],
            "transaction_time": pd.to_datetime([
                "2025-01-01 10:00:00",
                "2025-01-01 10:10:00",
                "2025-01-01 10:20:00"
            ])
        })

        # Ensure fraud columns exist
        transactions["fraud_flag"] = False
        transactions["fraud_reason"] = ""
        transactions["transaction_status"] = "VALID"

        result = detect_rapid_transactions(transactions)

        self.assertFalse(result["fraud_flag"].any())


if __name__ == "__main__":
    unittest.main()