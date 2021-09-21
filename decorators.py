from flask import session, redirect, url_for
from functools import wraps


def admin_only(func):
    @wraps(func)  # wraps must be used for Python to track that not 'wrapper' function was called, but 'unav_for_admin'
    def wrapper(**kwargs):
        if not session.get('admin'):
            return redirect(url_for('index'))
        # parameters presence needs to be checked, because there might be parameters passed in url,
        # which will go through my decorator
        if kwargs:
            return func(**kwargs)
        else:
            return func()

    return wrapper


def unavailable_for_admin(func):
    @wraps(func)  # wraps must be used for Python to track that not 'wrapper' function was called, but 'unav_for_admin'
    def wrapper(**kwargs):
        if session.get('admin'):
            return redirect(url_for('admin_panel.admin'))
        # parameters presence needs to be checked, because there might be parameters passed in url,
        # which will go through my decorator
        if kwargs:
            return func(**kwargs)
        else:
            return func()

    return wrapper


def unavailable_for_logged_client(func):
    @wraps(func)
    def wrapper(**kwargs):
        if session.get('client'):
            return redirect(url_for('account.index'))
        # parameters presence needs to be checked, because there might be parameters passed in url,
        # which will go through my decorator
        if kwargs:
            return func(**kwargs)
        else:
            return func()

    return wrapper


'''redirects user to login page if he is not logged in'''


def login_required(func):
    @wraps(func)
    def wrapper(**kwargs):
        if not session.get('client') or not session.get('admin'):
            return func()
        return redirect(url_for('account.login'))

    return wrapper
