from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class CreateCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    short_name = StringField('Short name', validators=[DataRequired()])
    submit = SubmitField('Create')


class EditCategoryForm(FlaskForm):
    characteristics = TextAreaField('Characteristics')
    category_id = HiddenField()
    submit = SubmitField('Edit')
