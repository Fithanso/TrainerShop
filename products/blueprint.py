from app import db
from flask import Blueprint, render_template, request, redirect, url_for
from products.models.Product import *
from functions import get_navbar
from decorators import admin_only
from products.forms import *
from categories.models import Category
import json

products = Blueprint('products', __name__, template_folder='templates')


@products.route('/')
def index():

    navbar_links = get_navbar()
    data_dict = {'products': ProductModel.query.all()}

    return render_template('products/products_list.html', d=data_dict, navbar_links=navbar_links)


@products.route('/add', methods=['GET'])
@admin_only
def add():

    form = AddProductForm()
    categories = Category.CategoryModel.query.all()
    form.category.choices = [(c.short_name, c.name) for c in categories]
    navbar_links = {'account.logout': 'Log out'}
    return render_template('products/add_product.html', navbar_links=navbar_links, form=form)


@products.route('/add_form_submit', methods=['POST'])
def add_form_submit():
    # if form was submitted to this address
    data = request.values
    print(data)

    # go through all data to find additional info - values of characteristics. they always have a numeric key
    additional = json.dumps([[key, value] for key, value in data.items() if key.isnumeric()])

    print(additional)
    try:
        if data:
            product_id = ProductModelRepository.create_id()
            new_product = ProductModel(id=product_id, name=data['name'], description=data['description'],
                                       price=data['price'], pieces_left=data['pieces_left'],
                                       category=data['category'], specifications=additional,
                                       box_dimensions=data['box_dimensions'], weight=data['weight'],
                                       img_paths=data['img_paths'])
            db.session.add(new_product)
            db.session.commit()

    except Exception as e:
        return {"message": str(e)}

    return redirect(url_for('admin_panel.admin'))

