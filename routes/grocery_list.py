from flask import Blueprint, render_template, request
from models import db
from models.recipe import Recipe

# Define the blueprint with a URL prefix
grocery_list_bp = Blueprint('grocery_list', __name__, url_prefix='/grocery-list')

@grocery_list_bp.route('/<meal_ids>')
def view(meal_ids):
    """
    View function to display a grocery list based on selected meal IDs.
    :param meal_ids: Comma-separated string of meal IDs.
    """
    # Convert comma-separated meal IDs into a list of integers
    meal_ids = [int(id) for id in meal_ids.split(',') if id.isdigit()]
    
    # Query the database for the selected recipes
    recipes = Recipe.query.filter(Recipe.id.in_(meal_ids)).all()

    # Collect all ingredients from the recipes
    ingredients = []
    for recipe in recipes:
        if hasattr(recipe, 'ingredients') and recipe.ingredients:
            ingredients.extend(recipe.ingredients.split(','))  # Split ingredients by comma

    # Remove duplicate ingredients and sort them for better readability
    unique_ingredients = sorted(set(ingredients))
    
    # Render the grocery list template with the unique ingredients
    return render_template('grocery_list.html', ingredients=unique_ingredients)

