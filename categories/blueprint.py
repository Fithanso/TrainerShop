from app import db
from flask import Blueprint, render_template, request, redirect, url_for
from categories.models.Category import CategoryModel, CategoryModelRepository
from models.Characteristic import CharacteristicModel, CharacteristicModelRepository
from products.models.Product import ProductModel, ProductModelRepository
from global_settings.models.GlobalSetting import GlobalSettingModelRepository
from decorators import admin_only
from categories.forms import *
import json

categories = Blueprint('categories', __name__, template_folder='templates')


def assemble_to_pairs(charcs) -> str:
    """
    Method takes list of objects and transforms them into text like this: (characteristic name:type, ...)
    """
    result = ''
    # "convert" objects into text to insert in textarea
    for item in charcs:
        unit = item.name + ':' + item.type + ', '
        result += unit
    return result


def assemble_to_list(charcs) -> list:
    """
    Method takes list of objects and transforms them into list of lists like this: (characteristic name,id,type)
    """

    result = []
    for item in charcs:
        result.append([item.name, str(item.id), item.type])
    return result


@categories.route('/<category_name>/', methods=['GET'])
def view(category_name):
    """ Method displays all products within a given category """

    category = CategoryModel.query.filter(CategoryModel.name == category_name).first()
    entities = ProductModel.query.filter(ProductModel.category == category.short_name).all()

    chunks = GlobalSettingModelRepository.get('products_in_row')
    chunks = int(chunks)
    max_chars = GlobalSettingModelRepository.get('max_chars_on_product_card')
    max_chars = int(max_chars)

    products_list = ProductModelRepository.prepare_list(entities, chunks, max_chars)

    data_dict = {'products': products_list}

    if len(entities) == 0:
        data_dict['message'] = 'No products found'

    return render_template('products/list_products.html', d=data_dict)


@categories.route('/')
def list():

    categories_list = CategoryModel.query.all()
    data_dict = {'categories': categories_list}

    if len(categories_list) == 0:
        data_dict['message'] = 'No categories found'

    return render_template('categories/list_categories.html', d=data_dict)


@categories.route('/create/', methods=['GET', 'POST'])
@admin_only
def create():
    form = CreateCategoryForm()

    if form.validate_on_submit():
        data = request.form

        try:
            category_id = CategoryModelRepository.create_id()
            new_category = CategoryModel(id=category_id, name=data['name'], short_name=data['short_name'])
            db.session.add(new_category)
            db.session.commit()
        except Exception as e:
            return {"message": str(e)}

        return redirect(url_for('admin_panel.list_categories'))

    return render_template('categories/create_category.html', form=form)


@categories.route('/edit/<category_id>/', methods=['GET'])
@admin_only
def edit(category_id):

    form = EditCategoryForm()

    # charcs = characteristics
    # find existing characteristics for the category and display them
    old_charcs = CharacteristicModel.query.filter(CharacteristicModel.category_id == category_id).all()
    textarea_content = assemble_to_pairs(old_charcs)

    # hidden field with category id
    form.category_id.data = category_id
    form.characteristics.data = textarea_content

    return render_template('categories/edit_category.html', form=form, category_id=category_id)


@categories.route('/edit_form_submit/', methods=['POST'])
@admin_only
def edit_form_submit():
    # if form was submitted to this address
    form = EditCategoryForm()
    data = request.values
    data_c = data['characteristics'].strip()
    if form.validate_on_submit():
        try:
            # find all characteristics assigned to a group
            all_existing = CharacteristicModel.query.filter(
                CharacteristicModel.category_id == data['category_id']).all()

            # if textarea is empty, delete all characteristics
            if not data_c:
                for obj in all_existing:
                    db.session.delete(obj)
                    db.session.commit()
            else:
                # if textarea is not empty
                if data_c[-1] == ',':
                    data_c = data_c[0: -1]
                new_pairs = data_c.split(',')
                new_pairs = [pair.strip().split(':') for pair in new_pairs]

                for pair in new_pairs:
                    c_name, c_type = pair
                    #  for each name from textarea check whether it already exists. if not, create a new one
                    existing_entity = CharacteristicModel.query.filter(
                        CharacteristicModel.category_id == data['category_id'],
                        CharacteristicModel.name == c_name,
                        CharacteristicModel.type == c_type).all()
                    if not existing_entity:
                        characteristic_id = CharacteristicModelRepository.create_id()
                        new_characteristic = CharacteristicModel(id=characteristic_id, name=c_name,
                                                                 category_id=data['category_id'], type=c_type)
                        db.session.add(new_characteristic)
                        db.session.commit()

                # delete items that are no more present in textarea (deleted by admin) from db
                for obj in all_existing:
                    if [obj.name, obj.type] not in new_pairs:
                        db.session.delete(obj)
                        db.session.commit()

        except Exception as e:
            return {"message": str(e)}

    return redirect(url_for('admin_panel.list_categories'))


@categories.route('/get_characteristics/<short_name>/', methods=['POST'])
@admin_only
def get_characteristics(short_name):
    """method collects all characteristics of one category"""

    category = CategoryModel.query.filter(CategoryModel.short_name == short_name).first()

    items = CharacteristicModel.query.filter(CharacteristicModel.category_id == category.id).all()
    result = assemble_to_list(items)
    return json.dumps(result)


@categories.route('/delete/<category_id>/', methods=['GET'])
@admin_only
def delete(category_id):
    entity = CategoryModel.query.get(category_id)
    db.session.delete(entity)
    db.session.commit()

    return redirect(url_for('admin_panel.list_categories'))








