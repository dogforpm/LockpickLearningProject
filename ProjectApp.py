# from flask import Flask, render_template, request, redirect, url_for

# app = Flask(__name__)
# app.config['SECRET_KEY'] = '1QaZsE4RfVgY7UjMkO0P'


# @app.route('/index')
# def index():
#     user = {'username': 'Dominic Toretto'}
#     return render_template('Base.html', user=user)

# @app.route('/test')
# def test():
#     user = {'username': 'Dominic Toretto'}
#     return render_template('TestBlock.html', user=user)

# @app.route('/')
# @app.route('//homepage')
# def homepage():
#     user = {'username': 'Dominic Toretto', 'started': 'No'}
#     return render_template('homepage.html', user=user)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = "Incorrect login"
#         else:
#             return redirect(url_for('homepage')) 
#     return render_template('login.html', error=error)

# if __name__=='__main__':
#     app.run(debug=True)

from app import app, db
from app.models import Users

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users}
