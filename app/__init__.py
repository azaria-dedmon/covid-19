"""Application."""

from flask import Flask, session, g, render_template, redirect, flash
from forms import LoginUser
from models import connect_db, User
from config import config


CURR_USER_KEY = "curr_user"

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
    """Method logsout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handles user login."""
    form = LoginUser()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

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



@app.route('/user')
def show_user():
    """Shows homepage of user."""
    return render_template('users/user_homepage.html')
