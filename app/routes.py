from flask import Flask, render_template, request, redirect, url_for, flash
from app import app
from app.forms import UserLoginForm

@app.route('/index')
def index():
    user = {'username': 'Dominic Toretto'}
    return render_template('Base.html', user=user)

@app.route('/register')
def register():
    user = {'username': 'Dominic Toretto'}
    return render_template('register.html', user=user)

@app.route('/test')
def test():
    flash('You were successfully logged in')
    return redirect(url_for('index'))
    user = {'username': 'Dominic Toretto'}
    return render_template('index.html', user=user)

@app.route('/')
@app.route('/homepage')
def homepage():
    user = {'username': 'Dominic Toretto', 'started': 'No'}
    return render_template('homepage.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = UserLoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            if request.form['username'] == 'admin' or request.form['password'] == 'admin':
                flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
                return redirect(url_for('homepage'))
            else:
                error = "Incorrect login"
    return render_template('login.html', error=error, form=form)