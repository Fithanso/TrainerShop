from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, Optional
from flask_wtf import FlaskForm


class NonValidatingDateField(DateField):
    def pre_validate(self, form):
        pass


class EditAccountForm(FlaskForm):
    login = StringField('Login')
    password = PasswordField('Password')
    name = StringField('Name')
    surname = StringField('Surname')
    patronymic = StringField('Patronymic (if there is)')
    delivery_address = StringField('Delivery address')
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[Optional()])

    submit = SubmitField('Edit personal data')


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

