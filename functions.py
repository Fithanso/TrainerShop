import hashlib
from flask import session
from flask_wtf import FlaskForm
import json


def json_load(obj, datatype=list):
    """sometimes object need to be loaded multiple times, and the function comes in handy"""
    while not isinstance(obj, datatype):
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
    navbar_links = {'account.signup': 'Sign up', 'account.login': 'Log in', 'products.list': 'Products',
                    'categories.list': 'Categories', 'cart.index': 'My cart'}

    if session.get('admin'):
        del navbar_links['products.list']
        del navbar_links['categories.list']
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


def insert_data_into_form(entity, form, exclude=()) -> FlaskForm:
    entity_data = entity.__dict__
    form_fields = form.__dict__['_fields']

    # take only fields needed, exclude other
    field_names = set(form_fields.keys())

    for name in exclude:
        field_names.remove(name)

    for name in field_names:
        form_fields[name].data = entity_data[name]

    return form


