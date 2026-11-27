import tempfile
import shutil
import unittest
from pathlib import Path
from app import create_app


class OrderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        path = Path(self.temp.name) / 'orders.json'
        shutil.copy2(Path(__file__).resolve().parents[1] / 'data/orders.json', path)
        self.client = create_app(path).test_client()

    def test_pages(self):
        for path in ('/orders', '/orders/OD-261115-01', '/backoffice/orders', '/backoffice/orders/OD-261115-01', '/health'):
            self.assertEqual(self.client.get(path).status_code, 200)
        self.assertEqual(self.client.get('/orders/not-found').status_code, 404)

    def test_save_note(self):
        response = self.client.post('/orders/OD-261115-01/note', data={'note': '下午联系\n请放前台'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('下午联系'.encode(), response.data)
        self.assertIn('请放前台'.encode(), response.data)

    def test_staff_note(self):
        response = self.client.post('/backoffice/orders/OD-261115-01/note', data={'note': '待门店复核\n明早安排'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('待门店复核'.encode(), response.data)


if __name__ == '__main__':
    unittest.main()
