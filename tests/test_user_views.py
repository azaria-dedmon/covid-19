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

    def test_user_login(self):
        """Can users login sucessfully?"""
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
        with self.client as c:
            resp = c.post('/login', data={'username': 'test1234',
                                          'password': 'password'},follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("dummytest2@test.com", html)

    def test_invalid_login(self):
        """Does authentication fail with invalid credentials are provided?"""
        with self.client as c:
            resp = c.post('/login', data={'username': self.testuser.username,
                                          'password': self.testuser.password},follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Need to register?', html)

    def test_homepage(self):
        """Are we on the current user's homepage?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get('/user')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Hello, test', html)

    def test_user_logout(self):
        """Can users logout successfully?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                sess[CURR_USER_KEY] = None

            resp = c.get('/logout', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Covid Testing', html)

    def test_map_locations(self):
        """Does the map show testing locations?"""
        with self.client as c:
            resp = c.get('/location?state=California')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn('San Francisco', html)