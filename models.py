"""SQLAlchemy models for Covid App"""

from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy 

bcrypt = Bcrypt()  
db = SQLAlchemy()  
 
def connect_db(app):    
    db.app = app    
    db.init_app(app)
    db.create_all()
        
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

    @classmethod
    def signup(cls, firstname, lastname, username,
            email, password, image, state, vax_date, covid_status):
        """Sign up user. Hashes password and adds user to system."""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            firstname=firstname,
            lastname=lastname,
            username=username,
            email=email,
            password=hashed_pwd,
            image=image,
            state=state,
            vax_date=vax_date,
            covid_status=covid_status)

        db.session.add(user)
        return user


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


testing_states = [('Arizona', 'Arizona'), ('California', 'California'),
                 ('Delaware', 'Delaware'), ('Florida', 'Florida'),
                 ('Massachusetts', 'Massachusetts'), ('Nevada', 'Nevada'),
                 ('New Jersey', 'New Jersey'), ('New York', 'New York'),
                 ('Pennsylvania', 'Pennsylvania'), ('Texas', 'Texas'),
                 ('Utah', 'Utah'), ('Washington', 'Washington')]
