from src.client import HezhouPayClient

if __name__ == "__main__":
    cli = HezhouPayClient()
    req = cli.create_order("DEMO-20261122-001", 19900, "企业版年度订阅")
    print(req)
