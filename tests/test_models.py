import unittest
from datetime import date
from app import create_app, db
from models.user import User
from models.recipe import Recipe
from models.meal_plan import MealPlan
from models.grocery_list import GroceryList
from models.saved_grocery_list import SavedGroceryList
from models.feedback import Feedback

class ModelTestCase(unittest.TestCase):
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

    def test_user_creation(self):
        user = User(email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(user.email, 'test@example.com')

    def test_recipe_relationship(self):
        user = User(email='test@example.com', password='password')
        recipe = Recipe(
            title='Test Recipe',
            ingredients='Ing1, Ing2',
            meal_type='breakfast',
            user=user
        )
        db.session.add_all([user, recipe])
        db.session.commit()
        self.assertEqual(user.recipes.count(), 1)
        self.assertEqual(recipe.author, user)

    def test_meal_plan_creation(self):
        user = User(email='test@example.com', password='password')
        meal_plan = MealPlan(
            week_start_date=date(2024, 1, 1),
            user=user,
            meals_data='{"0": {"breakfast": 1}}'
        )
        db.session.add_all([user, meal_plan])
        db.session.commit()
        self.assertEqual(user.meal_plans.count(), 1)
        self.assertIsInstance(meal_plan.get_meals(), dict)

    def test_grocery_list_relationships(self):
        user = User(email='test@example.com', password='password')
        meal_plan = MealPlan(week_start_date=date.today(), user=user)
        grocery_list = GroceryList(
            meal_plan=meal_plan,
            items='Item1, Item2'
        )
        db.session.add_all([user, meal_plan, grocery_list])
        db.session.commit()
        self.assertEqual(meal_plan.grocery_lists.count(), 1)

    def test_feedback_creation(self):
        user = User(email='test@example.com', password='password')
        feedback = Feedback(
            user=user,
            rating=5,
            content='Great app!'
        )
        db.session.add_all([user, feedback])
        db.session.commit()
        self.assertEqual(user.feedbacks.count(), 1)
        self.assertEqual(feedback.rating, 5)

if __name__ == '__main__':
    unittest.main()
