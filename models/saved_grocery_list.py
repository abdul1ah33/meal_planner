from . import db
from datetime import datetime
import json

class SavedGroceryList(db.Model):
    __tablename__ = 'saved_grocery_lists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)  # Stored as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_ingredients(self, ingredients_list):
        self.ingredients = json.dumps(ingredients_list)

    def get_ingredients(self):
        return json.loads(self.ingredients)
