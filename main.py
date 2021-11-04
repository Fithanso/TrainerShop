from app import app
import view
from products.blueprint import products
from account.blueprint import account
from admin_panel.blueprint import admin_panel
from categories.blueprint import categories
from global_settings.blueprint import global_settings
from cart.blueprint import cart
from order.blueprint import order
from shipment.blueprint import shipment

app.register_blueprint(products, url_prefix='/products/')
app.register_blueprint(categories, url_prefix='/categories/')
app.register_blueprint(account, url_prefix='/account/')
app.register_blueprint(admin_panel, url_prefix='/admin/')
app.register_blueprint(global_settings, url_prefix='/global_settings/')
app.register_blueprint(cart, url_prefix='/cart/')
app.register_blueprint(order, url_prefix='/order/')
app.register_blueprint(shipment, url_prefix='/shipment/')

if __name__ == '__main__':
    app.run(debug=True)




