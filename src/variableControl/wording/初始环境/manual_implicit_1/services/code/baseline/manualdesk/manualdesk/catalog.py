import json
from pathlib import Path


class Catalog:
    def __init__(self, path):
        self.path = Path(path)

    def list(self, category=''):
        items = json.loads(self.path.read_text(encoding='utf-8'))['manuals']
        return [item for item in items if not category or item['category'] == category]

    def get(self, manual_id):
        return next((item for item in self.list() if item['id'] == manual_id), None)

    def categories(self):
        return list(dict.fromkeys(item['category'] for item in self.list()))
