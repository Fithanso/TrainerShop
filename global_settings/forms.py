from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class CreateGlobalSettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Create')


class EditGlobalSettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])
    global_setting_id = HiddenField()
    submit = SubmitField('Save')
