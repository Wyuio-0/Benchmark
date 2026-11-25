import hashlib
import hmac
import json
import os
import urllib.request


class HezhouPayClient:
    def __init__(self, base_url=None, mch_id=None, secret=None):
        self.base_url = base_url or os.getenv("GATEWAY_BASE_URL", "https://sandbox-api.hezhou-pay.com")
        self.mch_id = mch_id or os.getenv("MCH_ID", "")
        self.secret = secret or os.getenv("MCH_SECRET", "")

    def sign(self, payload: dict) -> str:
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hmac.new(self.secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()

    def create_order(self, out_trade_no: str, amount_fen: int, subject: str) -> dict:
        body = {
            "mch_id": self.mch_id,
            "out_trade_no": out_trade_no,
            "amount_fen": amount_fen,
            "subject": subject,
        }
        return {"url": f"{self.base_url}/v2/orders", "headers": {"X-Signature": self.sign(body)}, "body": body}
