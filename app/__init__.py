"""Application."""
import os
import requests
from flask import Flask, session, g, render_template, redirect, request, flash
from forms import RegisterUser, LoginUser
from models import connect_db, User, db, testing_states
from config import config
from sqlalchemy.exc import IntegrityError
from .location_details import get_testing_locations

CURR_USER_KEY = "curr_user"
API_BASE_URL = 'http://www.mapquestapi.com/geocoding/v1/address'
app = Flask(__name__)

def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    connect_db(app)
    return app

@app.before_request
def add_user_to_g():
    """If user has logged in, add current user to Flask global object."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Method logs in the user."""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Method logs out user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Handles user signup."""
    form = RegisterUser()

    if form.validate_on_submit():
        try:
            user = User.signup(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            image=form.image.data,
            state=form.state.data,
            vax_date=form.vax_date.data,
            covid_status=form.covid_status.data)
            db.session.commit()
            do_login(user)
            return redirect('/user')
        except IntegrityError:
            flash("Invalid information", 'danger')
            return render_template('users/register.html', form=form)
    else:
        return render_template('users/register.html', form=form)


@app.route('/user')
def show_user():
    """Shows homepage of user."""
    state = g.user.state
    url = f'https://covid-19-testing.github.io/locations/{state.lower()}/complete.json'
    res = requests.get(url)
    testing_data = res.json()
    return render_template('users/user_homepage.html', testing_data=testing_data)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handles user login."""
    form = LoginUser()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/user")
        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle user logout."""
    do_logout()
    flash("Success!", "success")
    return redirect("/")


@app.route('/')
def show_homepage():
    """Shows website homepage"""
    return render_template('homepage.html', testing_states=testing_states)


@app.route('/location')
def show_state_locations():
    """Return testing locations for state selected from drop down menu"""
    state = request.args.get('state')

    locations = get_testing_locations(state, API_BASE_URL)
    return render_template('location.html', locations=locations)


@app.route('/search-user')
def get_searched_user():
    """Search other users"""

    username = request.args.get('username')
    searched_user =  User.query.filter_by(username=username).first()

    return render_template('users/searched_user.html', searched_user=searched_user)
