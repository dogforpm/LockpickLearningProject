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
        db.create_all()

    def tearDown(self):
        
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):

        u = Users(username = "JohnSmith")

        u.set_password('JohnSmith123')

        self.assertFalse(u.check_password('JohnSmith987'))
        self.assertTrue(u.check_password('JohnSmith123'))

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_users(self):
        u = Users(username = "JohnSmith", name="Johnny")

        u.set_password('JohnSmith123')
        db.session.add(u)
        db.session.commit()
        
        rv = self.login('JohnSmith','JohnSmith123')
        print(rv.data)
        rv = self.app.get('/',follow_redirects=True)
        print(rv.data)
    
    def test_correct_login(self):
        tester = app.test_client(self)
        u = Users(username = "JohnSmith")
        u.set_password('JohnSmith123')
        response = tester.post(
        '/login',
        data = dict(username=u.username, password=u.password_hash),
        follow_redirects=True
        )
        self.assertIn(bytes(('Brings').encode("utf-8")), response.data)

if __name__=='__main__':
    unittest.main(verbosity = 2)



