import json
from project.tests.base import BaseTestCase

class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure we can add a new user"""
        with self.client:
            response = self.client.post('/users', 
                                        data=json.dumps(dict(
                                            username="neil",
                                            email="neilb14@mailinator.com"
                                        )),
                                        content_type='application/json'
                                        )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('neilb14@mailinator.com was added!', data['message'])
            self.assertIn('success', data['status'])
    
    def test_add_user_invalid_payload(self):
        """Ensure error when payload is empty"""
        with self.client:
            response = self.client.post('/users',
                                        data = json.dumps(dict()),
                                        content_type='application/json'
                                        )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_payload_keys(self):
        """Ensure error when payload is malformed"""
        with self.client:
            response = self.client.post('/users',
                                        data = json.dumps(dict(email="neilb14@mailinator.com")),
                                        content_type='application/json'
                                        )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload keys', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_user(self):
        """Ensure error when user already exists"""
        with self.client:
            payload = json.dumps(dict(email="neilb14@mailinator.com",username="neilb14"))
            self.client.post('/users',
                            data = payload,
                            content_type='application/json'
                            )
            response = self.client.post('/users',
                                        data = payload,
                                        content_type='application/json'
                                        )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('User already exists', data['message'])
            self.assertIn('fail', data['status'])