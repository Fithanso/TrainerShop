from application import db
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, get_flashed_messages

from categories.models.Category import CategoryModel, CategoryModelRepository
from categories.forms import *

from models.Characteristic import CharacteristicModel, CharacteristicModelRepository
from products.models.Product import ProductModel, ProductModelRepository
from global_settings.models.GlobalSetting import GlobalSettingModelRepository

from decorators import admin_only

import json

categories = Blueprint('categories', __name__, template_folder='templates')


@categories.route('/')
def display_all():

    categories_entities = CategoryModel.query.all()
    data_dict = {'categories': categories_entities}

    if not categories_entities:
        data_dict['message'] = 'No categories found'

    return render_template('categories/display_all_categories.html', d=data_dict)


@categories.route('/<string:category_short_name>/', methods=['GET'])
def view(category_short_name):
    """ Method displays all products within a given category """
    category_entity = CategoryModel.query.filter(CategoryModel.short_name == category_short_name).first()

    if not category_entity:
        abort(404)

    product_entities = ProductModel.query.filter(ProductModel.category == category_entity.short_name).all()

    chunks = int(GlobalSettingModelRepository.get('products_in_row'))
    max_chars = int(GlobalSettingModelRepository.get('max_chars_on_product_card'))
    main_currency_sign = GlobalSettingModelRepository.get('main_currency_sign')

    products_list = ProductModelRepository.prepare_list(product_entities, chunks, max_chars)

    data_dict = {'products': products_list, 'main_currency_sign': main_currency_sign}

    if not product_entities:
        data_dict['message'] = 'No products found'

    return render_template('products/display_all_products.html', d=data_dict)


@categories.route('/create/', methods=['GET', 'POST'])
@admin_only
def create():
    form = CreateCategoryForm()

    if form.validate_on_submit():
        data = request.form

        category_id = CategoryModelRepository.create_id()
        new_category = CategoryModel(id=category_id, name=data['name'], short_name=data['short_name'])
        db.session.add(new_category)
        db.session.commit()

        flash('Category created successfully', category='success')

        return redirect(url_for('admin_panel.display_all_categories'))

    return render_template('categories/create_category.html', form=form)


@categories.route('/edit/<int:category_id>/', methods=['GET'])
@admin_only
def edit(category_id):

    form = EditCategoryForm()

    # charcs = characteristics
    # find existing characteristics for the category and display them
    category_entity = CategoryModel.query.get(category_id)
    existing_charcs_entities = category_entity.characteristics

    characteristics_data = assemble_objects_to_pairs(existing_charcs_entities)

    # hidden field with category id
    form.category_id.data = category_id
    form.characteristics.data = characteristics_data

    return render_template('categories/edit_category.html', form=form, category_id=category_id)


def assemble_objects_to_pairs(charcs) -> str:
    """
    Method takes list of objects and transforms them into text like this: (characteristic name:type, ...)
    """
    result = ''
    # "convert" objects into text to insert in textarea
    for item in charcs:
        unit = item.name + ':' + item.type + ', '
        result += unit
    return result


@categories.route('/edit/', methods=['POST'])
@admin_only
def validate_edit():
    # if form was submitted to this address
    form = EditCategoryForm()

    if form.validate_on_submit():
        form_data = request.values
        characteristics_string = form_data['characteristics'].strip()

        if not characteristics_data_valid(characteristics_string):
            return redirect(request.referrer)

        # find all characteristics assigned to a group
        existing_charcs_entities = CharacteristicModel.query.filter(
            CharacteristicModel.category_id == form_data['category_id']).all()

        # if textarea is empty, delete all characteristics
        if not characteristics_string:
            delete_characteristics(existing_charcs_entities)
        else:

            name_type_pairs = arrange_string_to_pairs(characteristics_string)
            create_new_charcs_if_needed(name_type_pairs, form_data)

            # delete items that are no more present in textarea (deleted by admin) from db
            charcs_to_delete = [obj for obj in existing_charcs_entities
                                if [obj.name, obj.type] not in name_type_pairs]
            delete_characteristics(charcs_to_delete)

        flash('Category edited successfully', category='success')

    return redirect(url_for('admin_panel.display_all_categories'))


def characteristics_data_valid(characteristics_string):
    """function checks the string for overall correctness"""
    required_symbols = any(s in characteristics_string for s in [',', ':'])
    required_types = any(s in characteristics_string for s in ['boolean', 'integer', 'string'])

    if not all((required_types, required_symbols)):
        return False

    return True


def delete_characteristics(entities):
    for obj in entities:
        db.session.delete(obj)
        db.session.commit()


def arrange_string_to_pairs(characteristics_string):
    # cut unnecessary comma
    if characteristics_string[-1] == ',':
        characteristics_string = characteristics_string[0: -1]

    name_type_pairs = []
    # make a pair of characteristic's name and type
    for pair in characteristics_string.split(','):
        pair_list = [str(pair_item).strip() for pair_item in pair.split(':')]
        if '' not in pair_list and pair_list[1] in ['boolean', 'integer', 'string']:
            name_type_pairs.append(pair_list)

    return name_type_pairs


def create_new_charcs_if_needed(name_type_pairs, form_data):
    for pair in name_type_pairs:
        c_name, c_type = pair
        #  for each name from textarea check whether it already exists. if not, create a new one
        existing_entity = CharacteristicModel.query.filter(
            CharacteristicModel.category_id == form_data['category_id'],
            CharacteristicModel.name == c_name,
            CharacteristicModel.type == c_type).all()
        if not existing_entity:
            characteristic_id = CharacteristicModelRepository.create_id()
            new_characteristic = CharacteristicModel(id=characteristic_id, name=c_name,
                                                     category_id=form_data['category_id'], type=c_type)
            db.session.add(new_characteristic)
            db.session.commit()


@categories.route('/get_characteristics/<string:short_name>/', methods=['POST'])
@admin_only
def get_characteristics(short_name):
    """method collects all characteristics of one category"""

    category_entity = CategoryModel.query.filter(CategoryModel.short_name == short_name).first()
    result_list = assemble_objects_to_list(category_entity.characteristics)

    return json.dumps(result_list)


def assemble_objects_to_list(charcs) -> list:
    """
    Method takes list of objects and transforms them into list of lists like this: (characteristic name,id,type)
    """

    result = []
    for item in charcs:
        result.append([item.name, str(item.id), item.type])
    return result


@categories.route('/delete/<int:category_id>/', methods=['GET'])
@admin_only
def delete(category_id):
    category_entity = CategoryModel.query.get(category_id)
    db.session.delete(category_entity)
    db.session.commit()

    flash('Category was deleted', category='success')

    return redirect(url_for('admin_panel.display_all_categories'))








