"""User View tests."""

from unittest import TestCase
from models import db, User
from app import app, CURR_USER_KEY
from sqlalchemy.exc import InvalidRequestError

class UserViewTestCase(TestCase):
    """Test views for users."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///covidtest'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    db.drop_all()
    db.create_all()

    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()

        self.client = app.test_client()

        app.config['SECRET_KEY'] = 'secrets'

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

        with app.test_client() as client:
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
        with app.test_client() as client:
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
