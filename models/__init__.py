from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the Flask app.
    """
    db.init_app(app)

    # Automatically create tables if they don't exist
    with app.app_context():
        db.create_all()

# Import models here
from models.user import User
from models.recipe import Recipe
from models.meal_plan import MealPlan
from models.grocery_list import GroceryList
from models.feedback import Feedback

# Expose db and init_db for use in app.py
__all__ = ["db", "init_db", "User", "Recipe", "MealPlan", "GroceryList"]

