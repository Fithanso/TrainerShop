from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import FlaskForm


class SignupForm(FlaskForm):
    email = StringField('Enter your email', validators=[DataRequired(),
                                                        Email(),
                                                        Length(max=120)])
    password = PasswordField('Enter your password', validators=[
        DataRequired(),
        Length(min=8, message='Password should be at least %(min)d characters long')])
    submit = SubmitField(label='Sign up')


class LoginForm(FlaskForm):
    email = StringField('Enter your email', validators=[DataRequired(),
                                                        Email(),
                                                        Length(max=120)])
    password = PasswordField('Enter your password', validators=[
        DataRequired()
        # Length(min=8, message='Password should be at least %(min)d characters long')
        ])
    submit = SubmitField(label='Log in')

