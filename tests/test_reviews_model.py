"""Review model tests."""

from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Review

from app import app


class ReviewModelTestCase(TestCase):
    """Test case for Review Model"""
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

        r1 = Review(location='Testing Location', description='Just testing this out')
        r1.user_id = u1.id
        rid1 = 2222
        r1.id = rid1

        db.session.commit()

        u1 = User.query.get(uid1)
        r1 = Review.query.get(rid1)

        self.u1 = u1
        self.uid1 = uid1

        self.r1 = r1
        self.rid1 = rid1

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_review_model(self):
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
        u.id = 5555

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.review), 0)

        r = Review(location='Test', description="This is a test", user_id=u.id)
        db.session.add(r)
        db.session.commit()

        self.assertEqual(len(u.review), 1)
