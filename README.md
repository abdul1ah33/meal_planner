# Meal Planner Application 🍽️

A full-stack web application for meal planning, grocery list generation, and recipe management with user feedback capabilities.

## Features ✨

1. **User Authentication**
   - Secure registration/login system
   - Password hashing
   - Session management

2. **Meal Planning**
   - Weekly meal plan creation
   - Meal type categorization (Breakfast/Lunch/Dinner)
   - Drag-and-drop recipe assignment (UI implementation needed)

3. **Recipe Management**
   - Create/store custom recipes
   - Default recipe collection
   - Ingredients list management

4. **Grocery List Generation**
   - Auto-generated shopping lists
   - Manual ingredient additions/removals
   - Save/load previous lists

5. **Feedback System**
   - User ratings (1-5 stars)
   - Public feedback comments
   - Edit/delete own feedback

6. **Additional Features**
   - Responsive UI
   - Interactive forms
   - Database persistence
   - Flash notifications

## How It Works 🔧

1. **User Flow**
   - Registration → Login → Meal Planning → Recipe Management → Grocery List → Feedback

2. **Core Components**
- **Frontend**: Jinja2 templates + Bootstrap CSS
- **Backend**: Flask RESTful routes
- **Database**: SQLAlchemy ORM with SQLite
- **Auth**: Session-based with password hashing

## Installation 🛠️

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/meal-planner.git
cd meal-planner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
flask db init
flask db migrate
flask db upgrade

# Configure environment
cp .env.example .env

Configuration ⚙️
.env file requirements:

ini
Copy
SECRET_KEY=your_secret_key_here
SQLALCHEMY_DATABASE_URI=sqlite:///meal_planner.db
Usage 🚀
Start the Application

bash
Copy
flask run
Access in Browser

Copy
http://localhost:5000
Basic Workflow

Register new account

Create meal plan for the week

Add custom recipes

Generate grocery list

Save/share lists

Provide feedback

API Documentation 📚
Authentication Endpoints
Method	Endpoint	Description	Request Body
POST	/auth/login	User login	{email: str, password: str}
POST	/auth/signup	User registration	{email: str, password: str}
GET	/auth/logout	User logout	None
Meal Plan Endpoints
Method	Endpoint	Description	Parameters
GET	/meal-plan	View meal plan	None
POST	/meal-plan	Save meal plan	{week_start: date, meals: JSON}
POST	/meal-plan/add	Add new recipe	{title: str, ingredients: str}
Grocery List Endpoints
Method	Endpoint	Description	Parameters
GET	/grocery-list/int:id	View grocery list	day_filter: str (optional)
POST	/grocery-list/save	Save grocery list	{name: str, items: list}
DELETE	/grocery-list/int:id	Delete saved list	None
Feedback Endpoints
Method	Endpoint	Description	Request Body
GET	/feedback	View all feedback	None
POST	/feedback/create	Create new feedback	{rating: int, content: str}
PUT	/feedback/int:id	Update feedback	{rating: int, content: str}
DELETE	/feedback/int:id	Delete feedback	None
Testing 🧪
Run test suite:

bash
Copy
python -m unittest discover tests
Technologies Used 💻
Frontend:

HTML5/CSS3

Bootstrap 5

Jinja2 Templating

Backend:

Python 3

Flask

SQLAlchemy

Flask-Migrate

Database:

SQLite (Development)

PostgreSQL (Production-ready)

License 📄
MIT License - See LICENSE for details

Support & Contact 📧
For issues or feature requests, please open an issue on GitHub

Copy

This README includes:
1. Comprehensive feature list
2. System architecture overview
3. Installation/configuration instructions
4. Detailed API documentation
5. Usage examples
6. Testing information
7. Technology stack
8. License and contact info

You might want to:
1. Add screenshots in a `## Screenshots` section
2. Include deployment instructions for production
3. Add contribution guidelines
4. Include badges for build status/coverage
5. Add a roadmap section for future features

