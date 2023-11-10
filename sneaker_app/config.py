import os


class Config(object):
    SECRET_KEY = os.environ.get('MY_APP_SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///sneaker_app')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY', 'your-default-api-key')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use an in-memory SQLite database for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF tokens in the forms for tests
    SECRET_KEY = os.environ.get('MY_APP_SECRET_KEY', 'default-secret-key')
