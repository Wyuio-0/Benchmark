from src.http.client import request


def fetch_quote(transport, sku_id: str):
    return request(transport, "GET", f"/v1/pricing/quotes/{sku_id}")
