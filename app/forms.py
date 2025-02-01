from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from app.database.models import User

class RegistrationForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[DataRequired(), Length(min=2, max=64)]
    )
    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        label='Password',
        validators=[DataRequired(), Length(min=8)]
    )
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username занят')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email занят')


class LoginForm(FlaskForm):
    email = StringField(
        label='Email',
        validators=[DataRequired(), Length(min=8)]
    )
    password = PasswordField(
        label='Password',
        validators=[DataRequired(), Length(min=8)]
    )
    submit = SubmitField('Login')