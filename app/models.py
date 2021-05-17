# Imports
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Define User details to be stored
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), default=username)
    password_hash = db.Column(db.String(128))
    started = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Users {}>'.format(self.username)  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define Lesson details to be stored
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Completed = db.Column(db.Boolean, default=False)
    Type = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Lesson {}>'.format(self.Type)     

# Define Question details to be stored
# 1 Test can have many questions
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    QuestionNumber = db.Column(db.Integer)
    Answer = db.Column(db.String(128))
    Answered = db.Column(db.Boolean, default=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))

    def __repr__(self):
        return '<Question {}>'.format(self.Answer)   

# Records the info on the user currently logged in base on their user id
@login.user_loader
def LoginCurrentUser(id):
    return Users.query.get(int(id))
