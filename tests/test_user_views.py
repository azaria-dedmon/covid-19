"""User View tests."""

from unittest import TestCase
from models import db, User
from app import create_app, CURR_USER_KEY
from sqlalchemy.exc import InvalidRequestError

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.testuser = User.signup('test',
                            'dummy',
                            'test123',
                            'dummytest@test.com',
                            'password',
                            None,
                            "Texas",
                            None,
                            None)
        self.uid = 1111
        self.testuser.id = self.uid
        db.session.commit()

<<<<<<< HEAD
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_register_redirect(self):
       with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post('/register', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

    def test_user_signup(self):
        user = User.signup('tester',
                            'person',
                            'test1234',
                            'dummytest2@test.com',
                            'password',
                            None,
                            "Texas",
                            None,
                            None)
        uid = 22222
        user.id = uid

        db.session.commit()

        with self.client as client:
            resp = client.post('/register', data={'firstname': 'tester',
                                                  'lastname': 'person',
                                                  'username': 'test12345',
                                                  'email': 'dummytest22@test.com',
                                                  'password': 'password',
                                                  'image': None,
                                                  'state': 'Texas',
                                                  'vax_date': None,
                                                  'covid_status': None},
                                                   follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("dummytest22@test.com", html)

    def test_invalid_user_signup(self):
        with self.client as client:
            resp = client.post('/register', data={'firstname': 'tester',
                                                  'lastname': 'person',
                                                  'username': 'test123',
                                                  'email': 'test@test.com',
                                                  'password': 'password',
                                                  'image': None,
                                                  'state': 'Texas',
                                                  'vax_date': None,
                                                  'covid_status': None},
                                                   follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sign Up", html)

            with self.assertRaises(InvalidRequestError):
                db.session.commit()
=======
    def test_homepage(self):
        """Does Logout link appear on user's homepage page?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = self.client.get('/user')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

<<<<<<< HEAD
            self.assertIn('Dallas', html)
>>>>>>> login/logout functionality"
=======
            self.assertIn('Logout', html)
>>>>>>> add login/logout functionality
