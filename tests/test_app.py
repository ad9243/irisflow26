import tempfile
import unittest
from pathlib import Path
import sqlite3
import app as website

class WebsiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.original = website.DATABASE
        website.DATABASE = Path(self.temp.name) / 'inquiries.sqlite3'
        self.client = website.app.test_client()
    def tearDown(self):
        website.DATABASE = self.original
        self.temp.cleanup()
    def test_pages_and_assets(self):
        for route, text in [('/', b'Less busywork.'), ('/team', b'Introductions are on the way.'), ('/blog', b'THE FLOW JOURNAL')]:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            self.assertIn(text, response.data)
        for path in ('/static/style.css', '/static/app.js', '/static/logo.svg'):
            with self.client.get(path) as response:
                self.assertEqual(response.status_code, 200)
    def test_inquiry_persists(self):
        data = dict(name='Test Person', email='test@example.com', company='Studio', service='Workflow automation', message='Help automate our onboarding.')
        response = self.client.post('/api/inquiries', json=data)
        self.assertEqual(response.status_code, 201)
        with sqlite3.connect(website.DATABASE) as db:
            self.assertEqual(db.execute('SELECT name, email, service FROM inquiries').fetchone(), ('Test Person', 'test@example.com', 'Workflow automation'))
    def test_invalid_inquiries_are_rejected(self):
        for data in ({}, [], dict(name='Alex', email='invalid', message='A real project brief', service='AI assistants')):
            self.assertEqual(self.client.post('/api/inquiries', json=data).status_code, 400)
        self.assertFalse(website.DATABASE.exists())
    def test_sql_input_is_stored_as_text(self):
        data = dict(name="Robert'); DROP TABLE inquiries;--", email='test@example.com', company='', service='AI assistants', message='A useful project request.')
        self.assertEqual(self.client.post('/api/inquiries', json=data).status_code, 201)
        with sqlite3.connect(website.DATABASE) as db:
            self.assertEqual(db.execute('SELECT name FROM inquiries').fetchone()[0], data['name'])

if __name__ == '__main__':
    unittest.main()
