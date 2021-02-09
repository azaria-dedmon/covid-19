"""Application."""

from flask import Flask
from models import connect_db
from config import config


app = Flask(__name__)

CURR_USER_KEY = "curr_user"

def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    connect_db(app)
    return app