from wtforms import Form, StringField, TextAreaField, HiddenField, SubmitField
from flask_wtf import FlaskForm


class AddCategoryForm(FlaskForm):
    name = StringField('Name')
    short_name = StringField('Short name')


class EditCategoryForm(FlaskForm):
    characteristics = TextAreaField('Characteristics')
    category_id = HiddenField()
    submit = SubmitField('Rewrite')
