from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create instances of SQLAlchemy and Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    # Define the User table columns
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)  # Hashed and salted password
    Email = db.Column(db.String(255), unique=True, nullable=False)
    FullName = db.Column(db.String(255), nullable=False)
    JoinDate = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Define relationships (if necessary, e.g., for favorites)
    # Example: user.favorites will give access to user's favorite sneakers

class Favorite(db.Model):
    __tablename__ = 'favorites'
    # Define the Favorite table columns
    FavoriteID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID', ondelete='CASCADE'), nullable=False)
    SneakerID = db.Column(db.String(255), nullable=False)

    # Define relationships
    user = db.relationship('User', backref=db.backref('favorites', lazy=True, cascade="all, delete-orphan"))

    # DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
