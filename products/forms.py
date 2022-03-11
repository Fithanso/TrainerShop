from wtforms import StringField, IntegerField, SelectField, SubmitField, MultipleFileField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed

from constants import ALLOWED_EXTENSIONS


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class CreateProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    pieces_left = IntegerField('Pieces left', validators=[DataRequired()])
    # I used my own class because I get "Not a valid choice" error every time
    category = NonValidatingSelectField('Category', render_kw={"id": "add_category_select"})
    box_dimensions = StringField('Box dimensions', validators=[DataRequired()],
                                 render_kw={"placeholder": "Length*width*height (mm.)"})
    box_weight = IntegerField('Box weight', validators=[DataRequired()], render_kw={"placeholder": "grams"})
    img_names = MultipleFileField('Select images', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')])
    submit = SubmitField('Create')


class EditProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    pieces_left = IntegerField('Pieces left', validators=[DataRequired()])
    # I used my own class because I get "Not a valid choice" error every time
    category = NonValidatingSelectField('Category', render_kw={"id": "edit_category_select"})
    box_dimensions = StringField('Box dimensions', validators=[DataRequired()], render_kw={"placeholder": "mm."})
    box_weight = IntegerField('Box weight', validators=[DataRequired()], render_kw={"placeholder": "grams"})
    img_names = MultipleFileField('Select images', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')])
    product_id = HiddenField()
    submit = SubmitField('Save')


