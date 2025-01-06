from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from models import db
from models.recipe import Recipe
from models.meal_plan import MealPlan
from models.saved_grocery_list import SavedGroceryList
from datetime import datetime

grocery_list_bp = Blueprint('grocery_list', __name__, url_prefix='/grocery-list')

@grocery_list_bp.route('/<int:meal_plan_id>')
def view(meal_plan_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    day_filter = request.args.get('day_filter', 'all')
    
    meal_plan = MealPlan.query.get_or_404(meal_plan_id)
    meals_data = meal_plan.get_meals()
    
    # Collect recipe IDs based on filter
    recipe_ids = set()
    if day_filter == 'all':
        for day_meals in meals_data.values():
            recipe_ids.update(day_meals.values())
    else:
        day_meals = meals_data.get(day_filter, {})
        recipe_ids.update(day_meals.values())
    
    # Query recipes and collect ingredients
    recipes = Recipe.query.filter(Recipe.id.in_(recipe_ids)).all()
    all_ingredients = []
    for recipe in recipes:
        all_ingredients.extend(recipe.ingredients_list)
    
    # Remove duplicates and sort
    unique_ingredients = sorted(set(all_ingredients))
    
    # Get user's saved grocery lists
    saved_lists = SavedGroceryList.query.filter_by(user_id=session['user_id']).all()
    
    return render_template('grocery_list.html', 
                         ingredients=unique_ingredients,
                         day_filter=day_filter,
                         meal_plan_id=meal_plan_id,
                         saved_lists=saved_lists)

@grocery_list_bp.route('/add-ingredient', methods=['POST'])
def add_ingredient():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    ingredient = request.form.get('ingredient')
    if not ingredient:
        return jsonify({"error": "No ingredient provided"}), 400
    
    return jsonify({"ingredient": ingredient.strip()})

@grocery_list_bp.route('/save-list', methods=['POST'])
def save_list():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    ingredients = request.form.getlist('ingredients[]')
    list_name = request.form.get('list_name', f"Shopping List {datetime.now().strftime('%Y-%m-%d')}")
    
    saved_list = SavedGroceryList(
        user_id=session['user_id'],
        name=list_name,
        ingredients=''  # Will be set below
    )
    saved_list.set_ingredients(ingredients)
    
    db.session.add(saved_list)
    db.session.commit()
    
    return jsonify({"success": True, "id": saved_list.id})

@grocery_list_bp.route('/delete-list/<int:list_id>', methods=['POST'])
def delete_list(list_id):
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    saved_list = SavedGroceryList.query.get_or_404(list_id)
    if saved_list.user_id != session['user_id']:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(saved_list)
    db.session.commit()
    
    return jsonify({"success": True})

@grocery_list_bp.route('/saved-lists')
def view_saved_lists():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    saved_lists = SavedGroceryList.query.filter_by(user_id=session['user_id']).order_by(SavedGroceryList.created_at.desc()).all()
    return render_template('saved_lists.html', saved_lists=saved_lists)
