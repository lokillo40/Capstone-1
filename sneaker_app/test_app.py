import logging
import unittest
from app import app, db, User
from flask import session
from config import TestConfig  # You need to create a TestConfig class for testing environment
from flask_bcrypt import Bcrypt

# Initialize Bcrypt for the test module
bcrypt = Bcrypt(app)

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("unittestLogger")

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        logger.debug('Setting up the test.')
        # Set up test configuration
        app.config.from_object(TestConfig)
        self.app = app.test_client()

        # Establish an application context
        self.ctx = app.app_context()
        self.ctx.push()
        logger.debug('Application context pushed.')

        # Create tables
        db.create_all()
        logger.debug('Database tables created.')

        # Begin a new transaction
        self.connection = db.engine.connect()
        self.transaction = self.connection.begin()
        db.session.configure(bind=self.connection)
        logger.debug('Database transaction started.')

        # Add a test user
        hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
        test_user = User(Username='testuser', Email='test@example.com', Password=hashed_password, FullName='Test User')
        db.session.add(test_user)
        db.session.flush()  # Use flush instead of commit
        logger.debug('Test user added to the session.')

    def tearDown(self):
        logger.debug('Tearing down the test.')
        db.session.remove()
        self.transaction.rollback()
        self.connection.close()
        logger.debug('Database transaction rolled back and connection closed.')

        # Drop all tables
        db.drop_all()
        logger.debug('Database tables dropped.')

        # Pop the application context
        self.ctx.pop()
        logger.debug('Application context popped.')


    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email, password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_home_route(self):
        # Test the home route with mock API response
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_successful_registration(self):
        response = self.app.post('/register', data=dict(
            username='newuser',
            email='new@example.com',
            password='newpassword',
            confirm_password='newpassword'
        ), follow_redirects=False)
        self.assertTrue(b'Your account has been created! You are now able to log in', response.data)

    def test_failed_registration(self):
        response = self.app.post('/register', data=dict(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            confirm_password='testpassword'
        ), follow_redirects=False)
        self.assertTrue(b'Email or username is already registered.', response.data)

    def test_login_logout(self):
        # Test login with correct credentials
        response = self.login('test@example.com', 'testpassword')
        self.assertIn(b'You have been logged in!', response.data)

        # Test logout
        response = self.logout()
        self.assertIn(b'You have been logged out!', response.data)

        # Test login with incorrect credentials
        response = self.login('test@example.com', 'wrongpassword')
        self.assertIn(b'Login Unsuccessful.', response.data)

    def test_profile_authentication(self):
        # Test profile route requires login
        response = self.app.get('/profile', follow_redirects=True)
        self.assertIn(b'Please log in to view this page.', response.data)

        # Test profile page with logged in user
        self.login('test@example.com', 'testpassword')
        response = self.app.get('/profile', follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    # You can add more test cases for search, add_to_favorites, delete_favorite, etc.

if __name__ == '__main__':
    unittest.main()