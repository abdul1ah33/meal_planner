import unittest
from flask import url_for, get_flashed_messages
from app import create_app, db
from models.user import User

class AuthRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
        # Create test user
        user = User(email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_page(self):
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login to Meal Planner', response.data)

    def test_successful_login(self):
        response = self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Weekly Meal Plan', response.data)

    def test_invalid_login(self):
        response = self.client.post(url_for('auth.login'), data={
            'email': 'wrong@example.com',
            'password': 'wrong'
        }, follow_redirects=True)
        self.assertIn(b'Invalid email or password', response.data)

    def test_signup_page(self):
        response = self.client.get(url_for('auth.signup'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)

    def test_successful_signup(self):
        response = self.client.post(url_for('auth.signup'), data={
            'email': 'new@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(User.query.count(), 2)
        self.assertIn(b'Please log in', response.data)

    def test_logout(self):
        self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        })
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertIn(b'You have been logged out', response.data)

if __name__ == '__main__':
    unittest.main()
