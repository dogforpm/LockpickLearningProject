from app import db

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Course {}>'.format(self.id)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), default=username)
    password_hash = db.Column(db.String(128))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return '<Users {}>'.format(self.username)    

class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(128))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return '<Lesson {}>'.format(self.Type)    

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(128))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))

    def __repr__(self):
        return '<Test {}>'.format(self.Type)  

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Answer = db.Column(db.String(128))
    Answered = db.Column(db.Boolean, default=False)
    Test_id = db.Column(db.Integer, db.ForeignKey('test.id'))

    def __repr__(self):
        return '<Question {}>'.format(self.Answer)   