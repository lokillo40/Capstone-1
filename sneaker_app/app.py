import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, timedelta
from dotenv import load_dotenv  # Import load_dotenv to load environment variables

# Load environment variables from .env file
load_dotenv()


from sneaker_app.forms import RegistrationForm, LoginForm, EditProfileForm, DeleteAccountForm, AddToFavoritesForm, SearchForm, FavoritesForm, EditPasswordForm
import requests

import sneaker_app.models
from sneaker_app.models import User, db, connect_db, Favorite
from sneaker_app.config import Config
from sneaker_app.search_utils import perform_search

# Create a Flask application
def create_app():
   
    # Create a Flask application
    app = Flask(__name__)

    # Configure your app using the Config class
    app.config.from_object(Config)
    # Initialize CSRF protection for the Flask app
    csrf = CSRFProtect(app)

    connect_db(app)
    app.app_context().push()
    db.create_all()

    # Initialize SQLAlchemy and Bcrypt
    bcrypt = Bcrypt(app)

    # Define the API endpoint URL
    API_URL = "https://v1-sneakers.p.rapidapi.com/v1/sneakers"


    @app.route('/')
    def home():
        form = SearchForm() 
        try:
            # Make an API request to retrieve sneaker data
            querystring = {"limit": "10"}  # Adjust the limit as needed
            headers = {
                "X-RapidAPI-Key": app.config.get('RAPIDAPI_KEY'),
                "X-RapidAPI-Host": "v1-sneakers.p.rapidapi.com"
            }           
            response = requests.get(API_URL, headers=headers, params=querystring)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON data from the API response
                api_sneaker_data = response.json()

                # Pass the data and the form to the template for rendering
                return render_template('home.html', sneaker_data=api_sneaker_data, form=form)
            else:
                # Handle API request errors
                flash("Error: Unable to retrieve data from the API", 'error')
                return render_template('home.html', form=form)  # Ensure form is passed even in case of an error

        except Exception as e:
            # Handle exceptions
            flash(f"Error: {str(e)}", 'error')
            return render_template('home.html', form=form)  # Ensure form is passed even in case of an exception


    @app.route("/login", methods=['GET', 'POST'])
    def login():
        # Create a LoginForm instance
        form = LoginForm()

        # Check if the form has been submitted and is valid
        if form.validate_on_submit():
            # Query the database for a user with the provided email
            user = User.query.filter_by(Email=form.email.data).first()

            # Check if a user with the given email exists and the password is correct
            if user and bcrypt.check_password_hash(user.Password, form.password.data):
                # Store the user's ID and username in the session to track the login status
                session['user_id'] = user.UserID
                session['username'] = user.Username  # Store the username in the session

                # Display a success message using flash
                flash('You have been logged in!', 'success')

                # Redirect the user to the home page or dashboard
                return redirect(url_for('home'))

            # If login is unsuccessful, display an error message
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')

        # If the form is not submitted or not valid, render the login page
        return render_template('users/login.html', title='Login', form=form)

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()

        if form.validate_on_submit():
            # Check if the username or email already exists in the database
            existing_user = User.query.filter(
                (User.Email == form.email.data) | (User.Username == form.username.data)
            ).first()

            if existing_user:
                # If a user is found with the same email or username, flash a message and return the same registration page
                flash('Email or username is already registered.', 'danger')
                return render_template('users/register.html', title='Register', form=form)

            # Hash the user's password for security
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            # Create a new User object with the form data
            user = User(
                Username=form.username.data,
                Email=form.email.data,
                Password=hashed_password,
                FullName=form.full_name.data  # Assuming your form has a 'full_name' field
            )

            # Add the new user to the database session
            db.session.add(user)

            # Commit the changes to the database
            db.session.commit()

            # Flash a success message
            flash('Your account has been created! You are now able to log in', 'success')

            # Redirect the user to the login page
            return redirect(url_for('login'))

        # If the form is not submitted or not valid, render the registration page
        return render_template('users/register.html', title='Register', form=form)



    @app.route("/logout")
    def logout():
        # Remove the user_id and username from the session
        session.pop('user_id', None)
        session.pop('username', None)  # Make sure to remove the username as well
        
        # Display a success message using flash
        flash('You have been logged out!', 'success')  
        
        # Redirect to home page
        return redirect(url_for('home')) 

    @app.route('/profile')
    def profile():
        form = SearchForm()  # Instantiate the form
        # Check if user is logged in
        if 'user_id' not in session:
            flash('Please log in to view this page.', 'danger')
            return redirect(url_for('login'))

        user_id = session['user_id']
        # Fetch user data from the database
        user = User.query.get(user_id)
        
        if user is None:
            flash('User not found.', 'danger')
            return redirect(url_for('home'))

        # Pass both the user data and the form to the template
        return render_template('users/profile.html', user=user, form=form)

    @app.route('/edit-profile', methods=['GET', 'POST'])
    def edit_profile():
        # Check if user is logged in
        if 'user_id' not in session:
            # If not logged in, redirect to login page with a message
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))

        # Retrieve the user's id from the session
        user_id = session['user_id']
        # Fetch the user from the database
        user = User.query.get(user_id)
        # Instantiate the profile edit form
        form = EditProfileForm()

            # Handle form submission
        if form.validate_on_submit():
            # Update user object with form data
            user.Username = form.username.data
            user.Email = form.email.data
            user.FullName = form.full_name.data
            # Commit changes to the database
            db.session.commit()
            # Notify the user of success
            flash('Your profile has been updated!', 'success')
            # Redirect to the profile view function (if exists) or any other page
            return redirect(url_for('profile'))

        # Populate form with current user data if method is GET
        elif request.method == 'GET':
            form.username.data = user.Username
            form.email.data = user.Email
            form.full_name.data = user.FullName

        # Render the profile edit template
        return render_template('users/edit_profile.html', title='Edit Profile', form=form)

    @app.route('/delete-account', methods=['GET', 'POST'])
    def delete_account():
        # Check if user is logged in
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))

        form = DeleteAccountForm()  # Instantiate the delete account form

        if form.validate_on_submit():
            user_id = session['user_id']  # Retrieve the user's id from the session
            user = User.query.get(user_id)  # Fetch the user from the database

            if user and bcrypt.check_password_hash(user.Password, form.password.data):
                try:
            
                    # Update the UserID in the Favorite table to None for this user's favorites
                    Favorite.query.filter_by(UserID=user.UserID).update({"UserID": None})
                    # Delete the user from the database
                    db.session.delete(user)
                    # Commit the transaction
                    db.session.commit()
                    # Clear the user session to log them out
                    session.pop('user_id', None)
                    # Notify the user of account deletion
                    flash('Your account has been deleted!', 'success')
                    # Redirect to the home page
                    return redirect(url_for('home'))
                except Exception as e:
                    flash('An error occurred while deleting your account. Please try again later.', 'danger')
            else:
                flash('Password is incorrect.', 'danger')
                return render_template('users/delete_account.html', title='Delete Account', form=form)

        # Render the delete account template for GET request or if form is not valid
        return render_template('users/delete_account.html', title='Delete Account', form=form)




    @app.route('/search', methods=['GET', 'POST'])
    def search():
        form = SearchForm()  # Instantiate your form
        attempted_search = False

        if form.validate_on_submit():  # This will validate the form on POST
            search_query = form.search_query.data  # Get the data from the form field
            attempted_search = True  # A search was attempted

            # Access the RAPIDAPI_KEY from app.config
            rapidapi_key = app.config.get('RAPIDAPI_KEY')

            if rapidapi_key is None:
                flash('RAPIDAPI_KEY is not set. Check your environment variables or configuration.', 'error')
                return render_template('search.html', form=form, search_results=None, attempted_search=attempted_search)

            search_results, error = perform_search(search_query, API_URL, app)

            if error:
                flash(error, 'error')
                return render_template('search.html', form=form, search_results=None, attempted_search=attempted_search)

            if not search_results.get('results'):
                flash("No search results found.", 'error')
                return render_template('search.html', form=form, search_results=None, attempted_search=attempted_search)

            return render_template('search.html', form=form, search_results=search_results, attempted_search=attempted_search)

        # On GET or if form is not valid (e.g., empty field), render page with form
        return render_template('search.html', form=form, search_results=None, attempted_search=attempted_search)


    @app.route('/add_to_favorites/<sneaker_id>', methods=['POST'])
    def add_to_favorites(sneaker_id):
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': 'You must be logged in to add favorites.'}), 401

        user_id = session['user_id']
        user = User.query.get(user_id)

        # Check if the shoe is already in the user's favorites
        existing_favorite = Favorite.query.filter_by(UserID=user_id, SneakerID=sneaker_id).first()
        if existing_favorite:
            # Shoe is already in favorites
            return jsonify({'status': 'info', 'message': 'Sneaker is already in your favorites.'}), 200

        # Shoe is not in favorites, proceed to add
        new_favorite = Favorite(UserID=user_id, SneakerID=sneaker_id)
        db.session.add(new_favorite)
        try:
            db.session.commit()
            return jsonify({'status': 'success'}), 200
        except Exception as e:
            db.session.rollback()
            # Log the exception here
            return jsonify({'status': 'error', 'message': f'An error occurred while adding the sneaker to favorites: {e}'}), 500


    @app.route('/favorites', methods=['GET', 'POST'])
    def favorites():
        # Check if the user is logged in
        if 'user_id' not in session:
            flash('You must be logged in to access your favorites.', 'danger')
            return redirect(url_for('login'))

        # Create the FavoritesForm instance
        form = FavoritesForm()

        # Fetch the user's favorite sneakers' SneakerID from the database
        user_id = session['user_id']
        user = User.query.get(user_id)

        favorite_sneakers_info = []

        if user:
            favorite_sneaker_ids = [favorite.SneakerID for favorite in user.favorites]
            print("Favorite Sneaker IDs:", favorite_sneaker_ids)

            # Fetch sneaker information for each favorite
            for sneaker_id in favorite_sneaker_ids:
                url = f"https://v1-sneakers.p.rapidapi.com/v1/sneakers/{sneaker_id}"
                headers = {
                    "X-RapidAPI-Key": app.config.get('RAPIDAPI_KEY'),
                    "X-RapidAPI-Host": "v1-sneakers.p.rapidapi.com"
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    sneaker_info = response.json()
                    favorite_sneakers_info.append(sneaker_info)
                else:
                    flash('Failed to fetch sneaker information. Please try again later.', 'danger')

            print("Favorite Sneaker Info:", favorite_sneakers_info)

            return render_template('users/favorites.html', favorite_sneakers_info=favorite_sneakers_info, form=form)

        flash('User not found.', 'danger')
        return redirect(url_for('login'))

    @app.route('/delete_favorite/<string:sneaker_id>', methods=['POST'])
    def delete_favorite(sneaker_id):
        # Check if the user is logged in
        if 'user_id' not in session:
            flash('You must be logged in to delete favorites.', 'danger')
            return redirect(url_for('login'))

        # Check if the sneaker is in the user's favorites
        user_id = session['user_id']
        favorite = Favorite.query.filter_by(UserID=user_id, SneakerID=sneaker_id).first()

        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            flash('Sneaker removed from favorites.', 'success')
        else:
            flash('Sneaker is not in your favorites.', 'info')

        return redirect(url_for('favorites'))

    return app

# @app.route('/edit_password', methods=['GET', 'POST'])
# def edit_password():
#     form = EditPasswordForm()

#     if form.validate_on_submit():
#         # Get the current user's ID from the session
#         user_id = session.get('user_id')

#         # Retrieve the current user from the database
#         user = User.query.get(user_id)

#         if user and user.check_password(form.current_password.data):
#             # If the current password is correct, update the user's password
#             user.set_password(form.new_password.data)
#             db.session.commit()
#             flash('Password updated successfully.', 'success')
#             return redirect(url_for('profile'))
#         else:
#             flash('Current password is incorrect.', 'danger')

#     return render_template('users/edit_password.html', title='Edit Password', form=form)





# if __name__ == '__main__':
#     # Create the database tables (you may want to run this manually or use migrations)
#     with app.app_context():
#         db.create_all()
    
    # Run the Flask app in debug mode

if __name__ == '__main__':
    # Create the Flask app instance
    app = create_app()
    app.run(debug=True)
