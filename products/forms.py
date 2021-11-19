from app import ALLOWED_EXTENSIONS
from wtforms import StringField, IntegerField, SelectField, SubmitField, MultipleFileField, HiddenField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class CreateProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()], render_kw={"placeholder": "$"})
    pieces_left = IntegerField('Pieces left', validators=[DataRequired()])
    # I used my own class because I get "Not a valid choice" error every time
    category = NonValidatingSelectField('Category')
    box_dimensions = StringField('Box dimensions', validators=[DataRequired()],
                                 render_kw={"placeholder": "Length*width*height (mm.)"})
    weight = IntegerField('Box weight', validators=[DataRequired()], render_kw={"placeholder": "grams"})
    img_names = MultipleFileField('Select images', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')])
    submit = SubmitField('Create')


class EditProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()], render_kw={"placeholder": "$"})
    pieces_left = IntegerField('Pieces left', validators=[DataRequired()])
    # I used my own class because I get "Not a valid choice" error every time
    category = NonValidatingSelectField('Category')
    box_dimensions = StringField('Box dimensions', validators=[DataRequired()], render_kw={"placeholder": "mm."})
    weight = IntegerField('Weight', validators=[DataRequired()], render_kw={"placeholder": "grams"})
    img_names = MultipleFileField('Select images', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')])
    product_id = HiddenField()
    submit = SubmitField('Save')


