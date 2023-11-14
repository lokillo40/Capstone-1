from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class RegistrationForm(FlaskForm):
    # Form to sign up a new user
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    full_name = StringField(
        "Full Name", validators=[DataRequired(), Length(min=2, max=50)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    # Form to log in user
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class EditProfileForm(FlaskForm):
    # Form to edit profile
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    full_name = StringField(
        "Full Name", validators=[DataRequired(), Length(min=2, max=50)]
    )
    submit = SubmitField("Update Profile")


class DeleteAccountForm(FlaskForm):
    # Form to delete user
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Delete Account")


class AddToFavoritesForm(FlaskForm):
    # Form to add to favorite
    submit = SubmitField("Add to Favorites", validators=[DataRequired()])


class SearchForm(FlaskForm):
    # Form to search
    search_query = StringField("Search Query", validators=[DataRequired()])


class FavoritesForm(FlaskForm):
    sneaker_id = StringField("Sneaker ID", validators=[DataRequired()])
    submit = SubmitField("Fetch Sneaker Info")


class EditPasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", [validators.DataRequired()])
    new_password = PasswordField(
        "New Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm_password", message="Passwords must match"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm New Password", [validators.DataRequired()]
    )
    submit = SubmitField("Update Password")
