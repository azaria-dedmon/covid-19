"""Tests for Review Model"""


# run these tests like:
#
#    python -m unittest test_reviews_model.py


from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Review

from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///covid-test'


db.create_all()

class ReviewModelTest(TestCase):
    def setUp(self):
        """Create a test client, add sample data."""
        
        db.drop_all()
        db.create_all()

        u1 = User.signup("test", "case", "test123", "test123@test.com", "test123",
                        None, "California", None, None)
        u1id = 1111
        u1.id = u1id

        r1 = Review(location="Test location", description="I am testing review functionality")
        r1id = 2222
        r1.id = r1id
        r1.user_id = u1.id

        db.session.commit()

        u1 = User.query.get(u1id)
        r1 = Review.query.get(r1id)

        self.u1 = u1
        self.u1id = u1id
        self.r1 = r1
        self.r1id = r1id

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_review_creation(self):
        r2 = Review(location="Test location #2", description="I am testing review functionality #2",
                    user_id=self.u1id)
        r2id = 3333
        r2.id = r2id

        db.session.add(r2)
        db.session.commit()
        
        review_test = Review.query.get(r2.id)
        self.assertEqual(review_test.location, "Test location #2")
