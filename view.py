from app import app
from flask import render_template, session, request
from models import *
from functions import *


@app.route('/')
def index():
    name = 'Shop'
    navbar_links = get_navbar()

    return render_template('index.html', navbar_links=navbar_links)

