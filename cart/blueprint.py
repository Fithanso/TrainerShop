from application import *
from flask import *

from cart.classes.DeleteInCart import *
from cart.classes.ChangeQuantityInCart import ChangeQuantityInCart
from cart.classes.QuantityManager import QuantityManager
from cart.classes.CartValidator import CartValidator
from cart.classes.AddToCartManager import AddToCartManager
from cart.funcs import *

from products.models.Product import *
from global_settings.models.GlobalSetting import *

from decorators import unavailable_for_admin
from helpers import customer_logged, to_int_if_fractional_zero

cart = Blueprint('cart', __name__, template_folder='templates')


@cart.route('/', methods=['GET'])
@unavailable_for_admin
def index():

    products_quantities = get_products_quantities_dict()

    main_currency_sign = GlobalSettingModelRepository.get('main_currency_sign')

    product_rows = []
    total_price = 0

    if products_quantities:

        for product_id, quantity in products_quantities.items():
            product_entity = ProductModel.query.get(int(product_id))

            if not product_entity:
                # If product in cart is deleted
                return redirect(url_for('cart.delete_product', product_id=product_id))

            product_price = to_int_if_fractional_zero(product_entity.price)

            if int(quantity) > int(product_entity.pieces_left):
                quantity = product_entity.pieces_left
                flash('The number of some added products has been reduced', category='warning')

            product_row_dict = {'product': product_entity, 'quantity': quantity,
                                'row_price':  product_price * quantity}

            product_rows.append(product_row_dict)

            total_price += product_price * quantity

    return render_template('cart/cart.html', product_rows=product_rows,
                           total_price=total_price, main_currency_sign=main_currency_sign)


@cart.route('/add-to-cart/<string:product_id>/', methods=['GET'])
def add_to_cart(product_id):
    cart_validator = CartValidator()
    add_manager = AddToCartManager(product_id)

    if customer_logged():
        if not cart_validator.validate_logged_customers_cart():
            return redirect(url_for('cart.index'))

    status = add_manager.add_product_return_status()

    if status == AddToCartManager.PRODUCT_ALREADY_IN_CART:
        return redirect(url_for('cart.increase_product_quantity', product_id=product_id))

    # redirect back to product's page
    return redirect(request.referrer)


@cart.route('/increase-product-quantity/<string:product_id>', methods=['GET'])
@unavailable_for_admin
def increase_product_quantity(product_id):
    cart_validator = CartValidator()

    if not cart_validator.validate_cart_with_product(product_id):
        return redirect(url_for('cart.index'))

    quantity_manager = QuantityManager(ChangeQuantityInCart.INCREASE, product_id)

    status = quantity_manager.change_quantity_return_status()

    if status == QuantityManager.QUANTITY_EXCEEDS_PIECES_LEFT:
        flash('Not enough product in stock', category='warning')

    return redirect(request.referrer)


@cart.route('/decrease-product-quantity/<string:product_id>', methods=['GET'])
@unavailable_for_admin
def decrease_product_quantity(product_id):

    cart_validator = CartValidator()

    if not cart_validator.validate_cart_with_product(product_id):
        return redirect(url_for('cart.index'))

    quantity_manager = QuantityManager(ChangeQuantityInCart.DECREASE, product_id)

    status = quantity_manager.change_quantity_return_status()

    if status == QuantityManager.QUANTITY_IS_NULL:
        return redirect(url_for('cart.delete_product', product_id=product_id))

    return redirect(request.referrer)


@cart.route('/delete-product/<string:product_id>', methods=['GET'])
@unavailable_for_admin
def delete_product(product_id):
    if customer_logged():
        customer_entity = get_logged_in_customer()
        if customer_entity.active_cart is None:
            return redirect(url_for('cart.index'))
        strategy = DeleteInCustomer(customer_entity)
    else:
        strategy = DeleteInSession()

    product_deleter = DeleteInCart(strategy)
    product_deleter.delete_product(product_id)

    return redirect(url_for('cart.index'))
