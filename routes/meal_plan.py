from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.recipe import Recipe
from models.meal_plan import MealPlan

meal_plan_bp = Blueprint('meal_plan', __name__, url_prefix='/meal-plan')

@meal_plan_bp.route('/', methods=['GET', 'POST'])
def plan():
    if request.method == 'POST':
        selected_meals = request.form.getlist('meals')
        if not selected_meals:
            flash('Please select at least one meal.', 'warning')
            return redirect(url_for('meal_plan.plan'))
        
        meal_ids = ','.join(selected_meals)
        return redirect(url_for('grocery_list.view', meal_ids=meal_ids))

    # Only show recipes created by the current user
    user_id = session.get('user_id')
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    return render_template('meal_plan.html', recipes=recipes)

@meal_plan_bp.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        user_id = session['user_id']

        if not title or not ingredients:
            flash('Title and ingredients are required', 'error')
            return redirect(url_for('meal_plan.add_recipe'))

        new_recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            user_id=user_id
        )

        db.session.add(new_recipe)
        db.session.commit()

        flash('Recipe added successfully!', 'success')
        return redirect(url_for('meal_plan.plan'))

    return render_template('add_recipe.html')
