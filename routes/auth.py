from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from models.recipe import Recipe
from utils.default_recipes import default_recipes

# Create the blueprint with a name that matches the URL prefix
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('meal_plan.plan'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email and password are required', 'danger')
            return redirect(url_for('auth.signup'))

        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.signup'))

        try:
            # Create new user
            new_user = User(
                email=email,
                password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.flush()  # Get the user ID before committing

            # Add default recipes for the new user
            for recipe_data in default_recipes:
                recipe = Recipe(
                    title=recipe_data["title"],
                    description=recipe_data["description"],
                    ingredients=recipe_data["ingredients"],
                    user_id=new_user.id
                )
                db.session.add(recipe)

            db.session.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            print(f"Registration error: {str(e)}")  # For debugging
            return redirect(url_for('auth.signup'))

    return render_template('auth/signup.html')

@auth_bp.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

# Optional: Protection decorator for routes that require login
from functools import wraps
from flask import abort

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
