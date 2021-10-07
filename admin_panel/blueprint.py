from flask import Blueprint, render_template
from categories.models.Category import CategoryModel
from decorators import *
from functions import get_navbar


admin_panel = Blueprint('admin_panel', __name__, template_folder='templates')


@admin_panel.route('/', methods=['GET'])
@admin_only
def index():

    navbar_links = {'account.logout': 'Log out'}
    panel_links = {'products.list': 'Products', 'products.create': 'Add product',
                   'admin_panel.list_categories': 'Categories'}
    return render_template('admin_panel/admin_index.html', navbar_links=navbar_links, panel_links=panel_links)


@admin_panel.route('/categories/', methods=['GET'])
@admin_only
def list_categories():

    navbar_links = get_navbar()
    data_dict = {'categories': CategoryModel.query.all()}

    if len(CategoryModel.query.all()) == 0:
        data_dict['message'] = 'No categories found'

    return render_template('admin_panel/admin_list_categories.html', d=data_dict, navbar_links=navbar_links)

