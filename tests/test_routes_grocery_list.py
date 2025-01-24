import unittest
from flask import url_for
from app import create_app, db
from models.user import User
from models.meal_plan import MealPlan
from models.grocery_list import GroceryList

class GroceryListRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
        # Create test data
        user = User(email='test@example.com', password='password')
        meal_plan = MealPlan(
            week_start_date='2024-01-01',
            user=user,
            meals_data='{"0": {"breakfast": 1}}'
        )
        grocery_list = GroceryList(
            meal_plan=meal_plan,
            items='Eggs, Milk'
        )
        db.session.add_all([user, meal_plan, grocery_list])
        db.session.commit()
        
        # Login user
        with self.client.session_transaction() as sess:
            sess['user_id'] = user.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_view_grocery_list(self):
        response = self.client.get(url_for('grocery_list.view', meal_plan_id=1))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Grocery List', response.data)

    def test_save_grocery_list(self):
        response = self.client.post(url_for('grocery_list.save_list'), data={
            'list_name': 'Test List',
            'ingredients[]': ['Eggs', 'Milk']
        }, follow_redirects=True)
        self.assertIn(b'List saved successfully', response.data)

    def test_view_saved_lists(self):
        response = self.client.get(url_for('grocery_list.view_saved_lists'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Saved Lists', response.data)

if __name__ == '__main__':
    unittest.main()
