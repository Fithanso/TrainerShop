import hashlib
from flask import session
import json


def load_json_until_type(obj, datatype=list):
    """sometimes object need to be loaded multiple times, and the function comes in handy"""
    while not isinstance(obj, datatype):
        obj = json.loads(obj)
    return obj


def json_load_multiple(obj, tries=2):
    for i in range(tries):
        obj = json.loads(obj)
    return obj


def encrypt_sha1(string) -> str:
    """Function encrypts the string using sha1 algorithm"""
    result = hashlib.sha1(string.encode()).hexdigest()
    return result


def password_valid(right, guess) -> bool:
    """Function checks if entered password matches the one from database"""
    return right == hashlib.sha1(guess.encode()).hexdigest()


def set_session_vars(**kwargs):
    """Function sets session variables"""
    for key, value in kwargs.items():
        session[key] = value


def del_session_vars(*args):
    """Function deletes session variables"""
    for key in args:
        session.pop(key, None)


def get_navbar() -> dict:
    """Function returns navbar links depending on who is logged in"""
    navbar_links = {'account.signup': 'Sign up', 'account.login': 'Log in', 'products.display_all': 'Products',
                    'categories.display_all': 'Categories', 'cart.index': 'My cart'}

    if session.get('admin'):
        del navbar_links['products.display_all']
        del navbar_links['categories.display_all']
        del navbar_links['cart.index']
        navbar_links['admin_panel.index'] = 'Dashboard'

    if session.get('customer'):
        navbar_links['account.index'] = 'Profile'

    if session.get('customer') or session.get('admin'):
        del navbar_links['account.login']
        del navbar_links['account.signup']
        navbar_links['account.logout'] = 'Log out'

    return navbar_links


def admin_logged() -> bool:
    """ Function checks if admin is logged in """
    if session.get('admin'):
        return True
    return False


def customer_logged() -> bool:
    """ Function checks if customer is logged in """
    if session.get('customer'):
        return True
    return False


def update_entity(entity, data):
    for attribute, value in data.items():
        setattr(entity, attribute, value)

    return entity


def nullify_empty_values_in_dict(data_dict):
    for key in data_dict:
        if data_dict[key] == '':
            data_dict[key] = None

    return data_dict


def to_int_if_fractional_zero(number):
    if float(number).is_integer():
        return int(number)

    return number
