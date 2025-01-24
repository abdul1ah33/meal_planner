import unittest
from flask import url_for
from app import create_app, db
from models.user import User
from models.feedback import Feedback

class FeedbackRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
        # Create test user
        user = User(email='test@example.com', password='password')
        feedback = Feedback(
            user=user,
            rating=5,
            content='Great app!'
        )
        db.session.add_all([user, feedback])
        db.session.commit()
        
        # Login user
        with self.client.session_transaction() as sess:
            sess['user_id'] = user.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_feedback_index(self):
        response = self.client.get(url_for('feedback.index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Feedback', response.data)

    def test_create_feedback(self):
        response = self.client.post(url_for('feedback.create'), data={
            'rating': 5,
            'content': 'Test feedback'
        }, follow_redirects=True)
        self.assertEqual(Feedback.query.count(), 2)
        self.assertIn(b'Feedback submitted', response.data)

    def test_edit_feedback(self):
        response = self.client.post(url_for('feedback.edit', id=1), data={
            'rating': 4,
            'content': 'Updated feedback'
        }, follow_redirects=True)
        feedback = Feedback.query.get(1)
        self.assertEqual(feedback.rating, 4)
        self.assertIn(b'Feedback updated', response.data)

    def test_delete_feedback(self):
        response = self.client.post(url_for('feedback.delete', id=1),
                                   follow_redirects=True)
        self.assertEqual(Feedback.query.count(), 0)
        self.assertIn(b'Feedback deleted', response.data)

if __name__ == '__main__':
    unittest.main()
