
from application import db
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, get_flashed_messages

from categories.models.Category import CategoryModel, CategoryModelRepository
from categories.classes.Filter import FilterCreator, FilterApplier
from categories.forms import *

from models.Characteristic import CharacteristicModel, CharacteristicModelRepository
from products.models.Product import ProductModel, ProductModelRepository
from global_settings.models.GlobalSetting import GlobalSettingModelRepository

from decorators import admin_only

from typing import *
import json
import random

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

    filter_creator = FilterCreator(category_entity, request.args)
    filter_objects_list = filter_creator.get_filters()

    if not category_entity:
        abort(404)

    if len(request.args) > 0:
        product_entities = get_filtered_products(category_entity.short_name, request.args)
    else:
        product_entities = ProductModel.query.filter(ProductModel.category == category_entity.short_name).all()

    settings = get_global_settings()

    product_repository = ProductModelRepository()
    products_list = product_repository.prepare_list(
        product_entities, settings['chunks'], settings['max_chars'], settings['uploads_path']
    )

    data_dict = {'products': products_list, 'main_currency_sign': settings['main_currency_sign'],
                 'category_short_name': category_short_name}

    if not product_entities:
        data_dict['message'] = 'No products found'

    return render_template('categories/display_products_with_filters.html', d=data_dict, filters=filter_objects_list)


def get_global_settings():

    result_dict = {
        'chunks': int(GlobalSettingModelRepository.get('products_in_row')),
        'max_chars': int(GlobalSettingModelRepository.get('max_chars_on_product_card')),
        'main_currency_sign': GlobalSettingModelRepository.get('main_currency_sign'),
        'uploads_path': GlobalSettingModelRepository.get('uploads_path'),
    }

    return result_dict


def get_filtered_products(category_name, filter_multidict) -> List[ProductModel]:

    product_entities = ProductModel.query.filter(ProductModel.category == category_name).all()
    filters_dict = remove_word_from_dict_keys(filter_multidict)
    filter_applier = FilterApplier(product_entities, filters_dict)
    products_list = filter_applier.apply_filters()

    return products_list


def remove_word_from_dict_keys(input_dict):
    """Function leaves only filter's id and number"""
    result_dict = {}

    for key, value in input_dict.items():
        prefix, filter_id, filter_number = key.split("_")
        new_key = filter_id + "_" + filter_number
        result_dict[new_key] = value

    return result_dict


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
    category_entity = CategoryModel.query.get(category_id)
    existing_charcs_entities = category_entity.characteristics

    characteristics_name_type_pairs = make_name_type_pairs(existing_charcs_entities)

    form.category_id.data = category_id
    form.characteristics.data = characteristics_name_type_pairs

    return render_template('categories/edit_category.html', form=form, category_id=category_id)


def make_name_type_pairs(charcs) -> str:
    """
    Method takes list of objects and transforms them into text like this: (characteristic name:type, ...)
    """
    result = ''
    # "convert" objects into text to insert in textarea
    for item in charcs:
        unit = item.name.strip() + ':' + item.type + ', '
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

            name_type_pairs = arrange_charc_string_to_dict(characteristics_string)
            create_new_charcs_if_needed(name_type_pairs, form_data)

            # delete items that are no more present in textarea (deleted by admin) from db
            charcs_to_delete = get_removed_charcs(existing_charcs_entities, name_type_pairs)
            delete_characteristics(charcs_to_delete)

        flash('Category edited successfully', category='success')

    return redirect(url_for('admin_panel.display_all_categories'))


def characteristics_data_valid(characteristics_string):
    """function checks the string for overall correctness"""

    required_symbols = any(s in characteristics_string for s in [',', ':'])
    required_types = any(s in characteristics_string for s in ['boolean', 'integer', 'string'])

    if all((required_types, required_symbols)):
        return True

    return False


def get_removed_charcs(existing_charcs, name_type_pairs):
    return [charc for charc in existing_charcs if (charc.name, charc.type) not in name_type_pairs.items()]


def delete_characteristics(entities):
    for obj in entities:
        db.session.delete(obj)
        db.session.commit()


def arrange_charc_string_to_dict(characteristics_string):
    # cut unnecessary comma
    if characteristics_string[-1] == ',':
        characteristics_string = characteristics_string[: -1]

    name_type_pairs = {}
    # make a pair of characteristic's name and type
    for pair in characteristics_string.split(','):
        c_name, c_type = pair.split(':')
        if '' not in [c_name, c_type] and c_type in ['boolean', 'integer', 'string']:
            name_type_pairs[c_name.strip()] = c_type

    return name_type_pairs


def create_new_charcs_if_needed(name_type_pairs, form_data):
    for c_name, c_type in name_type_pairs.items():
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


@categories.route('/get_characteristics_values/<string:short_name>/<int:product_id>/', methods=['POST'])
@admin_only
def get_characteristics_with_values_for_js(short_name, product_id):
    """method is used only by JS"""

    return json.dumps(get_characteristics_with_values(short_name, product_id))


def get_characteristics_with_values(short_name, product_id):
    """method collects all possible characteristics of a product and values if there are some."""
    category_entity = CategoryModel.query.filter(CategoryModel.short_name == short_name).first()
    product_entity = ProductModel.query.get(product_id)
    values = json.loads(product_entity.characteristics)

    result_list = []

    for item in category_entity.characteristics:
        item.id = str(item.id)
        charc_value = values[item.id] if item.id in values else ''
        result_list.append({"charc_name": item.name, "charc_id": item.id,
                            "charc_type": item.type, "value": charc_value})

    return result_list


@categories.route('/get_characteristics/<string:short_name>/', methods=['POST'])
@admin_only
def get_characteristics_without_values_for_js(short_name):
    """method is used only by JS"""

    return json.dumps(get_characteristics_without_values(short_name))


def get_characteristics_without_values(short_name):

    """method collects all possible characteristics of a product"""

    category_entity = CategoryModel.query.filter(CategoryModel.short_name == short_name).first()

    result_list = []

    for item in category_entity.characteristics:
        item.id = str(item.id)
        result_list.append({"charc_name": item.name, "charc_id": item.id,
                            "charc_type": item.type})

    return result_list


@categories.route('/delete/<int:category_id>/', methods=['GET'])
@admin_only
def delete(category_id):
    category_entity = CategoryModel.query.get(category_id)
    db.session.delete(category_entity)
    db.session.commit()

    flash('Category was deleted', category='success')

    return redirect(url_for('admin_panel.display_all_categories'))








