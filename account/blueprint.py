import json

from flask import Blueprint, request, render_template
from application import db
from sqlalchemy import desc

from account.models.Customer import CustomerModel, CustomerModelRepository
from account.classes.COR import CustomerLoginHandler, AdminLoginHandler
from account.classes.SearchAccount import AccountSearcher, SearchByName, SearchByPhoneNumber
from account.forms import *
from account.funcs import *

from order.models.Order import OrderModel, OrderModelRepository

from decorators import *
from helpers import update_entity

from datetime import datetime

account = Blueprint('account', __name__, template_folder='templates')


@account.route('/', methods=['GET'])
@unavailable_for_admin
@login_required
def index():

    customer_entity = CustomerModel.query.get(int(session.get('customer')['customer_id']))

    form = EditAccountForm(data=customer_entity.__dict__)

    order_ids = []
    if customer_entity.orders:
        # reverse because the last order's id should be on top
        order_ids = reversed([order_id.strip() for order_id in customer_entity.orders.split(',')])

    return render_template('account/account.html', form=form, order_ids=order_ids)


@account.route('/personal-data-edit/', methods=['POST'])
@unavailable_for_admin
@login_required
def personal_data_edit():

    form = EditAccountForm()
    if form.validate_on_submit():

        data_dict = get_edited_personal_data(request.form)
        customer_entity = get_customer_from_session()

        update_entity(customer_entity, data_dict)
        db.session.commit()

        return redirect(url_for('account.index'))


@account.route('/signup/', methods=['GET', 'POST'])
@unavailable_for_logged_customer
@unavailable_for_admin
def signup():
    form = SignupForm()

    error_message = ""

    if form.validate_on_submit():
        data = request.form

        existing_customer = CustomerModel.query.filter(CustomerModel.email == data['email']).first()

        if existing_customer is None:
            customer_id = CustomerModelRepository.create_id()
            encrypted_password = encrypt_sha1(data['password'])
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            active_cart = json.dumps({})
            new_customer = CustomerModel(id=customer_id, email=data['email'], password=encrypted_password,
                                         register_date=date_time, active_cart=active_cart)
            db.session.add(new_customer)
            db.session.commit()
            set_session_vars(customer={'customer_id': new_customer.id})

            return redirect(url_for('account.index'))
        else:
            error_message = "Email already exists"

    return render_template('account/signup.html', form=form, error_message=error_message)


@account.route('/login/', methods=['GET', 'POST'])
@unavailable_for_logged_customer
@unavailable_for_admin
def login():
    """Operation of login is implemented using C-o-R pattern. Customers and admins can log in using just one form."""
    form = LoginForm()

    if form.validate_on_submit():
        data = request.form

        customer_handler = CustomerLoginHandler()
        admin_handler = AdminLoginHandler()
        customer_handler.set_next(admin_handler)

        result = customer_handler.handle(data)

        if result:
            return result
        else:
            return render_template('account/login.html', form=form, error_message='Email or login is invalid')

    return render_template('account/login.html', form=form)


@account.route('/logout/', methods=['GET'])
@login_required
def logout():
    session.pop('customer', None)
    session['admin'] = None
    return redirect(url_for('index'))


@account.route('/search/', methods=['GET'])
@admin_only
def search():
    form = SearchAccountForm()

    return render_template('account/search.html', form=form)


@account.route('/val_search/', methods=['POST'])
@admin_only
def validate_search():
    form = SearchAccountForm()

    if form.validate_on_submit():
        data = request.values

        strategy = None
        search_query = None

        if data['customer_phone_number']:
            strategy = SearchByPhoneNumber()
            search_query = data['customer_phone_number']
        elif data['customer_name']:
            strategy = SearchByName()
            search_query = data['customer_name']

        account_entities = AccountSearcher(strategy).search(search_query)

        for entity in account_entities:
            entity.orders = reversed([order_id.strip() for order_id in entity.orders.split(',')])

        return render_template('account/display_found_accounts.html', accounts=account_entities)
    else:
        return redirect(request.referrer)

