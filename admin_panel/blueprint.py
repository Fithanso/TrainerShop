from flask import Blueprint, render_template
from categories.models.Category import CategoryModel
from global_settings.models.GlobalSetting import GlobalSettingModel
from decorators import *
from functions import get_navbar


admin_panel = Blueprint('admin_panel', __name__, template_folder='templates')


@admin_panel.route('/', methods=['GET'])
@admin_only
def index():

    panel_links = {'products.list': 'Products', 'products.create': 'Add product',
                   'admin_panel.list_categories': 'Categories', 'admin_panel.list_global_settings': 'Global settings'}
    return render_template('admin_panel/admin_index.html', panel_links=panel_links)


@admin_panel.route('/categories/', methods=['GET'])
@admin_only
def list_categories():

    categories_list = CategoryModel.query.all()
    data_dict = {'categories': categories_list}

    if len(categories_list) == 0:
        data_dict['message'] = 'No categories found'

    return render_template('admin_panel/admin_list_categories.html', d=data_dict)


@admin_panel.route('/global-settings/', methods=['GET'])
@admin_only
def list_global_settings():

    global_settings_list = GlobalSettingModel.query.all()
    data_dict = {'global_settings': global_settings_list}

    if len(global_settings_list) == 0:
        data_dict['message'] = 'No categories found'

    return render_template('admin_panel/admin_list_global_settings.html', d=data_dict)



