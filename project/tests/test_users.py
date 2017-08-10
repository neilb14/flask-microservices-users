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