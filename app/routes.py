# Imports
from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, db
from flask_login import current_user, login_user, logout_user
from app.models import Users, Lesson, Question
from app.forms import UserLoginForm, UserRegistrationForm, UserQuestionCheck

# Define the '/index' project route, contains the base html used across all other 
# project pages in order to allow testing
@app.route('/index')
def index():
    print(current_user.name)
    user = {'username': 'Dominic Toretto'}
    return render_template('Base.html', user=user)


# Define the '/test' project route, A page that is used for testing/ internal
# debugging purposes. Or as a page to temporarily store code if needed.
@app.route('/test')
def test():
    user = {'username': 'Dominic Toretto'}
    return render_template('TestBlock.html', user=user)

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
        userlogin = Users.query.filter_by(username=form.username.data.lower()).first()
        # Checks if userlogin's username mataches the password in the login submission
        if userlogin is None or not userlogin.check_password(form.password.data):
            # Tells user their login failed and keeps them on the login page
            flash('Either the username or the password is not valid')
            return redirect(url_for('login'))
        # If login information is correct, the user is logged into the project and returned
        # to the homepage
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        login_user(userlogin, remember=form.remember_me.data)
        return redirect(url_for('DataEntry'))
    return render_template('login.html', title='Sign In', form=form)

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
        # Checks if a name for the user was submitted (which defaults to username if the user didn't specify one) 
        if form.name.data == "":
            Name = form.username.data
        else:
            Name = form.name.data
        # Assigns the submitted value for username and name and assigns it to 'user'
        user = Users(username=form.username.data.lower(), name=Name)
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

# Updates user record to say that they have started the teaching lesson
# Will probaby be moved into the "Start" section when made
@app.route('/UpdateUserState')
def UpdateUserState():
    if current_user.is_authenticated:
        UserStartState = Users.query.filter_by(id=current_user.id).first()
        if UserStartState.started is False:
            UserStartState.started = True
            db.session.commit()
    return ("nothing")

# Resets User's started state for the purposes of testing
@app.route('/RestartUser')
def RestartUser():
    if current_user.is_authenticated:
        UserStartState = Users.query.filter_by(id=current_user.id).first()
        if UserStartState.started is True:
            UserStartState.started = False
            db.session.commit()
    return redirect(url_for('homepage'))

# Empties DB for purpose of testing
@app.route('/EmptyDb')
def EmptyDb():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            TableList = [Users, Lesson, Question]
            for table in TableList:
                contents = table.query.all()
                for u in contents:
                    db.session.delete(u)
                db.session.commit()
            return redirect(url_for('homepage'))
    return redirect(url_for('homepage'))

# Requires "admin, admin" login, prints the whole DB to the server terminal
@app.route('/AdminInfo')
def AdminInfo():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            UsersList = db.session.query(Users).all()
            for users in UsersList:
                print(users)
                print(users.id, users.name, users.started)
            LessonList = db.session.query(Lesson).all()
            for LL in LessonList:
                print(LL)
                print(LL.id, LL.Type, LL.Completed, LL.user_id)
            QuestionList = db.session.query(Question).all()
            for QL in QuestionList:
                print(QL)
                print(QL.id, QL.Answer, QL.Answered, QL.lesson_id)
    return redirect(url_for('homepage'))

# Creates the related database records for the questions, tests and lessons
@app.route('/DataEntry', methods=['GET', 'POST'])
def DataEntry():
    if current_user.is_authenticated:
        UserLesson = Lesson.query.filter_by(user_id=current_user.id).first()
        if UserLesson is None:
            # Topics of each lesson
            TopicList = ["Lesson1", "Lesson2", "Lesson3"]
            QuestionAnswers = [[],[],[]]
            # Three lessons
            for i in range(0,3):
                LessonList = Lesson(Completed=False, Type=TopicList[i], user_id=current_user.id)
                db.session.add(LessonList)
                db.session.commit()
                # Two questions per test
                for n in range(0,3):
                    QuestionList = Question(QuestionNumber=i,Answered=False, Answer="TBD", lesson_id=LessonList.id)
                    db.session.add(QuestionList)
                    db.session.commit()
            return redirect(url_for('homepage'))
    return redirect(url_for('homepage'))

# Records statisctics for the number of questions answered (Current records not answered for testing purposes)
@app.route('/Stats')
def UserStats():
    if current_user.is_authenticated:
        UserTestStats = [0,0,0]
        for u, l, q in db.session.query(Users, Lesson, Question).filter(Users.id==Lesson.user_id).filter(Lesson.id==Question.lesson_id).filter(Users.id==current_user.id).all():
            if q.QuestionNumber == "1":
                if q.Answered == False:
                    UserTestStats[0] += 1
            if q.QuestionNumber == "2":
                if q.Answered == False:
                    UserTestStats[1] += 1
            if q.QuestionNumber == "3":
                if q.Answered == False:
                    UserTestStats[2] += 1
    return render_template('Stats.html', L1Score = UserTestStats[0], L2Score = UserTestStats[1], L3Score = UserTestStats[2], Overall=sum(UserTestStats))

@app.route('/Lesson1', methods=['GET','POST'])
def Lesson1():
    form = UserQuestionCheck()
    # print(form)
    if form.validate_on_submit():
        # print(form.example.data)
        for u, l, q in db.session.query(Users, Lesson, Question).filter(Users.id==Lesson.user_id).filter(Lesson.id==Question.lesson_id).filter(Users.id==current_user.id).filter(Question.QuestionNumber==1).all():
            if form.Question1.data == q.Answer:
                q.Answered = True
                db.session.commit()
        return redirect(url_for('homepage'))
    # else:
    #     print(form.errors)
    return render_template("Lesson1.html", form=form)

@app.route('/Lesson2')
def Lesson2():
    form = UserQuestionCheck()
    # print(form)
    if form.validate_on_submit():
        # print(form.example.data)
        for u, l, q in db.session.query(Users, Lesson, Question).filter(Users.id==Lesson.user_id).filter(Lesson.id==Question.lesson_id).filter(Users.id==current_user.id).filter(Question.QuestionNumber==2).all():
            if form.Question1.data == q.Answer:
                q.Answered = True
                db.session.commit()
        return redirect(url_for('homepage'))
    # else:
    #     print(form.errors)
    return render_template("Lesson2.html", form=form)

@app.route('/Lesson3')
def Lesson3():
    form = UserQuestionCheck()
    # print(form)
    if form.validate_on_submit():
        # print(form.example.data)
        for u, l, q in db.session.query(Users, Lesson, Question).filter(Users.id==Lesson.user_id).filter(Lesson.id==Question.lesson_id).filter(Users.id==current_user.id).filter(Question.QuestionNumber==3).all():
            if form.Question1.data == q.Answer:
                q.Answered = True
                db.session.commit()
        return redirect(url_for('homepage'))
    # else:
    #     print(form.errors)
    return render_template("Lesson3.html", form=form)
