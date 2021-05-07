# Imports
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Many to Many relationship resolution table
# As 1 User can have many lesson, but 1 Lesson can have many users
class UserCourse(db.Model):
    __tablename__ = 'UserCourse'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))

    def __repr__(self):
        return '<UserCourse {}>'.format(self.id)

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

    # def update_started(self, )

# Define Lesson details to be stored
class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(128))

    def __repr__(self):
        return '<Lesson {}>'.format(self.Type)    

# Define Test details to be stored
# 1 Lesson can have many Tests
class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(128))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))

    def __repr__(self):
        return '<Test {}>'.format(self.Type)  

# Define Question details to be stored
# 1 Test can have many questions
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Answer = db.Column(db.String(128))
    Answered = db.Column(db.Boolean, default=False)
    Test_id = db.Column(db.Integer, db.ForeignKey('test.id'))

    def __repr__(self):
        return '<Question {}>'.format(self.Answer)   

# Records the info on the user currently logged in base on their user id
@login.user_loader
def LoginCurrentUser(id):
    return Users.query.get(int(id))