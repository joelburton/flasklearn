import unittest

from blogapp.extensions import admin, rest_api
from blogapp.models import db, User, Role
from blogapp import create_app


class TestURLs(unittest.TestCase):
    def setUp(self):
        # Bug workarounds
        admin._views = []
        rest_api.resources = []

        app = create_app('blogapp.config.TestConfig')
        self.client = app.test_client()

        # Bug workaround
        db.app = app

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add(self):
        self.assertTrue(True)

    def test_root_redirect(self):
        """ Tests if the root URL gives a 302 """

        result = self.client.get('/')
        self.assertEquals(result.status_code, 302)
        self.assertIn("/blog/", result.headers['Location'])

    def test_login(self):
        """ Tests if the login form works correctly """

        test_role = Role(name="default")
        db.session.add(test_role)
        db.session.commit()

        test_user = User(username="test")
        test_user.set_password("test")
        db.session.add(test_user)
        db.session.commit()

        result = self.client.post('/login', data=dict(
            username='test',
            password="test"
        ), follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('You have been logged in', result.data)

if __name__ == '__main__':
    unittest.main()
