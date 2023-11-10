# Sneakers-app

## What is Sneakers-app?
Sneakers-app platform for sneaker enthusiasts to stay up-to-date with the latest sneaker releases. The website allows users to register, log in, search for sneakers, and maintain a list of their favorite sneakers.

## Features
- **User Registration and Login**: Secure sign-up and authentication system for users to create and access their accounts.
- **Sneaker Search**: A comprehensive search feature that allows users to find sneakers by brand, colorway and other criteria.
- **Favorites List**: Users can curate and manage a list of their favorite sneakers.
- **Sneaker Information**: Detailed information on sneaker releases, including images and descriptions, sourced from the "v1 sneakers" API.

## Tests
Tests are located in a file named `test_app.py`. To run these tests, use the following command in the terminal:

```bash
python test_app.py
```

## User Flow
- **Registration/Login**: Users start by registering for a new account or logging into an existing one.
- **Searching**: Once logged in users can search for sneakers using various criteria such as brand and release date.
- **Favorites**: Users can add sneakers to their favorites list for easy access later.
- **Editing**: Users can edit their profiles and delete sneaker from their favorites list.

## Technology Stack
- **Backend**: Python with Flask
- **Frontend**: jQuery and Bootstrap
- **API**: "v1 sneakers" API from RapidAPI.com for sneaker data
- **Database**: A relational database with a schema for users and favorites

## Setup Instructions

1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. sudo service postgresql start
5. update .env file
6. createdb sneaker_app
7. python seed.py
8. flask run






API LINK: https://rapidapi.com/tg4-solutions-tg4-solutions-default/api/v1-sneakers