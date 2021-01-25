from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired


class RegisterUser(FlaskForm):
    """Form for registering users"""
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    image = StringField('Image Url')
    state = SelectField('State', coerce=str, validators=[DataRequired()])
    vax_date = IntegerField('Vaccination Date')
    covid_status = StringField('Covid Status')