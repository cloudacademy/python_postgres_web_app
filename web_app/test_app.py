# Tests for the Flask application contained in the app.py file.

import unittest

from app import app

class TestApp(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(TestApp, self).__init__(*args, **kwargs)
        self.app = app.test_client()   

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'welcome to overshare!' in response.data.lower())
    
    def test_timeline(self):
        response = self.app.get('/timeline')
        self.assertEqual(response.status_code, 500)
        self.assertTrue(b'is the database up and running?' in response.data.lower())

    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'logging in...' in response.data.lower())
