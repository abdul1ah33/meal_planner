from app import app
from models import db
from models.recipe import Recipe

# Function to populate the database
def populate_recipes():
    # Sample meals and ingredients
    recipes = [
        {"title": "Pizza", "description": "Cheese and tomato pizza", "ingredients": "Cheese,Tomato,Flour,Yeast"},
        {"title": "Burger", "description": "Classic beef burger", "ingredients": "Beef Patty,Burger Bun,Lettuce,Tomato,Cheese"},
        {"title": "Pasta", "description": "Creamy Alfredo pasta", "ingredients": "Pasta,Heavy Cream,Garlic,Parmesan Cheese,Butter"},
        {"title": "Salad", "description": "Fresh vegetable salad", "ingredients": "Lettuce,Tomato,Cucumber,Olives,Feta Cheese"},
    ]

    with app.app_context():
        for recipe_data in recipes:
            recipe = Recipe(
                title=recipe_data["title"],
                description=recipe_data["description"],
                ingredients=recipe_data["ingredients"],
                user_id=1  # Assuming user_id 1 exists; adjust as needed
            )
            db.session.add(recipe)

        db.session.commit()
        print("Recipes added successfully!")

# Run the function
if __name__ == "__main__":
    populate_recipes()

