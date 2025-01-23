from . import db
from datetime import datetime

class GroceryList(db.Model):
    __tablename__ = 'grocery_lists'

    id = db.Column(db.Integer, primary_key=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plans.id'), nullable=False)
    items = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<GroceryList for MealPlan {self.meal_plan_id}>"
    

