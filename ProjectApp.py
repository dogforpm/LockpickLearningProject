from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')

def home():
    return "Hello World"

@app.route('/homepage')

def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = "Incorrect login"
        else:
            return redirect(url_for('homepage')) 
    return render_template('login.html', error=error)

if __name__=='__main__':
    app.run(debug=True)
