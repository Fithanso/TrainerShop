from app import *
import os
from flask import Blueprint, render_template, request, redirect, url_for
from products.models.Product import *
from functions import get_navbar, admin_logged, customer_logged
from global_settings.models.GlobalSetting import *
from cart.classes.GetCartProducts import GetCartProducts, GetCartFromCustomer, GetCartFromSession
from cart.classes.ChangeQuantityInCart import ChangeQuantityInCart, IncreaseInCustomer, IncreaseInSession, \
    DecreaseInCustomer, DecreaseInSession
from cart.classes.DeleteInCart import DeleteInCart, DeleteInCustomer, DeleteInSession

cart = Blueprint('cart', __name__, template_folder='templates')


@cart.route('/', methods=['GET'])
def index():
    if customer_logged():
        strategy = GetCartFromCustomer()
    else:
        strategy = GetCartFromSession()

    products_getter = GetCartProducts(strategy)
    products_quantity = products_getter.get_products()

    product_rows = []
    total_price = 0

    if products_quantity:
        for product_id, quantity in products_quantity.items():
            product_entity = ProductModel.query.get(int(product_id))
            product_rows.append({'product': product_entity, 'quantity': quantity,
                                 'row_price': product_entity.price * quantity})

            total_price += product_entity.price * quantity

    return render_template('cart/cart.html', product_rows=product_rows, total_price=total_price)


@cart.route('/increase-product-quantity/<product_id>', methods=['GET'])
def increase_product_quantity(product_id):
    """Operations of increase and decrease and strategies are separated because of a potential business logic inside"""

    if customer_logged():
        strategy = IncreaseInCustomer()
    else:
        strategy = IncreaseInSession()

    quantity_changer = ChangeQuantityInCart(strategy)
    quantity_changer.change_quantity(product_id)

    return redirect(request.referrer)


@cart.route('/decrease-product-quantity/<product_id>', methods=['GET'])
def decrease_product_quantity(product_id):

    if customer_logged():
        strategy = DecreaseInCustomer()
    else:
        strategy = DecreaseInSession()

    quantity_changer = ChangeQuantityInCart(strategy)
    quantity_changer.change_quantity(product_id)

    return redirect(request.referrer)


@cart.route('/delete-product/<product_id>', methods=['GET'])
def delete_product(product_id):

    if customer_logged():
        strategy = DeleteInCustomer()
    else:
        strategy = DeleteInSession()

    product_deleter = DeleteInCart(strategy)
    product_deleter.delete_product(product_id)

    return redirect(request.referrer)


