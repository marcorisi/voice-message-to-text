import unittest
from flask import Flask
from flask.testing import FlaskClient
from decorators import authorize_request

class AuthorizeRequestTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.test_client_class = FlaskClient
        self.app.testing = True

        @self.app.route('/test', methods=['GET'])
        @authorize_request
        def test_route():
            return {'test': 'Authorized'}

    def test_authorized_request(self):
        with self.app.test_client() as client:
            response = client.get('/test', headers={'X-API-KEY': 'valid_key'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'test': 'Authorized'})

    def test_unauthorized_request(self):
        with self.app.test_client() as client:
            response = client.get('/test')
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json, {'error': 'Unauthorized'})
