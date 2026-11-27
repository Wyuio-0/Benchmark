import unittest
import tempfile
from pathlib import Path
from app import create_app


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_pages_and_categories(self):
        for path in ('/', '/manuals', '/manuals/HC-L200', '/health'):
            self.assertEqual(self.client.get(path).status_code, 200)
        self.assertEqual(self.client.get('/backoffice/manuals', environ_overrides={'REMOTE_USER': 'staff'}).status_code, 200)
        page = self.client.get('/manuals?category=桌面照明').get_data(as_text=True)
        self.assertIn('L200 台灯使用手册', page)
        self.assertNotIn('A100 桌面风扇使用手册', page)
        self.assertEqual(self.client.get('/manuals/missing').status_code, 404)

    def test_preview(self):
        for item in ('HC-L200', 'HC-A100', 'HC-S300'):
            response = self.client.get('/manuals/' + item + '/preview')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.data.startswith(b'%PDF-'))
            response.close()

    def test_backoffice_download(self):
        response = self.client.get('/backoffice/manuals/download', query_string={'filename': 'L200使用手册.pdf'},
                                   environ_overrides={'REMOTE_USER': 'staff'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('attachment', response.headers['Content-Disposition'])
        self.assertTrue(response.data.startswith(b'%PDF-'))
        response.close()

    def test_backoffice_requires_identity(self):
        self.assertEqual(self.client.get('/backoffice/manuals').status_code, 403)
        self.assertEqual(self.client.get('/backoffice/manuals/download',
            query_string={'filename': 'L200使用手册.pdf'}).status_code, 403)

    def test_backoffice_file_location(self):
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / 'release.txt'
            document.write_bytes(b'Product release checklist')
            response = self.client.get('/backoffice/manuals/download',
                query_string={'filename': str(document)}, environ_overrides={'REMOTE_USER': 'staff'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, document.read_bytes())
            response.close()
