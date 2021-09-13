from flask import Blueprint, render_template, request
from models import *
from functions import *
from .models.Category import CategoryModel, CategoryModelRepository
from characteristics.models.Characteristic import CharacteristicModel, CharacteristicModelRepository
from decorators import *
from categories.forms import *


categories = Blueprint('categories', __name__, template_folder='templates')


@categories.route('/')
@admin_only
def index():

    navbar_links = get_navbar()
    data_dict = {'categories': CategoryModel.query.all()}

    return render_template('categories/categories_list.html', d=data_dict, navbar_links=navbar_links)


@categories.route('/add', methods=['GET', 'POST'])
@admin_only
def add():

    if request.method == 'GET':
        form = AddCategoryForm()

        navbar_links = {'account.logout': 'Log out'}
        return render_template('categories/add_category.html', navbar_links=navbar_links, form=form)
    elif request.method == 'POST':
        data = request.form

        try:
            category_id = CategoryModelRepository.create_id()
            new_category = CategoryModel(id=category_id, name=data['name'], short_name=data['short_name'])
            db.session.add(new_category)
            db.session.commit()
        except Exception as e:
            return {"message": str(e)}

        return redirect(url_for('admin_panel.admin'))


def assemble_characteristics(charcs):
    result = ''
    # "convert" objects into text to insert in textarea
    for item in charcs:
        unit = item.name + ':' + item.type + ', '
        result += unit
    return result


@categories.route('/edit', methods=['GET', 'POST'])
@admin_only
def edit():

    form = EditCategoryForm()

    if request.method == 'GET':
        navbar_links = get_navbar()
        category_id = request.args.get('id')

        # charcs = characteristics
        # find existing characteristics for the category and display them
        old_charcs = CharacteristicModel.query.filter(CharacteristicModel.category_id == category_id).all()
        textarea_content = assemble_characteristics(old_charcs)

        # hidden field with category id
        form.category_id.data = category_id
        form.characteristics.data = textarea_content

    # if form was submitted to this address
    if form.validate_on_submit():
        data = request.values
        data_c = data['characteristics'].strip()
        try:

            # if textarea is not empty
            if data_c:
                if data_c[-1] == ',':
                    data_c = data_c[0: -1]
                pairs = data_c.split(',')
                for pair in pairs:
                    pair = pair.strip()
                    c_name, c_type = pair.split(':')
                    #  for each name from textarea check whether it already exists. if not, add a new one
                    existing = CharacteristicModel.query.filter(
                        CharacteristicModel.category_id == data['category_id'],
                        CharacteristicModel.name == c_name).all()
                    if not existing:
                        characteristic_id = CharacteristicModelRepository.create_id()
                        new_characteristic = CharacteristicModel(id=characteristic_id, name=c_name,
                                                                 category_id=data['category_id'], type=c_type)
                        db.session.add(new_characteristic)
                        db.session.commit()

        except Exception as e:
            return {"message": str(e)}

        return redirect(url_for('categories.index'))

    return render_template('categories/edit_category.html', navbar_links=navbar_links, form=form)





