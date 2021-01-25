from flask import Flask
from models import db, connect_db

app = Flask(__name__)

connect_db(app)
