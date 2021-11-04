from wtforms import IntegerField, StringField, HiddenField, SubmitField
from flask_wtf import FlaskForm


class CreateShipmentMethodForm(FlaskForm):
    cost = IntegerField('Cost')
    estimated_time = IntegerField('Estimated time in days')
    name = StringField('Name')
    submit = SubmitField('Create')


class EditShipmentMethodForm(FlaskForm):
    cost = IntegerField('Cost')
    estimated_time = IntegerField('Estimated time in days')
    name = StringField('Name')
    shipment_method_id = HiddenField()
    submit = SubmitField('Edit')
