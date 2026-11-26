from src.http.client import request


def fetch_catalog(transport):
    return request(transport, "GET", "/v1/catalog/items")
