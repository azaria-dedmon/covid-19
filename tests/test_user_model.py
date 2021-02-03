"""User model tests."""
from unittest import TestCase
from sqlalchemy import exc

from models import db, User
<<<<<<< HEAD
from app import create_app
=======

from app import app
>>>>>>> covid project database structure


class UserModelTestCase(TestCase):
    """Test case for User Model"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

<<<<<<< HEAD
<<<<<<< HEAD
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
=======
        u1 = User(firstname="test", 
                    lastname="user",
                    username="testuser123", 
                    email="test@test.com", 
                    password="password", 
                    image=None, 
                    state="California", 
                    vax_date=None, 
>>>>>>> covid project database structure
=======
        u1 = User(firstname="test",
                    lastname="user",
                    username="testuser123",
                    email="test@test.com",
                    password="password",
                    image=None,
                    state="California",
                    vax_date=None,
>>>>>>> login/logout functionality"
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

<<<<<<< HEAD
=======
        self.assertEqual(len(u.review), 0)

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

>>>>>>> covid project database structure
        u_test = User.query.get(user.id)
        self.assertEqual(u_test.username, 'test123')


    def test_invalid_email_signup(self):
<<<<<<< HEAD
<<<<<<< HEAD
        """ Invalid email sign up"""
        user = User.signup('test',
                            'dummy',
                            'test123',
                            None,
                            'password',
=======
        user = User.signup('test', 
                            'dummy',
                            'test123',
                            None, 
                            'password', 
>>>>>>> covid project database structure
=======
        user = User.signup('test',
                            'dummy',
                            'test123',
                            None,
                            'password',
>>>>>>> login/logout functionality"
                            None,
                            "Texas",
                            None,
                            None)
        user_id = 991010
        user.id = user_id
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

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