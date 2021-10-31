from app import app
from flask import render_template, session, request
from functions import *


@app.route('/')
def index():
    name = 'Shop'
    navbar_links = get_navbar()

    return render_template('index.html')


@app.context_processor
def navbar_processor():
    navbar_links = get_navbar()

    return {'navbar_links': navbar_links}

