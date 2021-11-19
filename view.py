from app import app
from flask import render_template, session, request, url_for
from functions import *
import random


@app.route('/')
def index():
    easter_egg = random.choices([0, 1], weights=(95, 5))[0]
    return render_template('index.html', easter_egg=easter_egg)


@app.context_processor
def navbar_processor():
    navbar_links = get_navbar()
    return {'navbar_links': navbar_links}


