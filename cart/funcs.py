from flask import session

from cart.classes.EmptyCart import EmptyCart, EmptyInCustomer, EmptyInSession
from cart.classes.GetCartProducts import GetCartProducts, GetCartFromCustomer, GetCartFromSession

from account.models.Customer import CustomerModel

from helpers import customer_logged, load_json_until_type
import json


def empty_cart():
    if customer_logged():
        customer_entity = get_logged_in_customer()
        strategy = EmptyInCustomer(customer_entity)
    else:
        strategy = EmptyInSession()

    cart_deleter = EmptyCart(strategy)
    cart_deleter.delete_cart()


def get_logged_in_customer():
    customer_id = session.get('customer')['customer_id']
    customer_entity = CustomerModel.query.get(customer_id)

    return customer_entity


def product_exists_in_any_cart(customer_entity, product_id):
    if product_exists_in_session_cart(product_id) or product_exists_in_customers_cart(customer_entity, product_id):
        return True
    return False


def product_exists_in_session_cart(product_id):
    session_cart_dict = session.get('active_cart')
    if session_cart_dict is None or product_id not in session_cart_dict:
        return False

    return True


def product_exists_in_customers_cart(customer_entity, product_id):
    cart_products_dict = load_json_until_type(customer_entity.active_cart, dict)

    if cart_products_dict and product_id in cart_products_dict:
        return True
    return False


def customers_cart_is_valid(customer_entity):
    if customer_entity.active_cart is None or not customers_cart_is_dict(customer_entity):
        return False
    return True


def customers_cart_is_dict(customer_entity):
    if not isinstance(json.loads(customer_entity.active_cart), dict):
        return False
    return True


def get_products_quantities_dict():
    if customer_logged():
        strategy = GetCartFromCustomer()
    else:
        strategy = GetCartFromSession()

    products_getter = GetCartProducts(strategy)
    products_quantity = products_getter.get_products()

    return products_quantity


def get_session_cart_or_none():
    return session.get('active_cart')
