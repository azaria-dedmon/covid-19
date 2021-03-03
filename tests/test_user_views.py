"""User View tests."""
from unittest import TestCase
from models import db, User, Review
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

        self.testreview = Review(location='9191 S Polk Street Dallas', description='Just testing this out', user_id=self.testuser.id)
        self.rid = 2222
        self.testreview.id = self.rid
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


    def test_user_search(self):
        """Can user's search for other users?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f'/search-user?username={self.testuser.username}')
            html = resp.get_data(as_text=True)
            self.assertIn('test', html)

    def test_edit_profile(self):
        """Can user's edit their profile?"""
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
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = user.id
            resp = c.get('/user/edit')
            html = resp.get_data(as_text=True)
            self.assertIn('tester', html)

            resp = c.post('/user/edit', data={'firstname': 'testme',
                                                  'lastname': 'person',
                                                  'username': 'test12345',
                                                  'email': 'dummytest22@test.com',
                                                  'image': None,
                                                  'state': 'Texas',
                                                  'vax_date': None,
                                                  'covid_status': None},
                                                   follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('testme', html)

    def test_user_delete(self):
        """Can a user delete their account?"""
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
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = user.id

            resp = c.get('/user/delete')
            html = resp.get_data(as_text=True)
            self.assertIn('verify', html)

            resp = c.post('/user/delete', data={'password': 'password'},
                                                   follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Covid-19', html)

    def test_invalid_user_delete(self):
        """Can a user delete their account?"""
        user = User.signup(firstname='tester',
                           lastname='person',
                           username='test1234',
                           email='dummytest2@test.com',
                           password='password',
                           image= None,
                           state="Texas",
                           vax_date=None,
                           covid_status=None)
        uid = 22222
        user.id = uid

        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = user.id

            resp = c.get('/user/delete')
            html = resp.get_data(as_text=True)
            self.assertIn('verify', html)
    
            resp = c.post('/user/delete', data={'password': 'blahhhh'},
                                                        follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("verify", html)

    def test_add_review(self):
        """Can a user add a review for a testing location?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get('/add/location/review')
            html = resp.get_data(as_text=True)
            self.assertIn('love', html)

            resp = c.post('/add/location/review', data={'test-site': '9191 S Polk Street Dallas', 'description': 'Great!', 'user_id': self.testuser.id}, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Hello", html)


    def test_view_review(self):
        """Can a user view their reviews for a testing location?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.get('/user/reviews')
            html = resp.get_data(as_text=True)
            self.assertIn('Your Reviews', html)


    def test_search_review(self):
        """Can a user search reviews for a testing location?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get('/location/review?address=9191+S+Polk+Street+Dallas')
            html = resp.get_data(as_text=True)
            self.assertIn('Dallas', html)
    
    def test_edit_review(self):
        """Can a user edit their reviews?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            review = Review(location='9191 S Polk Street Dallas', description='Tester', user_id=self.testuser.id)
            review.id = 1
            db.session.add(review)
            db.session.commit()

            resp = c.get(f'/edit/review/{review.id}')
            html = resp.get_data(as_text=True)
            self.assertIn('Edit', html)

            resp = c.post(f'/edit/review/{review.id}', data={'description': 'Change!'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Hello", html)