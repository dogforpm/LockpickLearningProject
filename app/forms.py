# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Users


# Define User Login forms
class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

# Define User Registration forms
class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name')
    password = PasswordField('Password', validators=[DataRequired()])
    # Gets user to enter their password twice, so they are more likely to avoid accidentally
    # mistyping the password they wanted to enter
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Wtforms internal validation method to check if the user name a user is entering
    # has or has not already been chosen by another user
    def validate_username(self, username):
        UsernameUnique = Users.query.filter_by(username=username.data.lower()).first()
        if UsernameUnique is not None:
            raise ValidationError('Please use a different username.')