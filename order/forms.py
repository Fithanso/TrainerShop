from app import ALLOWED_EXTENSIONS
from wtforms import StringField, IntegerField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, optional
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class CreateOrderForm(FlaskForm):
    name = StringField('Name of recipient', validators=[DataRequired()])
    surname = StringField('Surname of recipient', validators=[DataRequired()])
    patronymic = StringField('Patronymic of recipient (if there is)', validators=[DataRequired()])
    delivery_address = StringField('Delivery address', validators=[DataRequired()])
    phone_number = StringField('Phone number of recipient', validators=[DataRequired()])
    email = StringField('Email of recipient', validators=[DataRequired()])
    # I used my own class because I get "Not a valid choice" error every time
    shipment_method = NonValidatingSelectField('Delivery type', render_kw={'style': 'width:300px'})
    customer_id = HiddenField()
    purchased_products = HiddenField()

    submit = SubmitField('Create order')


class SearchOrderForm(FlaskForm):
    order_id = IntegerField('Search by ID', validators=[optional()])
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
        if self.order_id.data or self.customer_phone_number.data or self.customer_name.data:
            return True
        return False

    def full_name_given(self):
        if len(self.customer_name.data.split(' ')) == 3:
            return True
        return False


