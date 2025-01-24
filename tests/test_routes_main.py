import unittest
from flask import url_for
from app import create_app, db

class MainRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Plan Your Meals', response.data)

    def test_protected_routes_redirect(self):
        routes = [
            url_for('meal_plan.plan'),
            url_for('feedback.index'),
            url_for('grocery_list.view_saved_lists')
        ]
        
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 302)
            self.assertIn(url_for('auth.login'), response.location)

if __name__ == '__main__':
    unittest.main()
