from flask import Blueprint, render_template, request
from models import *
from functions import *
from decorators import *
from products.forms import *
from categories.models import Category


products = Blueprint('products', __name__, template_folder='templates')


@products.route('/')
def index():

    navbar_links = get_navbar()
    data_dict = {'products': ProductModel.query.all()}

    return render_template('products/products_list.html', d=data_dict, navbar_links=navbar_links)


@products.route('/add', methods=['GET', 'POST'])
@admin_only
def add():

    if request.method == 'GET':
        form = AddProductForm()
        categories = Category.CategoryModel.query.all()
        form.category.choices = [(c.short_name, c.name) for c in categories]
        navbar_links = {'account.logout': 'Log out'}
        return render_template('products/add_product.html', navbar_links=navbar_links, form=form)




