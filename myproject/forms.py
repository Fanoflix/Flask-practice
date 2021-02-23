# forms.py

# Imports
from flask.helpers import flash
from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class Registration(FlaskForm):
    # The validators is a list. DataRequired() makes this a must fill
    #                           Email() checks if the entry is in email format.
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    # EqualTo(pass_confirm) checks if its equal to the password given.
    password = PasswordField('Password', validators=[DataRequired()])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')
    
    # Checking if an email is already registered or not.
    def check_email(self, field):
        if User.query.filter_by(email=field).first():
            print('---------------------------------------------------TEST---------------------------------------------------')
            raise ValidationError('Your email is already registered.')

    # Checking if an username is already registered or not.
    def check_username(self, field):
        if User.query.filter_by(username=field).first():
            raise ValidationError('This username is taken.')

class Err(FlaskForm):
    err = SubmitField('Generate Error')