"""Shared upstream HTTP client wrapper for gateway-router."""


def request(transport, method: str, url: str, json_body=None, max_retries: int = 0):
    attempts = 0
    while True:
        response = transport(method, url, json_body)
        if response.get("status") != 504 or attempts >= max_retries:
            return response
        attempts += 1
