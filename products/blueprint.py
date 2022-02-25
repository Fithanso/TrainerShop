from flask import *

from products.models.Product import *
from products.forms import *

from categories.models.Category import CategoryModel
from models.Characteristic import CharacteristicModel
from global_settings.models.GlobalSetting import *

from helpers import admin_logged, customer_logged, load_json_until_type, update_entity
from decorators import admin_only
from constants import ALLOWED_EXTENSIONS

from sqlalchemy import desc
from datetime import datetime
from werkzeug.utils import secure_filename
from uuid import uuid4
from typing import List
import json


products = Blueprint('products', __name__, template_folder='templates')


@products.route('/')
def display_all():

    product_entities = ProductModel.query.order_by(desc(ProductModel.creation_date)).all()
    products_list = prepare_products_for_display(product_entities)

    data_dict = {'products': products_list}

    if not product_entities:
        data_dict['error_message'] = 'No products found'

    if admin_logged():
        data_dict['add_to_cart_possible'] = False

    main_currency_sign = GlobalSettingModelRepository.get('main_currency_sign')

    data_dict['main_currency_sign'] = main_currency_sign

    return render_template('products/display_all_products.html', d=data_dict)


@products.route('/search/', methods=['GET'])
def search():

    search_query = request.args.get('search_product')

    data_dict = {}

    main_currency_sign = GlobalSettingModelRepository.get('main_currency_sign')

    data_dict['main_currency_sign'] = main_currency_sign

    if search_query.strip() == '':
        data_dict['error_message'] = 'Search query is empty'
    else:
        results_by_name = search_by_field('name', search_query)
        results_by_description = search_by_field('description', search_query)
        search_results = results_by_name + results_by_description

        if search_results:
            products_list = prepare_products_for_display(search_results)
            data_dict['products'] = products_list
        else:
            data_dict['error_message'] = 'No products found. Try another query'

    return render_template('products/display_all_products.html', d=data_dict)


def search_by_field(field, search_query) -> List:
    search_query = "%{}%".format(search_query)
    result_entities = ProductModel.query.filter(getattr(ProductModel, field).ilike(search_query)).all()
    return result_entities


def prepare_products_for_display(entities) -> List:
    # get values of global settings
    chunks = int(GlobalSettingModelRepository.get('products_in_row'))
    max_chars = int(GlobalSettingModelRepository.get('max_chars_on_product_card'))

    products_list = ProductModelRepository.prepare_list(entities, chunks, max_chars)
    return products_list


@products.route('/create/', methods=['GET'])
@admin_only
def create():
    form = CreateProductForm()
    main_currency_sign = GlobalSettingModelRepository.get('main_currency_sign')

    category_entities = CategoryModel.query.all()
    form.category.choices = [(c.short_name, c.name) for c in category_entities]
    form.price.render_kw = {"placeholder": main_currency_sign}

    return render_template('products/create_product.html', form=form)


@products.route('/create/', methods=['POST'])
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

        form_data = request.values
        # go through all data to find additional info - values of characteristics
        characteristics_fields = json.dumps(extract_characteristics(form_data))

        images = request.files.getlist("img_names")

        # check if extensions of all files are allowed
        images_valid = validate_images(images)

        upload_path = GlobalSettingModelRepository.get('uploads_path')
        img_necessary = GlobalSettingModelRepository.get('is_img_necessary_in_product')

        try:
            # if at least one image was loaded
            if images_valid:
                img_names = save_images(images, upload_path)
            else:
                # if some files are not allowed, return to a previous page according to a global setting
                if img_necessary == 'True':
                    return redirect(request.referrer)

            product_id = ProductModelRepository.create_id()
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            new_product = ProductModel(id=product_id, name=form_data['name'], description=form_data['description'],
                                       price=form_data['price'], pieces_left=form_data['pieces_left'],
                                       category=form_data['category'], characteristics=characteristics_fields,
                                       box_dimensions=form_data['box_dimensions'], weight=form_data['weight'],
                                       img_names=json.dumps(img_names), creation_date=date_time, last_edited=date_time)
            db.session.add(new_product)
            db.session.commit()

            flash('Product created successfully', category='success')

        except Exception as e:
            flash('Error occurred while creating a product', category='error')
            return {"message": str(e)}

        return redirect(url_for('products.display_all'))


@products.route('/<int:product_id>/', methods=['GET'])
def view(product_id):
    """Method prepares all product's data to be properly displayed."""
    product_entity = ProductModel.query.get(product_id)

    if not product_entity:
        abort(404)

    upload_path = GlobalSettingModelRepository.get('uploads_path')
    main_currency_sign = GlobalSettingModelRepository.get('main_currency_sign')

    product_images = get_image_paths(product_entity.img_names, upload_path)

    products_characteristics = get_characteristics(product_entity)

    # find a normal name for a category using a short name
    category = CategoryModel.query.filter(CategoryModel.short_name == product_entity.category).first()

    data_dict = {'characteristics': products_characteristics, 'product_images': product_images,
                 'category': category.short_name}

    if admin_logged():
        add_admin_info_into_dict(data_dict, product_entity)
        data_dict['add_to_cart_possible'] = False

    return render_template('products/view_product.html', d=data_dict, product=product_entity,
                           main_currency_sign=main_currency_sign)


def add_admin_info_into_dict(data_dict, product_entity):
    data_dict['admin_info'] = {}
    data_dict['admin_info']['product_id'] = product_entity.id
    data_dict['admin_info']['creation_date'] = product_entity.creation_date
    data_dict['admin_info']['last_edited'] = product_entity.last_edited

    return data_dict


def get_image_paths(img_names, upload_path):
    filenames = []
    for img_name in json.loads(img_names):
        # i add a system separator to make a path absolute, otherwise it'll search a 'static' folder inside products
        filenames.append(os.path.sep + os.path.join(upload_path) + img_name)

    return filenames


@products.route('/edit/<int:product_id>/', methods=['GET'])
@admin_only
def edit(product_id):

    product_entity = ProductModel.query.get(product_id)

    form = EditProductForm(data=product_entity.__dict__)

    # available choices are set before inserting data to this field
    # set available categories
    category_entities = CategoryModel.query.all()
    form.category.choices = [(c.short_name, c.name) for c in category_entities]

    # insert product's ID into a hidden field
    form.product_id.data = product_id

    # set a placeholder for currency
    main_currency_sign = GlobalSettingModelRepository.get('main_currency_sign')
    form.price.render_kw = {"placeholder": main_currency_sign}

    # get names of a product's characteristics:
    products_characteristics = get_characteristics(product_entity)

    # find a normal name for a category using a short name
    category = CategoryModel.query.filter(CategoryModel.short_name == product_entity.category).first()

    data_dict = {'characteristics': products_characteristics, 'category': category.name}

    return render_template('products/edit_product.html', d=data_dict, product=product_entity, form=form)


def get_characteristics(product_entity):
    product_entity.characteristics = load_json_until_type(product_entity.characteristics)

    characteristics = []
    if product_entity.characteristics:
        characteristics = get_characteristics_with_names(product_entity.characteristics)

    return characteristics


@products.route('/edit/', methods=['POST'])
@admin_only
def validate_edit():
    """
    Method edits a product
    """

    form = EditProductForm()

    if form.validate_on_submit():

        form_data = request.values

        product_id = int(form_data['product_id'])
        product_entity = ProductModel.query.get(product_id)

        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        extra_data = {'last_edited': date_time}

        upload_path = GlobalSettingModelRepository.get('uploads_path')

        images = request.files.getlist("img_names")
        # check if extensions of all files are allowed
        images_valid = validate_images(images)

        # this also checks if any file was sent. If nothing is sent, there is one empty FileStorage object with
        # unallowed extension. If no files were sent, old data will not be deleted
        if images_valid or not no_images(images):
            img_names = save_images(images, upload_path)
        else:
            # if some files are not allowed, return to a previous page
            # return redirect(request.referrer)
            img_names = []

        # get values of characteristics if there are some.
        new_characteristics = extract_characteristics(form_data)

        if new_characteristics:
            extra_data['characteristics'] = json.dumps(new_characteristics),

        if img_names:
            extra_data['img_names'] = json.dumps(img_names)

        data_to_update = {**form_data.to_dict(), **extra_data}

        update_entity(product_entity, data_to_update)

        db.session.commit()

        flash('Product successfully edited', category='success')

    return redirect(url_for('products.display_all'))


def save_images(images, upload_path):
    img_names = []
    for file in images:
        # save all files. each file gets a random name
        filename = str(uuid4()) + '.' + file.mimetype.split('/')[1]
        file.save(os.path.join(upload_path, filename))
        img_names.append(filename)

    return img_names


def no_images(img_files):
    """function returns true if there is only one empty entity and it's not of type image"""
    return len(img_files) == 1 and img_files[0].mimetype == 'application/octet-stream'


def validate_images(files) -> bool:
    """function checks if filenames are valid and allowed"""
    allowed_list = []
    for file in files:
        filename = file.filename
        if filename:
            file_extension = filename.rsplit('.', 1)[1].lower()
            allowed = '.' in filename and file_extension in ALLOWED_EXTENSIONS and secure_filename(filename)
            allowed_list.append(allowed)
        else:
            allowed_list.append(False)

    return all(allowed_list)


def get_characteristics_with_names(characteristics):
    characteristics_list = characteristics

    # go through all ids and replace id with a characteristic's name. This may not be an optimal approach
    # (too much requests to the DB)
    for list_item in characteristics_list:
        charc_id = list_item[0]
        entity = CharacteristicModel.query.get(charc_id)
        list_item[0] = entity.name

    return characteristics_list


def extract_characteristics(data) -> List:
    # characteristic fields always have a numeric key
    return [[key, value] for key, value in data.items() if key.isnumeric()]


@products.route('/delete/<int:product_id>/', methods=['GET'])
@admin_only
def delete(product_id):

    product_entity = ProductModel.query.get(product_id)
    db.session.delete(product_entity)
    db.session.commit()

    flash('Product deleted successfully', category='success')

    return redirect(url_for('products.display_all'))


