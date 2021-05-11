from wtforms import Form, StringField


class SignupForm(Form):
    email = StringField('Enter your email')
    password = StringField('Enter your password')


class LoginForm(Form):
    email = StringField('Enter your email')
    password = StringField('Enter your password')
