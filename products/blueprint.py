from flask import Blueprint
from flask import render_template
from models import *


products = Blueprint('products', __name__, template_folder='templates')


@products.route('/')
def index():

    data_dict = {'products': ProductModel.query.all()}
    return render_template('products/products_list.html', d=data_dict)
