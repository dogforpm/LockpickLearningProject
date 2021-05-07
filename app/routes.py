# Imports
from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, db
from flask_login import current_user, login_user, logout_user
from app.models import Users
from app.forms import UserLoginForm, UserRegistrationForm

# Define the '/index' project route, contains the base html used across all other 
# project pages in order to allow testing
@app.route('/index')
def index():
    user = {'username': 'Dominic Toretto'}
    return render_template('Base.html', user=user)


# Define the '/test' project route, A page that is used for testing/ internal
# debugging purposes. Or as a page to temporarily store code if needed.
@app.route('/test')
def test():
    flash('You were successfully logged in')
    return redirect(url_for('index'))
    user = {'username': 'Dominic Toretto'}
    return render_template('index.html', user=user)

# Define the default route as well as the '/homepage' route, the opening page of the 
# project as well as the homepage
@app.route('/')
@app.route('/homepage')
def homepage():
    #user = {'username': 'Dominic Toretto', 'started': 'No'}
    return render_template('homepage.html')

# Define the '/login' route, Allow a user to login to the project using their login details
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Define default error value
    error = None
    # Check if the user is already logged into the project, returning them to the homepage
    # if they already are logged in
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    # Define form to use User Login forms created in forms.py
    form = UserLoginForm()
    # If the user submits their login detail as being valid, the requirements defined in
    # the forms.py
    if form.validate_on_submit():
        # Extracts the userlogin information from the database based on the username
        # submitted, there should be either one value or no value returned as 
        # usernames are unique (thus only one result) or not in the db (thus None)
        userlogin = Users.query.filter_by(username=form.username.data).first()
        # Checks if userlogin's username mataches the password in the login submission
        if userlogin is None or not userlogin.check_password(form.password.data):
            # Tells user their login failed and keeps them on the login page
            flash('Either the username or the password is not valid')
            return redirect(url_for('login'))
        # If login information is correct, the user is logged into the project and returned
        # to the homepage
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        login_user(userlogin, remember=form.remember_me.data)
        return redirect(url_for('homepage'))
    return render_template('login.html', title='Sign In', form=form)
    # if form.validate_on_submit():
    #     if request.method == 'POST':
    #         if request.form['username'] == 'admin' or request.form['password'] == 'admin':
    #             flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
    #             return redirect(url_for('homepage'))
    #         else:
    #             error = "Incorrect login"
    # return render_template('login.html', error=error, form=form)

# Define the '/register' project route, allows user to register their account 
# into the project database
@app.route('/register', methods=['GET','POST'])
def register():
    # Check if the user is already logged into the project, returning them to the homepage
    # if they already are logged in
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    # Define form to use User Registration forms created in forms.py
    form = UserRegistrationForm()
    # If the user submits their login detail as being valid, the requirements defined in
    # the forms.py
    if form.validate_on_submit():
        # Assigns the submitted value for username and name (which defaults to username
        # if the user didn't specify one) and assigns it to 'user'
        user = Users(username=form.username.data, name=form.name.data)
        # Hashes the password the user submitted
        user.set_password(form.password.data)
        # Adds and commits the user's registration to the db
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Defines the '/logout' route, logs the user out of the project and returns them 
# to the homepage
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))