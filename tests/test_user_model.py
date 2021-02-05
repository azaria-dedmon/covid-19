"""User model tests."""

from unittest import TestCase
from sqlalchemy import exc
from models import db, User
from app import create_app


class UserModelTestCase(TestCase):
    """Test case for User Model"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.app = create_app('testing')
        self.client = self.app.test_client()

        u1 = User(firstname="test",
                    lastname="user",
                    username="testuser123",
                    email="test@test.com",
                    password="password",
                    image=None,
                    state="California",
                    vax_date=None,
                    covid_status=None)
        uid1 = 1111
        u1.id = uid1

        db.session.commit()

        u1 = User.query.get(uid1)

        self.u1 = u1
        self.uid1 = uid1

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_authentication(self):
        user = User.signup(firstname='test',
                            lastname='dummy',
                            username='test123',
                            email='tester@test.com',
                            password='password',
                            image=None,
                            state='Texas',
                            vax_date=None,
                            covid_status=None)

        user_id = 99999
        user.id = user_id
        db.session.commit()

        user = User.authenticate('test123', 'password')
        db.session.commit()

        self.assertEqual(user.username, 'test123')


    def test_invalid_username_authentication(self):
        self.assertFalse(User.authenticate("badusername", "password"))