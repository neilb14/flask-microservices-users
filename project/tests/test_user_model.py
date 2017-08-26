from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user

class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = User(
            username = 'justatest',
            email = 'just@test.com',
            password='password123'
        )
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'just@test.com')
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)

    def test_add_user_duplicate_username(self):
        add_user('juneau', 'juneau@dog.com')
        duplicate_user = User(
            username='juneau',
            email='juneau@dog4ever.com',
            password='password123'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user('juneau', 'juneau@dog.com')
        duplicate_user = User(
            username='juneau123',
            email='juneau@dog.com',
            password='password123'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        user_one = add_user('juneau', 'juneau@dog.com', 'password123')
        user_two = add_user('jersey', 'jersey@cat.com', 'password123')
        self.assertNotEqual(user_one.password, user_two.password)
    
    def test_encode_auth_token(self):
        user = add_user('juneau', 'juneau@dog.com')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user('juneau','juneau@dog.com')
        auth_token = user.encode_auth_token(user.id)
        self.assertEqual(User.decode_auth_token(auth_token), user.id)