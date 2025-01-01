from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the Flask app.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()

# Import models here
from models.user import User  # Import the User model

# This makes `User` accessible when importing `models`
__all__ = ["db", "init_db", "User"]

