from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegistrationForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[DataRequired(), Length(min=2, max=64)]
    )
    email = StringField(
        label='Email',
        validators=[DataRequired(), Length(min=8)]
    )
    password = PasswordField(
        label='Password',
        validators=[DataRequired(), Length(min=8)]
    )
    submit = SubmitField('Sign Up')


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