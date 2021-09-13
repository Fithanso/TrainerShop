from flask import Blueprint, render_template
from decorators import *

admin_panel = Blueprint('admin_panel', __name__, template_folder='templates')


@admin_panel.route('/', methods=['GET'])
@admin_only
def admin():

    navbar_links = {'account.logout': 'Log out'}
    panel_links = {'products.index': 'Products', 'products.add': 'Add product',  'categories.index': 'Categories'}
    return render_template('admin_panel/admin_index.html', navbar_links=navbar_links, panel_links=panel_links)


