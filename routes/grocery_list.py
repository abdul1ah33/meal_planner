from flask import Blueprint, render_template
from models import db
from models.grocery_list import GroceryList

grocery_list_bp = Blueprint('grocery_list', __name__, url_prefix='/grocery-list')

@grocery_list_bp.route('/<int:meal_plan_id>')
def view(meal_plan_id):
    grocery_list = GroceryList.query.filter_by(meal_plan_id=meal_plan_id).first()
    return render_template('grocery_list.html', grocery_list=grocery_list)

