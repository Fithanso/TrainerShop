from flask import Blueprint, request, render_template
from .models.Customer import CustomerModel, CustomerModelRepository
from .classes.COR import CustomerLoginHandler, AdminLoginHandler
from .forms import *
from functions import *
from decorators import *


account = Blueprint('account', __name__, template_folder='templates')


@account.route('/', methods=['GET'])
@unavailable_for_admin
@login_required
def index():

    navbar_links = {'products.index': 'All products', 'account.logout': 'Log out'}
    return render_template('account/account.html', navbar_links=navbar_links)


@account.route('/signup', methods=['GET', 'POST'])
@unavailable_for_logged_client
def signup():

    if request.method == 'GET':
        form = SignupForm()
        navbar_links = {'account.signup': 'Sign up', 'account.login': 'Log in'}
        return render_template('account/signup.html', form=form, navbar_links=navbar_links)
    elif request.method == 'POST':
        data = request.form
        try:
            client_id = CustomerModelRepository.create_id()
            encrypted_password = encrypt_sha1(data['password'])

            new_client = CustomerModel(id=client_id, email=data['email'], password=encrypted_password)
            db.session.add(new_client)
            db.session.commit()
            set_session_vars(client={'client_id': new_client.id})
        except:
            return {"message": "Client creation failed"}
        return redirect(url_for('account.index'))


@account.route('/login', methods=['GET', 'POST'])
@unavailable_for_logged_client
def login():
    form = LoginForm()
    navbar_links = {'account.signup': 'Sign up', 'account.login': 'Log in'}

    if request.method == 'GET':
        return render_template('account/login.html', form=form, navbar_links=navbar_links)
    elif request.method == 'POST':
        data = request.form

        client_handler = CustomerLoginHandler()
        admin_handler = AdminLoginHandler()
        client_handler.set_next(admin_handler)

        result = client_handler.handle(data)

        if result:
            return result
        else:
            return render_template('account/login.html', form=form, er='Email or login is invalid',
                                   navbar_links=navbar_links)


@account.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('client', None)
    session['admin'] = None
    return redirect(url_for('account.login'))


