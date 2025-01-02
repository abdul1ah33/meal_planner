from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Use a secure key

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meal_planner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import db and initialize with app
from models import db, init_db
init_db(app)

# Initialize migration tools
migrate = Migrate(app, db)

# Import blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.meal_plan import meal_plan_bp  # Import the meal_plan blueprint

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(main_bp)
app.register_blueprint(meal_plan_bp, url_prefix='/meal-plan')  # Register the meal_plan blueprint

if __name__ == '__main__':
    app.run(debug=True)

