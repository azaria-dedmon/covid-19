"""User model tests."""

from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Review

from app import app




class UserModelTestCase(TestCase):
    """Test case for User Model"""

    def setUp(self):
        """Create test client, add sample data."""

        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///covidtest'

        db.drop_all()
        db.create_all()

        u1 = User(firstname="test", lastname="user", username="testuser123", 
        email="test@test.com", password="password", image=None, 
        state="California", vax_date=None, covid_status=None)
        uid1 = 1111
        u1.id = uid1

        db.session.commit()

        u1 = User.query.get(uid1)

        self.u1 = u1
        self.uid1 = uid1

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            firstname='test',
            lastname='case',
            username="testuser",
            email="test@testing.com",
            password="HASHED_PASSWORD",
            image=None,
            state="Arizona"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.review), 0)
