from app import *
from flask import Blueprint, render_template, request, redirect, url_for
from products.models.Product import *
from decorators import unavailable_for_admin
from functions import customer_logged
from global_settings.models.GlobalSetting import *
from cart.classes.GetCartProducts import GetCartProducts, GetCartFromCustomer, GetCartFromSession
from cart.classes.ChangeQuantityInCart import ChangeQuantityInCart, IncreaseInCustomer, IncreaseInSession, \
    DecreaseInCustomer, DecreaseInSession
from cart.classes.DeleteInCart import DeleteInCart, DeleteInCustomer, DeleteInSession

cart = Blueprint('cart', __name__, template_folder='templates')


@cart.route('/', methods=['GET'])
@unavailable_for_admin
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
            if product_entity:
                product_rows.append({'product': product_entity, 'quantity': quantity,
                                     'row_price': product_entity.price * quantity})

                total_price += product_entity.price * quantity
            else:
                # Product may be already deleted
                return redirect(url_for('cart.delete_product', product_id=product_id))

    return render_template('cart/cart.html', product_rows=product_rows, total_price=total_price)


@cart.route('/increase-product-quantity/<product_id>', methods=['GET'])
@unavailable_for_admin
def increase_product_quantity(product_id):
    """Operations of increase and decrease and strategies are separated because of a potential business logic inside"""

    if customer_logged():
        strategy = IncreaseInCustomer()
    else:
        strategy = IncreaseInSession()

    quantity_changer = ChangeQuantityInCart(strategy)
    quantity_changer.change_quantity(product_id)

    return redirect(url_for('cart.index'))


@cart.route('/decrease-product-quantity/<product_id>', methods=['GET'])
@unavailable_for_admin
def decrease_product_quantity(product_id):

    if customer_logged():
        strategy = DecreaseInCustomer()
    else:
        strategy = DecreaseInSession()

    quantity_changer = ChangeQuantityInCart(strategy)
    new_quantity = quantity_changer.change_quantity(product_id)

    if new_quantity == 0:
        return redirect(url_for('cart.delete_product', product_id=product_id))

    return redirect(url_for('cart.index'))


@cart.route('/delete-product/<product_id>', methods=['GET'])
@unavailable_for_admin
def delete_product(product_id):

    if customer_logged():
        strategy = DeleteInCustomer()
    else:
        strategy = DeleteInSession()

    product_deleter = DeleteInCart(strategy)
    product_deleter.delete_product(product_id)

    return redirect(url_for('cart.index'))


