from flask import Blueprint, render_template, request
from flask_wtf.csrf import CSRFError

from application import application

import logging

logging.basicConfig(filename='record.log', level=logging.ERROR,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

errors = Blueprint('errors', __name__, template_folder='templates')


@errors.app_errorhandler(400)
def handle_error_400(error):
    return render_template('errors/error_400.html'), 400


@errors.app_errorhandler(401)
def handle_error_401(error):
    return render_template('errors/error_401.html'), 401


@errors.app_errorhandler(403)
def handle_error_403(error):
    return render_template('errors/error_403.html'), 403


@errors.app_errorhandler(404)
def handle_error_404(error):
    return render_template('errors/error_404.html'), 404


@errors.app_errorhandler(405)
def handle_error_405(error):
    return render_template('errors/error_405.html'), 405


@errors.app_errorhandler(501)
def handle_error_501(error):
    return render_template('errors/error_501.html'), 501


@errors.app_errorhandler(CSRFError)
def handle_csrf_error(error):
    return render_template('errors/csrf_error.html', reason=error.description), 404







