from app import *
import os
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from uuid import uuid4
from products.models.Product import *
from functions import get_navbar, admin_logged
from decorators import admin_only
from products.forms import *
from categories.models import Category
from characteristics.models import Characteristic
import json
from datetime import datetime

products = Blueprint('products', __name__, template_folder='templates')


def allowed_file(filename) -> bool:
    """function checks if a filename extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@products.route('/')
def list():

    navbar_links = get_navbar()
    entities = ProductModel.query.all()

    chunks = 3
    max_chars = 120

    products_list = ProductModelRepository.prepare_list(entities, chunks, max_chars)

    data_dict = {'products': products_list}

    if len(entities) == 0:
        data_dict['message'] = 'No products found'

    return render_template('products/list_products.html', d=data_dict, navbar_links=navbar_links)


@products.route('/create/', methods=['GET'])
@admin_only
def create():
    form = CreateProductForm()

    categories = Category.CategoryModel.query.all()
    form.category.choices = [(c.short_name, c.name) for c in categories]

    navbar_links = {'account.logout': 'Log out'}
    return render_template('products/create_product.html', navbar_links=navbar_links, form=form)


@products.route('/validate_create/', methods=['POST'])
@admin_only
def validate_create():
    """Method creates a new product. There were two options for me: 1) to store all necessary data inside an entity,
     eg. a normal name of a category, not a convenient short one, normal names of characteristics and etc.
     2) to store only the most necessary data. eg. short name of a category and indexes of characteristics.
     I have chosen the second one. So when a product is displayed, we need to make additional requests to the DB
     to get a beautiful data suitable for human (category name, characteristics names).
    """

    form = CreateProductForm()

    if form.validate_on_submit():

        data = request.values
        # go through all data to find additional info - values of characteristics. they always have a numeric key
        additional_fields = json.dumps([[key, value] for key, value in data.items() if key.isnumeric()])

        images = request.files.getlist("img_names")

        # check if extensions of all files are allowed
        allowed_extensions = [allowed_file(file.filename) and secure_filename(file.filename) for file in images]

        try:
            img_names = []
            if all(allowed_extensions):
                for file in images:
                    # save all files. each file gets a random name
                    filename = str(uuid4()) + '.' + file.mimetype.split('/')[1]
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    img_names.append(filename)
            # else:
            #     # if some files are not allowed, return to a previous page
            #     return redirect(request.referrer)

            product_id = ProductModelRepository.create_id()
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_product = ProductModel(id=product_id, name=data['name'], description=data['description'],
                                       price=data['price'], pieces_left=data['pieces_left'],
                                       category=data['category'], characteristics=additional_fields,
                                       box_dimensions=data['box_dimensions'], weight=data['weight'],
                                       img_names=json.dumps(img_names), creation_date=date_time, last_edited=date_time)
            db.session.add(new_product)
            db.session.commit()

        except Exception as e:
            return {"message": str(e)}

        return redirect(url_for('admin_panel.index'))


@products.route('/<product_id>/', methods=['GET'])
def view(product_id):
    """Method prepares all product's data to be properly displayed."""
    navbar_links = get_navbar()

    product = ProductModel.query.get(product_id)

    # get characteristics:
    characteristics = json.loads(product.characteristics)

    product_images = []
    for filename in json.loads(product.img_names):
        # i add a system separator to make a path absolute, otherwise it'll search a 'static' folder inside products
        product_images.append(os.path.sep + os.path.join(app.config['UPLOAD_FOLDER']) + filename)

    # go through all ids and replace id with a characteristic's name. This may not be an optimal approach
    # (too much requests to the DB)
    for list_item in characteristics:
        entity = Characteristic.CharacteristicModel.query.get(list_item[0])
        list_item[0] = entity.name

    # find a normal name for a category using a short name
    category = Category.CategoryModel.query.filter(Category.CategoryModel.short_name == product.category).first()

    data_dict = {'characteristics': characteristics, 'product_images': product_images, 'category': category.name}

    if admin_logged():
        data_dict['admin_info'] = {}
        data_dict['admin_info']['product_id'] = product.id
        data_dict['admin_info']['creation_date'] = product.creation_date
        data_dict['admin_info']['last_edited'] = product.last_edited

    return render_template('products/view_product.html', d=data_dict, navbar_links=navbar_links, product=product)


@products.route('/edit/<product_id>/', methods=['GET'])
@admin_only
def edit(product_id):

    navbar_links = get_navbar()

    # Take only fields needed
    form = EditProductForm()
    form_fields = form.__dict__['_fields']
    field_names = set(form_fields.keys())
    field_names.remove('submit')
    field_names.remove('csrf_token')
    field_names.remove('product_id')

    # take existing product's data
    product = ProductModel.query.get(product_id)
    product_data = product.__dict__

    # I need to set available choices before inserting data to this field
    categories = Category.CategoryModel.query.all()
    form.category.choices = [(c.short_name, c.name) for c in categories]

    for name in field_names:
        form_fields[name].data = product_data[name]

    # insert product's ID into a secret field
    form.product_id.data = product_id

    # get characteristics:
    characteristics = json.loads(product.characteristics)

    # go through all ids and replace id with a characteristic's name. This may not be an optimal approach
    # (too much requests to the DB)
    for list_item in characteristics:
        entity = Characteristic.CharacteristicModel.query.get(list_item[0])
        list_item[0] = entity.name

    # find a normal name for a category using a short name
    category = Category.CategoryModel.query.filter(Category.CategoryModel.short_name == product.category).first()

    data_dict = {'characteristics': characteristics, 'category': category.name,
                 'product_id': product.id, 'creation_date': product.creation_date,
                 'last_edited': product.last_edited}

    return render_template('products/edit_product.html', d=data_dict, navbar_links=navbar_links,
                           product=product, form=form)


@products.route('/validate_edit/', methods=['POST'])
@admin_only
def validate_edit():
    """
    Method edits a product
    """

    form = EditProductForm()

    if form.validate_on_submit():

        data = request.values
        # go through all data to find additional info - values of characteristics. they always have a numeric key
        additional_fields = json.dumps([[key, value] for key, value in data.items() if key.isnumeric()])

        images = request.files.getlist("img_names")

        # check if extensions of all files are allowed
        allowed_extensions = [allowed_file(file.filename) and secure_filename(file.filename) for file in images]

        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:

            img_names = []

            # this also checks if any file was sent. If nothing is sent, there is one empty FileStorage object with
            # unallowed extension. If no files were sent, old data will not be deleted
            if all(allowed_extensions):
                for file in images:
                    # save all files. each file gets a random name
                    filename = str(uuid4()) + '.' + file.mimetype.split('/')[1]
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    img_names.append(filename)
            # else:
            #     # if some files are not allowed, return to a previous page
            #     return redirect(request.referrer)

            product_id = data['product_id']
            entity = ProductModel.query.filter(ProductModel.id == product_id).first()
            # made to automatically assign new values excluding data which did not came directly through the form
            # (characteristics and images)
            attrs_list = ['name', 'description', 'price', 'pieces_left', 'category', 'box_dimensions', 'weight']

            for attr in attrs_list:
                setattr(entity, attr, data[attr])

            entity.characteristics = additional_fields
            entity.last_edited = date_time

            # If no files were sent, old data will not be deleted
            if img_names:
                entity.img_names = json.dumps(img_names)

            db.session.commit()

        except Exception as e:
            return {"message": str(e)}

        return redirect(url_for('admin_panel.index'))


@products.route('/delete/<product_id>/', methods=['GET'])
@admin_only
def delete(product_id):

    entity = ProductModel.query.get(product_id)
    db.session.delete(entity)
    db.session.commit()

    return redirect(url_for('admin_panel.index'))
