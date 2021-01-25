"""User model tests."""
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Review

from app import create_app


class UserModelTestCase(TestCase):
    """Test case for User Model"""

    def setUp(self):
        """Create test client, add sample data."""

        self.app = create_app('testing')
        self.client = self.app.test_client()
        db.drop_all()
        db.create_all()

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

    def test_signup(self):
        """Are users able to sign up?"""
        user = User.signup('test',
                            'dummy',
                            'test123',
                            'dummytest@test.com',
                            'password',
                            None,
                            "Texas",
                            None,
                            None)
        user_id = 99999
        user.id = user_id
        db.session.commit()

        u_test = User.query.get(user.id)
        self.assertEqual(u_test.username, 'test123')


    def test_invalid_email_signup(self):
        user = User.signup('test',
                            'dummy',
                            'test123',
                            None,
                            'password',
                            None,
                            "Texas",
                            None,
                            None)
        user_id = 991010
        user.id = user_id
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
