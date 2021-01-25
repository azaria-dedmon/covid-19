import os

from flask import Flask, render_template, request, session, redirect, flash, g
from flask_sqlalchemy import SQLAlchemy
from models import connect_db, db, User, Review, testing_states
from forms import LoginUser, RegisterUser, Reviews
import requests

CURR_USER_KEY = "curr_user"
API_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"

key = os.environ.get('key')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///covid'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = "secretkey"

connect_db(app)
db.create_all()



