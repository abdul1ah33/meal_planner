from flask import Flask
from models import init_db, db
from models.user import User
from models.recipe import Recipe
from models.meal_plan import MealPlan
from models.grocery_list import GroceryList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meal_planner.db'  # Update as needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

if __name__ == "__main__":
    app.run(debug=True)

