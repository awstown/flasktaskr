# test.py


import os
import unittest

from views import app, db
from models import User
from config import basedir

TEST_DB = 'test.db'


class Users(unittest.TestCase):

    ### SETUP/TEARDOWN

    # this is a special method that is executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # this is a special method that is executed after each test
    def tearDown(self):
        db.drop_all()
    
    ### HELPER METHODS
    
    def login(self, name, password):
        return self.app.post('', data=dict(
            name=name, password=password), follow_redirects=True)


    ### TESTS
    # each test should start with 'test'
    
    def test_users_can_register(self):
        new_user = User("mherman", "michael@mherman.org", "michaelherman")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
            assert t.name == "mherman"

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Please sign in to access your task list.', response.data)

    def login(self, name, password):
        return self.app.post('', data=dict(
            name=name, password=password), follow_redirects=True)

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn('Invalid username or password.', response.data)

if __name__ == '__main__':
    unittest.main()