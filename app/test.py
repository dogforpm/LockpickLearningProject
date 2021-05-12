import unittest
from app, import app, db
from app.models import Users, Course

class UserModelCase(unittest.TestCase):

    def setUp(self):
        
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):

        u = Users(username = "JohnSmith")

        u.set.password('hunter2')

        self.assertFalse(u.check_password('hunter3'))
        self.assertTrue(u.check_password('hunter2'))

    def test_follow(self):

        u1 = Users(username = "JohnSmith", name = "John", password = "1234")
        u2 = Users(username = "MichealScott", name = "Mike", password = "123456")

        db.session.add(u1)
        db.session.add(u2)

        db.session.commit()

        self.assertEqual(u1.remember_me(), False)
        self.assertEqual(u2.remember_me(), False)

        u1.remember_me(True)

        db.session.commit()

        self.assertTrue(u1.check_remember_me(True))


if __name__=='__main__':
    unittest.main(verbosity = 2)

    # run with 'python test.py'

TableList = [UserCourse, Users, Lesson, Test, Question]
for table in TableList:
    contents = table.query.all()
    for u in contents:
        db.session.delete(u)
    db.session.commit()

