from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.recipe import Recipe
from models.meal_plan import MealPlan

meal_plan_bp = Blueprint('meal_plan', __name__, url_prefix='/meal-plan')

@meal_plan_bp.route('/', methods=['GET', 'POST'])
def plan():
    if request.method == 'POST':
        # Save meal plan logic
        flash('Meal plan created successfully!', 'success')
        return redirect(url_for('main.index'))

    recipes = Recipe.query.all()
    return render_template('meal_plan.html', recipes=recipes)

