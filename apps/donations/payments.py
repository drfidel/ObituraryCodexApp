import hashlib
import hmac
import os
import requests


class FlutterwaveService:
    endpoint = "https://api.flutterwave.com/v3/payments"

    @classmethod
    def create_payment_link(cls, amount, email, tx_ref, redirect_url):
        payload = {
            "tx_ref": tx_ref,
            "amount": str(amount),
            "currency": "UGX",
            "redirect_url": redirect_url,
            "customer": {"email": email},
        }
        headers = {
            "Authorization": f"Bearer {os.getenv('FLUTTERWAVE_SECRET_KEY', '')}",
            "Content-Type": "application/json",
        }
        return requests.post(cls.endpoint, json=payload, headers=headers, timeout=20).json()


def verify_flutterwave_signature(raw_body, signature):
    secret = os.getenv("FLUTTERWAVE_WEBHOOK_SECRET", "")
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
