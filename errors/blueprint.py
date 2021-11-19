from flask import Blueprint, render_template, request

errors = Blueprint('errors', __name__, template_folder='templates')


@errors.app_errorhandler(403)
def handle_error_403(error):
    return render_template('errors/error_403.html'), 403


@errors.app_errorhandler(404)
def handle_error_404(error):
    return render_template('errors/error_404.html'), 404


@errors.app_errorhandler(405)
def handle_error_405(error):
    return render_template('errors/error_405.html'), 405







