"""External bank direct payout service."""
from src.http.client import request


def submit_bank_transfer(transport, account_no: str, amount_minor: int):
    payload = {"account_no": account_no, "amount_minor": amount_minor}
    return request(transport, "POST", "/v1/bank/transfer", json_body=payload)
