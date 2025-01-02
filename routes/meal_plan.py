from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.recipe import Recipe
from models.meal_plan import MealPlan

# Define the Blueprint
meal_plan_bp = Blueprint('meal_plan', __name__, url_prefix='/meal-plan')

@meal_plan_bp.route('/', methods=['GET', 'POST'])
def plan():
    if request.method == 'POST':
        selected_meals = request.form.getlist('meals')  # List of selected meal IDs
        if not selected_meals:
            flash('Please select at least one meal.', 'warning')
            return redirect(url_for('meal_plan.plan'))
        
        # Optional: Save the meal plan to the database
        # ...

        # Redirect to grocery list page with selected meal IDs
        meal_ids = ','.join(selected_meals)
        return redirect(url_for('grocery_list.view', meal_ids=meal_ids))

    recipes = Recipe.query.all()
    return render_template('meal_plan.html', recipes=recipes)

