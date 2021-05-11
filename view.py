from app import app
from flask import render_template, request
from models import *


@app.route('/')
def index():
    name = 'Shop'
    navbar_links = {'account.signup': 'Sign up', 'account.login': 'Log in'}
    return render_template('index.html', n=name, navbar_links=navbar_links)

