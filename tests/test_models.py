# tests/test_models.py
import unittest
from app import create_app, db
from app.models import UserModel, QuestionModel, AnswerModel, EventModel, LikeModel, CommentModel
from datetime import datetime

class ModelTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create a test client
        self.client = self.app.test_client()

    def tearDown(self):
        """Tear down test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model(self):
        """Test user model functionality."""
        user = UserModel(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        # Check if user is in the database
        user_in_db = UserModel.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user_in_db)
        self.assertTrue(user_in_db.check_password('password123'))
        self.assertFalse(user_in_db.check_password('wrongpassword'))

    def test_question_model(self):
        """Test question model functionality."""
        user = UserModel(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        question = QuestionModel(title='Test Question', content='This is a test question.', author_id=user.id)
        db.session.add(question)
        db.session.commit()

        # Check if question is in the database
        question_in_db = QuestionModel.query.filter_by(title='Test Question').first()
        self.assertIsNotNone(question_in_db)
        self.assertEqual(question_in_db.content, 'This is a test question.')
        self.assertEqual(question_in_db.author_id, user.id)

    def test_answer_model(self):
        """Test answer model functionality."""
        user = UserModel(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        question = QuestionModel(title='Test Question', content='This is a test question.', author_id=user.id)
        db.session.add(question)
        db.session.commit()

        answer = AnswerModel(content='This is a test answer.', question_id=question.id, author_id=user.id)
        db.session.add(answer)
        db.session.commit()

        # Check if answer is in the database
        answer_in_db = AnswerModel.query.filter_by(content='This is a test answer.').first()
        self.assertIsNotNone(answer_in_db)
        self.assertEqual(answer_in_db.question_id, question.id)
        self.assertEqual(answer_in_db.author_id, user.id)

    def test_event_model(self):
        """Test event model functionality."""
        user = UserModel(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        event = EventModel(
            title='Test Event', 
            location='Test Location', 
            description='This is a test event.', 
            author_id=user.id, 
            event_time=datetime.utcnow()
        )
        db.session.add(event)
        db.session.commit()

        # Check if event is in the database
        event_in_db = EventModel.query.filter_by(title='Test Event').first()
        self.assertIsNotNone(event_in_db)
        self.assertEqual(event_in_db.location, 'Test Location')
        self.assertEqual(event_in_db.author_id, user.id)

    def test_like_model(self):
        """Test like model functionality."""
        user = UserModel(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        event = EventModel(
            title='Test Event', 
            location='Test Location', 
            description='This is a test event.', 
            author_id=user.id, 
            event_time=datetime.utcnow()
        )
        db.session.add(event)
        db.session.commit()

        like = LikeModel(event_id=event.id, user_id=user.id)
        db.session.add(like)
        db.session.commit()

        # Check if like is in the database
        like_in_db = LikeModel.query.filter_by(event_id=event.id, user_id=user.id).first()
        self.assertIsNotNone(like_in_db)

    def test_comment_model(self):
        """Test comment model functionality."""
        user = UserModel(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        event = EventModel(
            title='Test Event', 
            location='Test Location', 
            description='This is a test event.', 
            author_id=user.id, 
            event_time=datetime.utcnow()
        )
        db.session.add(event)
        db.session.commit()

        comment = CommentModel(content='This is a test comment.', event_id=event.id, user_id=user.id)
        db.session.add(comment)
        db.session.commit()

        # Check if comment is in the database
        comment_in_db = CommentModel.query.filter_by(content='This is a test comment.').first()
        self.assertIsNotNone(comment_in_db)
        self.assertEqual(comment_in_db.event_id, event.id)
        self.assertEqual(comment_in_db.user_id, user.id)

if __name__ == '__main__':
    unittest.main()
