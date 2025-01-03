from app import app
from models import db
from models.recipe import Recipe

# Function to populate the database
def populate_recipes():
    # Sample meals and ingredients
    recipes = [
    {"title": "Chicken Stir-Fry", "description": "Spicy chicken stir-fry with vegetables", "ingredients": "Chicken,Vegetables (Onions, Peppers, Broccoli), Soy Sauce, Ginger, Garlic"},
    {"title": "Sushi", "description": "Delicious and healthy sushi", "ingredients": "Sushi Rice, Nori Sheets, Salmon, Avocado, Cucumber"},
    {"title": "Tacos", "description": "Mexican-style tacos with various fillings", "ingredients": "Tortillas, Ground Beef, Lettuce, Tomato, Onion, Cheese, Salsa"},
    {"title": "Lasagna", "description": "Layered pasta dish with meat sauce and cheese", "ingredients": "Lasagna Sheets, Ground Beef, Tomato Sauce, Ricotta Cheese, Mozzarella Cheese"},
    {"title": "Mac and Cheese", "description": "Classic comfort food", "ingredients": "Macaroni, Cheese, Milk, Butter"},
    {"title": "Pancakes", "description": "Fluffy pancakes for breakfast", "ingredients": "Flour, Eggs, Milk, Baking Powder"},
    {"title": "French Toast", "description": "Sweetened bread dipped in egg batter", "ingredients": "Bread, Eggs, Milk, Cinnamon, Sugar"},
    {"title": "Scrambled Eggs", "description": "Simple and quick breakfast", "ingredients": "Eggs, Milk, Cheese (Optional), Vegetables (Optional)"},
    {"title": "Oatmeal", "description": "Healthy and filling breakfast", "ingredients": "Rolled Oats, Milk, Water, Toppings (Fruits, Nuts, Seeds)"},
    {"title": "Smoothie", "description": "Refreshing and nutritious drink", "ingredients": "Fruits (Berries, Banana, Mango), Yogurt, Milk, Spinach (Optional)"}
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

