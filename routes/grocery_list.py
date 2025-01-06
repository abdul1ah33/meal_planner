from flask import Blueprint, render_template, request
from models import db
from models.recipe import Recipe
from models.meal_plan import MealPlan

grocery_list_bp = Blueprint('grocery_list', __name__, url_prefix='/grocery-list')

@grocery_list_bp.route('/<int:meal_plan_id>')
def view(meal_plan_id):
    day_filter = request.args.get('day_filter', 'all')
    
    meal_plan = MealPlan.query.get_or_404(meal_plan_id)
    meals_data = meal_plan.get_meals()
    
    # Collect recipe IDs based on filter
    recipe_ids = set()
    if day_filter == 'all':
        # Get all recipe IDs from all days
        for day_meals in meals_data.values():
            recipe_ids.update(day_meals.values())
    else:
        # Get recipe IDs for specific day
        day_meals = meals_data.get(day_filter, {})
        recipe_ids.update(day_meals.values())
    
    # Query recipes and collect ingredients
    recipes = Recipe.query.filter(Recipe.id.in_(recipe_ids)).all()
    all_ingredients = []
    for recipe in recipes:
        all_ingredients.extend(recipe.ingredients_list)
    
    # Remove duplicates and sort
    unique_ingredients = sorted(set(all_ingredients))
    
    return render_template('grocery_list.html', 
                         ingredients=unique_ingredients,
                         day_filter=day_filter)
