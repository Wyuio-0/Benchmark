import json
from pathlib import Path


class OrderRepository:
    def __init__(self, path):
        self.path = Path(path)

    def list_orders(self):
        return json.loads(self.path.read_text(encoding='utf-8'))['orders']

    def get(self, order_id):
        return next((order for order in self.list_orders() if order['id'] == order_id), None)

    def save_note(self, order_id, field, note):
        orders = self.list_orders()
        order = next(order for order in orders if order['id'] == order_id)
        order[field] = note
        self.path.write_text(json.dumps({'orders': orders}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
