"""SQLAlchemy models for Covid App"""

from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy 

bcrypt = Bcrypt()  
db = SQLAlchemy()  
 
 
def connect_db(app):    
        db.app = app    
        db.init_app(app)
        
class User (db.Model):
    """User in the system"""
    __tablename__ = "users" 

    id = db.Column( 
        db.Integer, 
        primary_key=True    
    )   
    firstname = db.Column(  
        db.Text,    
        nullable=False  
    )   
    lastname = db.Column(   
        db.Text,    
        nullable=False  
    )   
    username = db.Column(   
        db.Text,    
        nullable=False, 
        unique=True 
    )   
    email = db.Column(  
        db.Text,    
        nullable=False, 
        unique=True 
    )   
    password = db.Column(   
        db.Text,    
        nullable=False  
    )   
    image = db.Column(  
        db.Text 
    )   
    state = db.Column(  
        db.Text,    
        nullable=False  
    )   
    vax_date = db.Column(   
        db.Text,
        nullable=True  
    )   
    covid_status = db.Column(   
        db.Text,
        nullable=True
    )
    review = db.relationship('Review', backref='users')


class Review (db.Model):   
    """Reviews made by users for testing locations"""
    __tablename__ = "reviews" 

    id = db.Column( 
        db.Integer, 
        primary_key=True    
    )   
    location = db.Column(   
        db.Text,    
        nullable=False  
    )   
    description = db.Column(
        db.Text,
        nullable=False
    )   
    user_id = db.Column(    
        db.Integer, 
        db.ForeignKey('users.id', ondelete='CASCADE'),  
        nullable=False  
    )   
    user = db.relationship('User', backref="reviews", passive_deletes=True)

