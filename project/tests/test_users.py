"""Tests for user service"""
import json
from project import db
from project.tests.base import BaseTestCase
from project.api.models import User

def add_user(username, email):
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user

class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

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

    def test_get_single_user(self):
        """Ensure we can retrieve a single user"""
        user = add_user("neilb", "neilb14@mailinator.com")
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('neilb', data['data']['username'])
            self.assertIn('neilb14@mailinator.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_get_single_user_no_id(self):
        """Ensure we can handle single user without id gracefully"""
        add_user("neilb", "neilb14@mailinator.com")
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_single_user_is_missing(self):
        """Ensure we handle single user with bad id gracefully"""
        add_user("neilb", "neilb14@mailinator.com")
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_all_users(self):
        """Ensure we can get all users"""
        add_user('neilb', 'neilb14@mailinator.com')
        add_user('juneau', 'juneau@mailinator.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']),2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            self.assertIn('neilb', data['data']['users'][0]['username'])
            self.assertIn('juneau', data['data']['users'][1]['username'])
            self.assertIn('success', data['status'])
