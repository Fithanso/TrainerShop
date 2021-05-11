from flask import Blueprint, request, redirect, url_for, render_template, session
from models import *
from .forms import *
from helpers import *


account = Blueprint('account', __name__, template_folder='templates')


@account.route('/', methods=['GET'])
def index():
    if not session.get('client'):
        return redirect(url_for('account.login'))

    navbar_links = {'account.logout': 'Log out'}
    return render_template('account/account.html', navbar_links=navbar_links)


@account.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        form = SignupForm()
        navbar_links = {'account.signup': 'Sign up', 'account.login': 'Log in'}
        return render_template('account/signup.html', form=form, navbar_links=navbar_links)
    elif request.method == 'POST':
        data = request.form
        try:
            client_id = create_entry_id(ClientModel, 'bigint')
            encrypted_password = encrypt_sha1(data['password'])

            new_client = ClientModel(id=client_id, email=data['email'], password=encrypted_password)
            db.session.add(new_client)
            db.session.commit()
        except:
            return {"message": "Client creation failed"}
        return redirect(url_for('account.index'))


@account.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    navbar_links = {'account.signup': 'Sign up', 'account.login': 'Log in'}

    if request.method == 'GET':
        return render_template('account/login.html', form=form, navbar_links=navbar_links)
    elif request.method == 'POST':
        data = request.form
        client = ClientModel.query.filter(ClientModel.email == data['email']).first()

        if client and password_valid(client.password, data['password']):
            set_session_vars(client={'client_id': client.id})
            return redirect(url_for('account.index'))

        return render_template('account/login.html', form=form, er='Email or login is invalid',
                               navbar_links=navbar_links)


@account.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    return redirect(url_for('account.login'))


