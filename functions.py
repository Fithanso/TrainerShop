import hashlib
from flask import session


"""Function encrypts the string using sha1 algorithm"""


def encrypt_sha1(string):
    result = hashlib.sha1(string.encode()).hexdigest()
    return result


"""Function checks if entered password matches the one from database"""


def password_valid(right, guess):
    return right == hashlib.sha1(guess.encode()).hexdigest()


"""Function sets session variables"""


def set_session_vars(**kwargs):
    for key, value in kwargs.items():
        session[key] = value

"""Function returns navbar links"""


def get_navbar():
    navbar_links = {'account.signup': 'Sign up', 'account.login': 'Log in', 'products.index': 'All products'}

    if session.get('client') or session.get('admin'):
        del navbar_links['account.login']
        del navbar_links['account.signup']
        navbar_links['account.logout'] = 'Log out'

    return navbar_links


