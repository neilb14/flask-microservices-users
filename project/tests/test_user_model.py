from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase

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
        user = User(
            username='juneau',
            email='juneau@dog.com',
            password='password123'
        )
        db.session.add(user)
        db.session.commit()
        duplicate_user = User(
            username='juneau',
            email='juneau@dog4ever.com',
            password='password123'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)