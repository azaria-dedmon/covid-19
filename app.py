from flask import Flask, session, g, render_template, redirect, request
from forms import RegisterUser
from models import db, connect_db, User, testing_states


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


@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Handles user signup"""
    states = [state for state in testing_states]
    form = RegisterUser(request.form)
    form.state.choices = states

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
        if user:
            """Automatically logins in user"""
            do_login(user)
            return redirect('/user')
    return render_template('users/register.html', form=form)
