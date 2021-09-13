from wtforms import Form, StringField, IntegerField, SelectField, FieldList


class AddProductForm(Form):
    name = StringField('Name')
    description = StringField('Description')
    price = IntegerField('Price')
    pieces_left = IntegerField('Pieces left')
    category = SelectField('Category', coerce=str)
    box_dimensions = StringField('Box dimensions')
    weight = IntegerField('Weight')
    img_paths = StringField('Paths to images')
