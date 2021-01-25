"""Tests for User Model"""


# run these tests like:
#
#    python -m unittest test_user_model.py


from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Review

from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///covid-test'



db.create_all()

class UserModelTest(TestCase):
    def setUp(self):
        """Create a test client, add sample data."""
        
        db.drop_all()
        db.create_all()

        u1 = User.signup("test", "case", "test123", "test123@test.com", "test123",
                        None, "California", None, None)
        u1id = 1111
        u1.id = u1id

        db.session.commit()

        u1 = User.query.get(u1id)

        self.u1 = u1
        self.u1id = u1id

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model_signup(self):
        """Does user model work?"""

        u = User.signup(
            firstname="test",
            lastname="case",
            username="testuser",
            email="test123case@test.com",
            password="testing123",
            image=None,
            state="California",
            vax_date=None,
            covid_status=None
        )
        u_id = 12345
        u.id = u_id
        db.session.commit()

        u_test = User.query.get(u.id)
        self.assertEqual(u_test.username, "testuser")

    def test_invalid_user_model_signup(self):
        """Does invalid user work?"""
        u = User.signup(
            firstname=None,
            lastname="case",
            username="testuser",
            email="test123case@test.com",
            password="testing123",
            image=None,
            state="California",
            vax_date=None,
            covid_status=None
        )
        u_id = 67891
        u.id = u_id
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_user_login(self):
        """Does user login work?"""
        user = User.signup(
               firstname='test', 
               lastname='me', 
               username='testme123', 
               email='me@test.com', 
               password='password123',
               image=None,
               state="California",
               vax_date="08/31/2020",
               covid_status=None
        )
        user_id = 99999
        user.id = user_id
        db.session.commit()

        user = User.authenticate('testme123', 'password123')
        db.session.commit()
        self.assertEquals(user.username, 'testme123')

    def test_invalid_username_authentication(self):
        self.assertFalse(User.authenticate("badusername", "test123"))

    def test_invalid_password_authentication(self):
        self.assertFalse(User.authenticate(self.u1.username, "test"))