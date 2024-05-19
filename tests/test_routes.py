# tests/test_routes.py
import unittest
from datetime import datetime
from flask import url_for
from app import create_app, db
from app.models import UserModel, QuestionModel, EventModel, LikeModel
from unittest.mock import patch
class BasicTests(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')
        self.app.config['SERVER_NAME'] = 'localhost'  # Add this line
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create test users
        self.user = UserModel(username='testuser', email='test@example.com')
        self.user.set_password('password123')
        self.other_user = UserModel(username='otheruser', email='other@example.com')
        self.other_user.set_password('password123')
        db.session.add(self.user)
        db.session.add(self.other_user)
        db.session.commit()

    def tearDown(self):
        """Tear down test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_welcome_page(self):
        """Test welcome page."""
        response = self.client.get(url_for('main.welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to PetPals Forum', response.data)

    def test_login(self):
        """Test login functionality."""
        response = self.login('testuser', 'password123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_logout(self):
        """Test logout functionality."""
        self.login('testuser', 'password123')
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to PetPals Forum', response.data)  # Adjust this line to match the actual content

    def test_create_question(self):
        """Test question creation."""
        self.login('testuser', 'password123')
        response = self.client.post('/public_question', data=dict(
            title='Test Question',
            content='This is a test question.'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        question = QuestionModel.query.filter_by(title='Test Question').first()
        self.assertIsNotNone(question)

    def test_create_event(self):
        """Test event creation."""
        self.login('testuser', 'password123')
        response = self.client.post('/create_event', data=dict(
            title='Test Event',
            location='Test Location',
            description='This is a test event.',
            event_time=datetime(2024, 1, 1, 0, 0)
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        event = EventModel.query.filter_by(title='Test Event').first()
        self.assertIsNotNone(event)

    def test_like_event(self):
        """Test liking an event."""
        self.login('otheruser', 'password123')
        event = EventModel(
            title='Test Event',
            location='Test Location',
            description='This is a test event.',
            author_id=self.other_user.id,
            event_time=datetime(2024, 1, 1, 0, 0)
        )
        db.session.add(event)
        db.session.commit()
        self.logout()

        
        self.login('testuser', 'password123')
        response = self.client.post(f'/like_event/{event.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Event liked successfully.', response.data)
        like = LikeModel.query.filter_by(event_id=event.id, user_id=self.user.id).first()
        self.assertIsNotNone(like)

    @patch('app.routes.send_password_reset_email')
    def test_reset_password_request(self, mock_send_email):
        """Test requesting a password reset."""
        response = self.client.post('/reset_password_request', data={
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(mock_send_email.called)  
    def test_reset_password(self):
        """Test resetting the password."""
        with self.app_context:
            token = self.user.get_reset_password_token()
        
        response = self.client.get(url_for('main.reset_password', token=token))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url_for('main.reset_password', token=token), data={
            'password': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  
        user = db.session.get(UserModel, self.user.id)
        self.assertTrue(user.check_password('newpassword'))

if __name__ == '__main__':
    unittest.main()
