from . import db
from datetime import datetime
import json

class MealPlan(db.Model):
    __tablename__ = 'meal_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    week_start_date = db.Column(db.Date, nullable=False)
    meals_data = db.Column(db.Text, nullable=False)  # JSON string storing meal selections
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_meals(self, meals_dict):
        """Store meals dictionary as JSON string"""
        self.meals_data = json.dumps(meals_dict)

    def get_meals(self):
        """Retrieve meals dictionary from JSON string"""
        return json.loads(self.meals_data) if self.meals_data else {}

    def __repr__(self):
        return f"<MealPlan for week starting {self.week_start_date}>"
