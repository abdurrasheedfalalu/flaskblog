from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ( DataRequired, Length, Regexp, Email,
                                EqualTo, ValidationError)

from app.models import User



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={'placeholder': 'admin@example.com'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                        Length(min=2, max=20), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, message='username must have only number dot or underscore')], render_kw={'placeholder': 'Enter your username'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'admin@example.com'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField('Confirn Password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'Repeat Password'})
    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('username already exist. Choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('email already exist. Choose another.')