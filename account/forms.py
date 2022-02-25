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
    phone_number = StringField('Phone number')
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
    password = PasswordField('Enter your password', validators=[DataRequired()])
    submit = SubmitField(label='Log in')


class SearchAccountForm(FlaskForm):
    customer_phone_number = StringField('Search by customer`s phone number (with `+`)')
    customer_name = StringField('Search by customer`s name (full name should be given)',
                                render_kw={'placeholder': 'Name surname patronymic', 'style': 'width:400px'})

    submit = SubmitField('Search')

    def validate(self):
        if super().validate():

            if not self.at_least_one_value():
                self.customer_name.errors.append('At least one field must have a value')
                return False
            elif self.customer_name.data and not self.full_name_given():
                self.customer_name.errors.append('Enter full customer`s name')
                return False
            else:
                return True

        return False

    def at_least_one_value(self):
        if self.customer_phone_number.data or self.customer_name.data:
            return True
        return False

    def full_name_given(self):
        if len(self.customer_name.data.split(' ')) == 3:
            return True
        return False


