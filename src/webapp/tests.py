import unittest

from webapp.app import app

class RouteValidation(unittest.TestCase):
    
    def setUp(self):
        self.client = app.test_client()

    def test_request(self):
        response = self.client.get('/')
        # Ensure the timeline is loading correctly
        assert b'trending stories' in response.data.lower()
