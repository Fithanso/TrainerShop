from wtforms import StringField, HiddenField, SubmitField
from flask_wtf import FlaskForm


class CreateGlobalSettingForm(FlaskForm):
    name = StringField('Name')
    value = StringField('Value')
    submit = SubmitField('Create')


class EditGlobalSettingForm(FlaskForm):
    name = StringField('Name')
    value = StringField('Value')
    global_setting_id = HiddenField()
    submit = SubmitField('Save')
