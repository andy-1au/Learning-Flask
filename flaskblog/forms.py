from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import MyUser

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password',  message=" The entered passwords do not match.")])
    submit = SubmitField('Sign Up')

    # validate if username is taken
    # self parameter is a reference to the current instance of the RegistrationForm class
    # allows the method to access other attributes or methods of the form, such as `self.username.data`
    # self is also used implicitly
    def validate_username(self, username):
        user = MyUser.query.filter_by(username=username.data).first() # if there's already a user with the username passed in
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.') # raise the error
    
    # validate if email is taken
    def validate_email(self, email):
        email = MyUser.query.filter_by(email=email.data).first()
        # if the email already exist in the db
        if email: 
            raise ValidationError('This email is already taken. Please choose a different one.')

class LoginForm(FlaskForm):
    # use email as username
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    # validate if username is taken
    # self parameter is a reference to the current instance of the RegistrationForm class
    # allows the method to access other attributes or methods of the form, such as `self.username.data`
    # self is also used implicitly
    def validate_username(self, username):
        if username.data != current_user.username: # if they entered something different from their username
            user = MyUser.query.filter_by(username=username.data).first() # if there's already a user with the username passed in
            if user:
                raise ValidationError('This username is already taken. Please choose a different one.') # raise the error
    
    # validate if email is taken
    def validate_email(self, email):
        if email.data != current_user.email: # if they entered something different from their email
            email = MyUser.query.filter_by(email=email.data).first()
            # if the email already exist in the db
            if email: 
                raise ValidationError('This email is already taken. Please choose a different one.')