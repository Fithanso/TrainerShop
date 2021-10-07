from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from flask_wtf import FlaskForm


class CreateCategoryForm(FlaskForm):
    name = StringField('Name')
    short_name = StringField('Short name')
    submit = SubmitField('Create')


class EditCategoryForm(FlaskForm):
    characteristics = TextAreaField('Characteristics')
    category_id = HiddenField()
    submit = SubmitField('Edit')
