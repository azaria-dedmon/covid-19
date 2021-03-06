from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from models import testing_states

class RegisterUser(FlaskForm):
    """Form for registering users"""
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    image = StringField('Image Url')
    state = SelectField('State', choices=testing_states, validators=[DataRequired()])
    vax_date = StringField('Vaccination Date')
    covid_status = StringField('Covid Status')

class LoginUser(FlaskForm):
    """Form for user login"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class EditUser(FlaskForm):
    """Form for editing user profile"""
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    username = StringField('Username')
    email = StringField('Email')
    image = StringField('Image Url')
    state = SelectField('State', choices=testing_states)
    vax_date = StringField('Vaccination Date')
    covid_status = StringField('Covid Status')

class DeleteUser(FlaskForm):
    """Form for checking user's password before account deletion"""
    password = PasswordField('Password')

class EditReview(FlaskForm):
    """Form for editing user reviews"""
    description = TextAreaField('Description')