from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password_hash=password).first()

        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
        else:
            new_user = User(username=username, email=email, password_hash=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('signup.html')

