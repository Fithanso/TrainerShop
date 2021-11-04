from app import ALLOWED_EXTENSIONS
from wtforms import StringField, IntegerField, SelectField, SubmitField, MultipleFileField, HiddenField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class CreateOrderForm(FlaskForm):
    name = StringField('Name of recipient', validators=[DataRequired()])
    surname = StringField('Surname of recipient', validators=[DataRequired()])
    patronymic = StringField('Patronymic of recipient', validators=[DataRequired()])
    delivery_address = StringField('Delivery address', validators=[DataRequired()])
    phone_number = StringField('Phone number of recipient', validators=[DataRequired()])
    email = StringField('Email of recipient', validators=[DataRequired()])
    # I used my own class because I get "Not a valid choice" error every time
    shipment_method = NonValidatingSelectField('Delivery type')
    customer_id = HiddenField()
    purchased_products = HiddenField()

    submit = SubmitField('Create order')
