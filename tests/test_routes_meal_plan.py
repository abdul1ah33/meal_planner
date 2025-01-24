import unittest
from flask import url_for
from app import create_app, db
from models.user import User
from models.recipe import Recipe

class MealPlanRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
        # Create test data
        user = User(email='test@example.com', password='password')
        recipe = Recipe(
            title='Test Recipe',
            ingredients='Eggs, Milk',
            meal_type='breakfast',
            user=user
        )
        db.session.add_all([user, recipe])
        db.session.commit()
        
        # Login user
        with self.client.session_transaction() as sess:
            sess['user_id'] = user.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_meal_plan_page(self):
        response = self.client.get(url_for('meal_plan.plan'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Weekly Meal Plan', response.data)

    def test_add_recipe_page(self):
        response = self.client.get(url_for('meal_plan.add_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add New Recipe', response.data)

    def test_add_recipe_submission(self):
        response = self.client.post(url_for('meal_plan.add_recipe'), data={
            'title': 'New Recipe',
            'meal_type': 'lunch',
            'ingredients': 'Tomatoes, Cheese',
            'description': 'Test description'
        }, follow_redirects=True)
        self.assertEqual(Recipe.query.count(), 2)
        self.assertIn(b'Recipe added successfully', response.data)

if __name__ == '__main__':
    unittest.main()
