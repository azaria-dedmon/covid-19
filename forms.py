from flask_wtf import FlaskForm
<<<<<<< HEAD
<<<<<<< HEAD
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired
from models import testing_states
=======
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired

>>>>>>> covid project database structure
=======
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired
from models import testing_states
>>>>>>> login/logout functionality"

class RegisterUser(FlaskForm):
    """Form for registering users"""
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    image = StringField('Image Url')
<<<<<<< HEAD
<<<<<<< HEAD
    state = SelectField('State', choices=testing_states, validators=[DataRequired()])
    vax_date = StringField('Vaccination Date')
    covid_status = StringField('Covid Status')
=======
    state = SelectField('State', coerce=str, validators=[DataRequired()])
    vax_date = IntegerField('Vaccination Date')
    covid_status = StringField('Covid Status')
>>>>>>> covid project database structure
=======
    state = SelectField('State', choices=testing_states, validators=[DataRequired()])
    vax_date = StringField('Vaccination Date')
    covid_status = StringField('Covid Status')

class LoginUser(FlaskForm):
    """Form for user login"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
>>>>>>> login/logout functionality"
