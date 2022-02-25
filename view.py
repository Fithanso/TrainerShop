from application import application
from flask import render_template, session, request, url_for
from helpers import *
import random


@application.route('/')
def index():
    easter_egg = random.choices([0, 1], weights=(95, 5))[0]
    return render_template('index.html', easter_egg=easter_egg)


@application.context_processor
def navbar_processor():
    navbar_links = get_navbar()
    return {'navbar_links': navbar_links}


