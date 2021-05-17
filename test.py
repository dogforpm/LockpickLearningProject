import unittest
import pytest
from app import app, db
from app.models import Users, Lesson, Test, Question
from app.forms import UserLoginForm, UserRegistrationForm
from flask import current_app



class UserModelCase(unittest.TestCase):

    def setUp(self):
        
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

        self.app = app
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.create_all()

    def tearDown(self):
        
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):

        u = Users(username = "JohnSmith")

        u.set_password('JohnSmith123')

        self.assertFalse(u.check_password('JohnSmith987'))
        self.assertTrue(u.check_password('JohnSmith123'))

    # def test_unique_username(self):

    #     u1 = Users(username = "JohnSmith", name="Johnny")

    #     u1.set_password('JohnSmith123')
    #     db.session.add(u1)
    #     db.session.commit()

    #     u2 = Users(username = "JohnSmith", name="John")

    #     u2.set_password('JohnSmith987')

    #     self.assertFalse(u2.validate_username(u1.username))
    #     self.assertTrue(u2.validate_username(u1.username))

    def test_that_something_works(self):
        with self.client:
            tester = app.test_client(self)
            response = tester.post(
            '/login',
            data = dict(username="Michael", password="MadMike"),
            follow_redirects=True
            )
            print(response.data)
            #response = self.client.post('/login', { username: 'James', password: '007' })

            # success
            self.assertEquals(current_user.username, 'James')

    def test_data_generation(self):

        u1 = Users(username = "JohnSmith", name="Johnny")

        u1.set_password('JohnSmith123')
        db.session.add(u1)
        db.session.commit()

        tester = app.test_client(self)
        response = tester.post(
        '/DataEntry',
        data = dict(current_user=u1.id),
        follow_redirects=True
        )
        print(Lesson.query.filter_by(user_id=current_user.id).first() is None)
        self.assertFalse(Lesson.query.all() is None)

        #self.assertFalse(u2.validate_username(u1.username))
        #self.assertTrue(u2.validate_username(u1.username))

    # def login(self, username, password):
    #     return self.app.post('/login', data=dict(
    #         username=username,
    #         password=password
    #     ), follow_redirects=True)

    # def test_users(self):
    #     u = Users(username = "JohnSmith", name="Johnny")

    #     u.set_password('JohnSmith123')
    #     db.session.add(u)
    #     db.session.commit()
        
    #     rv = self.login('JohnSmith','JohnSmith123')
    #     print(rv.data)
    #     rv = self.app.get('/',follow_redirects=True)
    #     print(rv.data)
    # def test_Question_Update(self):

    #     u1 = Users(username = "JohnSmith", name = "John")
    #     l = Lesson(type="Forceful", completed=False, userid=u1.id)
    #     t1 = Test(completed=False, LessonNum="L1", lessonid=l.id)
    #     t2 = Test(completed=False, LessonNum="L1", lessonid=l.id)
    #     q1 = Question(Answered=False, Answer="A", test_id=t1.id)
    #     q2 = Question(Answered=False, Answer="B", test_id=t1.id)
    #     q3 = Question(Answered=False, Answer="C", test_id=t2.id)
    #     q4 = Question(Answered=False, Answer="D", test_id=t2.id)

    #     u1.set_password('JohnSmith123')

    #     db.session.add(u1)
    #     db.session.add(l)
    #     db.session.add(t1)
    #     db.session.add(t2)
    #     db.session.add(q1)
    #     db.session.add(q2)
    #     db.session.add(q3)
    #     db.session.add(q4)

    #     db.session.commit()

    #     self.assertEqual(u1.remember_me(), False)
    #     self.assertEqual(u2.remember_me(), False)

    #     u1.remember_me(True)

    #     db.session.commit()

    #     self.assertTrue(u1.check_remember_me(True))

    # def test_register(self):
    #     tester = app.test_client(self)
    #     response = tester.post(
    #     '/register',
    #     data = dict(username="Michael", name="Mike", password="MadMike", password2="MadMike", form=""),
    #     follow_redirects=True
    #     )
    #     self.assertIn(bytes(('Brings').encode("utf-8")), response.data)


        # tester = app.test_client(self)
        # response = self.app.post('/register', data = dict(username="Michael", name="Mike", password="MadMike", password2="MadMike", form=""), follow_redirects=True)
        # # '/register',
        # # data = dict(username="Michael", name="Mike", password="MadMike", password2="MadMike", form=""),
        # # follow_redirects=True
        # # )
        # self.assertIn(bytes(('Brings').encode("utf-8")), response.data)

    # def test_correct_login(self):
    #     tester = app.test_client(self)
    #     u = Users(username = "JohnSmith")
    #     u.set_password('JohnSmith123')
    #     response = tester.post(
    #     '/login',
    #     data = dict(username=u.username, password_hash=u.password_hash),
    #     follow_redirects=True
    #     )
    #     self.assertIn(bytes(('Brings').encode("utf-8")), response.data)

    # def test_user_login_form(self):

    #         form = UserRegistrationForm()
    #         form.username.data = "john"
    #         print(form.username.data)
    #         u = Users(username = "JohnSmith")

    #         u.set_password('JohnSmith123')

    #         self.assertFalse(u.check_password('JohnSmith987'))
    #         self.assertTrue(u.check_password('JohnSmith123'))

if __name__=='__main__':
    unittest.main(verbosity = 2)

    # run with 'python test.py'

TableList = [UserCourse, Users, Lesson, Test, Question]
for table in TableList:
    contents = table.query.all()
    for u in contents:
        db.session.delete(u)
    db.session.commit()