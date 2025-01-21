from models import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ingredients = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)  # 'breakfast', 'lunch', or 'dinner'

    @property
    def ingredients_list(self):
        """Return ingredients as a list"""
        return [i.strip() for i in self.ingredients.split(',')]

    def __repr__(self):
        return f"<Recipe {self.title}>"
