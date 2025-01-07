from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.feedback import Feedback
from models.user import User
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

@feedback_bp.route('/')
def index():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template('feedback/index.html', feedbacks=feedbacks)

@feedback_bp.route('/create', methods=['GET', 'POST'])
def create():
    if 'user_id' not in session:
        flash('Please login to leave feedback', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        rating = request.form.get('rating', type=int)
        content = request.form.get('content')

        if not rating or not content:
            flash('Both rating and content are required', 'error')
            return redirect(url_for('feedback.create'))

        if not 1 <= rating <= 5:
            flash('Rating must be between 1 and 5', 'error')
            return redirect(url_for('feedback.create'))

        feedback = Feedback(
            user_id=session['user_id'],
            rating=rating,
            content=content
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('feedback.index'))

    return render_template('feedback/create.html')

@feedback_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('auth.login'))

    feedback = Feedback.query.get_or_404(id)
    
    if feedback.user_id != session['user_id']:
        flash('You can only edit your own feedback', 'error')
        return redirect(url_for('feedback.index'))

    if request.method == 'POST':
        rating = request.form.get('rating', type=int)
        content = request.form.get('content')

        if not rating or not content:
            flash('Both rating and content are required', 'error')
            return redirect(url_for('feedback.edit', id=id))

        if not 1 <= rating <= 5:
            flash('Rating must be between 1 and 5', 'error')
            return redirect(url_for('feedback.edit', id=id))

        feedback.rating = rating
        feedback.content = content
        feedback.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Feedback updated successfully!', 'success')
        return redirect(url_for('feedback.index'))

    return render_template('feedback/edit.html', feedback=feedback)

@feedback_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('auth.login'))

    feedback = Feedback.query.get_or_404(id)
    
    if feedback.user_id != session['user_id']:
        flash('You can only delete your own feedback', 'error')
        return redirect(url_for('feedback.index'))

    db.session.delete(feedback)
    db.session.commit()
    
    flash('Feedback deleted successfully!', 'success')
    return redirect(url_for('feedback.index'))
