from app import app, db, bcrypt
from models import User, Favorite
from werkzeug.security import generate_password_hash

# Function to seed user data
def seed_users():
    # Create instances of the User model with sample data
     # Make sure to hash the passwords
    user1 = User(Username='user1', Email='user1@example.com', Password=generate_password_hash('password1'), FullName='User One')
    user2 = User(Username='user2', Email='user2@example.com', Password=generate_password_hash('password2'), FullName='User Two')
    # ... add more users as needed

    # Add users to the session
    db.session.add(user1)
    db.session.add(user2)
    # ... add more users to the session as needed

    # Commit the session to save users to the database
    db.session.commit()

# Function to seed favorite data
def seed_favorites():
    # Create instances of the Favorite model with sample data
    favorite1 = Favorite(UserID=1, SneakerID='sneaker1')
    favorite2 = Favorite(UserID=2, SneakerID='sneaker2')
    # ... add more favorites as needed

    # Add favorites to the session
    db.session.add(favorite1)
    db.session.add(favorite2)
    # ... add more favorites to the session as needed

    # Commit the session to save favorites to the database
    db.session.commit()

# Function to seed all data
def seed_data():
    # Call the seed functions
    seed_users()
    seed_favorites()

# The main entry point for the script
if __name__ == '__main__':
    # Create and push an application context
    with app.app_context():
        # Drop all tables if they exist and create them
        db.drop_all()
        db.create_all()

        # Call the function to seed the database
        seed_data()

        print("Database has been seeded.")