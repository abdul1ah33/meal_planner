from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
from models import db
from models.recipe import Recipe
from models.meal_plan import MealPlan
import json

meal_plan_bp = Blueprint('meal_plan', __name__, url_prefix='/meal-plan')

@meal_plan_bp.route('/', methods=['GET', 'POST'])
def plan():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    
    # Get recipes grouped by meal type
    breakfast_recipes = Recipe.query.filter_by(user_id=user_id, meal_type='breakfast').all()
    lunch_recipes = Recipe.query.filter_by(user_id=user_id, meal_type='lunch').all()
    dinner_recipes = Recipe.query.filter_by(user_id=user_id, meal_type='dinner').all()

    if request.method == 'POST':
        meals_data = {}
        week_start = datetime.strptime(request.form.get('week_start'), '%Y-%m-%d').date()
        
        # Collect meal selections for each day and meal type
        for day in range(7):
            day_meals = {}
            for meal_type in ['breakfast', 'lunch', 'dinner']:
                meal_key = f"day{day}_{meal_type}"
                selected_meal = request.form.get(meal_key)
                if selected_meal:
                    day_meals[meal_type] = int(selected_meal)
            if day_meals:
                meals_data[str(day)] = day_meals

        # Create or update meal plan
        meal_plan = MealPlan.query.filter_by(
            user_id=user_id,
            week_start_date=week_start
        ).first()

        if not meal_plan:
            meal_plan = MealPlan(
                user_id=user_id,
                week_start_date=week_start
            )

        meal_plan.set_meals(meals_data)
        db.session.add(meal_plan)
        db.session.commit()

        # Generate grocery list for all meals or specific day
        day_filter = request.form.get('day_filter')
        return redirect(url_for('grocery_list.view', 
                              meal_plan_id=meal_plan.id,
                              day_filter=day_filter if day_filter else 'all'))

    # Calculate default week start date (next Monday)
    today = datetime.now().date()
    days_ahead = 7 - today.weekday()
    next_monday = today + timedelta(days=days_ahead)
    
    return render_template('meal_plan.html', 
                         breakfast_recipes=breakfast_recipes,
                         lunch_recipes=lunch_recipes,
                         dinner_recipes=dinner_recipes,
                         week_start=next_monday)

@meal_plan_bp.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    """Handle adding new recipes"""
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        meal_type = request.form.get('meal_type')
        user_id = session['user_id']

        if not title or not ingredients or not meal_type:
            flash('Title, ingredients, and meal type are required', 'error')
            return redirect(url_for('meal_plan.add_recipe'))

        new_recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            meal_type=meal_type,
            user_id=user_id
        )

        db.session.add(new_recipe)
        db.session.commit()

        flash('Recipe added successfully!', 'success')
        return redirect(url_for('meal_plan.plan'))

    return render_template('add_recipe.html')
