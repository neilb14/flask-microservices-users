"""Tests for user service"""
import json,datetime
from project import db
from project.tests.base import BaseTestCase
from project.api.models import User
from project.tests.utils import add_user, login_test_user

class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_add_user(self):
        """Ensure we can add a new user"""
        with self.client:
            auth_header = login_test_user(self.client)
            response = self.client.post('/users', 
                                        data=json.dumps(dict(
                                            username="neil",
                                            email="neilb14@mailinator.com",
                                            password="password123"
                                        )),
                                        content_type='application/json',
                                        headers=auth_header
                                        )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('neilb14@mailinator.com was added!', data['message'])
            self.assertIn('success', data['status'])
    
    def test_add_user_invalid_payload(self):
        """Ensure error when payload is empty"""
        with self.client:
            auth_headers = login_test_user(self.client)
            response = self.client.post('/users',
                                        data = json.dumps(dict()),
                                        content_type='application/json',
                                        headers = auth_headers
                                        )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_payload_keys(self):
        """Ensure error when payload is malformed"""
        with self.client:
            auth_header = login_test_user(self.client)
            response = self.client.post('/users',
                                        data = json.dumps(dict(email="neilb14@mailinator.com")),
                                        content_type='application/json',
                                        headers=auth_header
                                        )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload keys', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error when user with email already exists"""
        with self.client:
            auth_headers = login_test_user(self.client)
            payload = json.dumps(dict(email="neilb14@mailinator.com",username="neilb14",password="password123"))
            self.client.post('/users',
                            data = payload,
                            content_type='application/json',
                            headers = auth_headers
                            )
            response = self.client.post('/users',
                                        data = payload,
                                        content_type='application/json',
                                        headers = auth_headers
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
        created_30_days_ago = datetime.datetime.utcnow() + datetime.timedelta(-30)
        add_user('neilb', 'neilb14@mailinator.com', 'password123', created_30_days_ago)
        add_user('juneau', 'juneau@mailinator.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']),2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            self.assertIn('juneau', data['data']['users'][0]['username'])
            self.assertIn('neilb', data['data']['users'][1]['username'])
            self.assertIn('success', data['status'])

    def test_add_users_invalid_json_keys_no_password(self):
        """Ensure we get an error when no password passed in"""
        with self.client:
            auth_header = login_test_user(self.client)
            response = self.client.post('/users',
                data = json.dumps(dict(email="neilb14@mailinator.com", username="neilb14")),
                content_type='application/json',
                headers=auth_header
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload keys', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_inactive(self):
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='michael',
                    email='michael@realpython.com',
                    password='test'
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Something went wrong. Please contact us.')
            self.assertEqual(response.status_code, 401)
