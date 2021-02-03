from flask import Flask, session, g, render_template, redirect, flash
import requests
from forms import RegisterUser, LoginUser
from models import connect_db, User, db


CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SECRET_KEY'] = "application20212021"

connect_db(app)


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


@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Handles user signup."""
    form = RegisterUser()

    if form.validate_on_submit():
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
        if user:
            do_login(user)
            return redirect('/user')
        flash("Username already taken", 'danger')
        return render_template('users/register.html', form=form)

    return render_template('users/register.html', form=form)


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
    state = g.user.state
    url = f'https://covid-19-testing.github.io/locations/{state.lower()}/complete.json'
    res = requests.get(url)
    testing_data = res.json()

    return render_template('users/user_homepage.html', testing_data=testing_data)
