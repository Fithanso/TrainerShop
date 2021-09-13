from wtforms import Form, StringField, PasswordField


class SignupForm(Form):
    email = StringField('Enter your email')
    password = PasswordField('Enter your password')


class LoginForm(Form):
    email = StringField('Enter your email')
    password = PasswordField('Enter your password')
