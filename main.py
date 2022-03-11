from application import application
import view
from products.blueprint import products
from account.blueprint import account
from admin_panel.blueprint import admin_panel
from categories.blueprint import categories
from global_settings.blueprint import global_settings
from cart.blueprint import cart
from order.blueprint import order
from shipment.blueprint import shipment
from errors.blueprint import errors

application.register_blueprint(products, url_prefix='/products/')
application.register_blueprint(categories, url_prefix='/categories/')
application.register_blueprint(account, url_prefix='/account/')
application.register_blueprint(admin_panel, url_prefix='/admin/')
application.register_blueprint(global_settings, url_prefix='/global_settings/')
application.register_blueprint(cart, url_prefix='/cart/')
application.register_blueprint(order, url_prefix='/order/')
application.register_blueprint(shipment, url_prefix='/shipment/')
application.register_blueprint(errors, url_prefix='/errors/')

if __name__ == '__main__':
    application.run(debug=True)






