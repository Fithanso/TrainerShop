from app import app
import view
from products.blueprint import products
from account.blueprint import account
from admin_panel.blueprint import admin_panel
from categories.blueprint import categories
from characteristics.blueprint import characteristics
from global_settings.blueprint import global_settings

app.register_blueprint(products, url_prefix='/products')
app.register_blueprint(categories, url_prefix='/categories')
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(admin_panel, url_prefix='/admin')
app.register_blueprint(characteristics, url_prefix='/characteristics')
app.register_blueprint(global_settings, url_prefix='/global_settings')

if __name__ == '__main__':
    app.run(debug=True)





