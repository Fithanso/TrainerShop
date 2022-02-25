from wtforms import IntegerField, StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class CreateShipmentMethodForm(FlaskForm):
    cost = IntegerField('Cost', validators=[DataRequired()])
    estimated_time = IntegerField('Estimated time in days', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create')


class EditShipmentMethodForm(FlaskForm):
    cost = IntegerField('Cost', validators=[DataRequired()])
    estimated_time = IntegerField('Estimated time in days', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    shipment_method_id = HiddenField()
    submit = SubmitField('Edit')
