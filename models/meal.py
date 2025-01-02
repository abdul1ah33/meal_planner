from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Meal model
class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.relationship('Ingredient', backref='meal', lazy=True)

# Ingredient model
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50))  # For example, "2 cups", "1 lb"
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
