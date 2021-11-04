from flask import Blueprint, request, render_template
from app import db
from account.models.Customer import CustomerModel, CustomerModelRepository
from order.models.Order import OrderModel
from shipment.models.ShipmentMethod import ShipmentMethodModel
from products.models.Product import ProductModel
from account.classes.COR import CustomerLoginHandler, AdminLoginHandler
from account.forms import *
from functions import *
from decorators import *
from datetime import datetime
from sqlalchemy import desc
from typing import List
import json

account = Blueprint('account', __name__, template_folder='templates')


@account.route('/', methods=['GET'])
@unavailable_for_admin
@login_required
def index():

    form = EditAccountForm()

    customer = CustomerModel.query.get(int(session.get('customer')['customer_id']))

    insert_data_into_form(customer, form, ('submit', 'csrf_token'))

    orders = []
    if customer.orders:
        order_ids = customer.orders.split(',')
        order_entities = OrderModel.query.filter(OrderModel.id.in_(order_ids)). \
            order_by(desc(OrderModel.order_datetime)).all()

        orders = get_orders_info(order_entities)

    return render_template('account/account.html', form=form, orders=orders)


def get_orders_info(order_entities) -> List:
    """function iterates all order entities and extracts the information needed"""
    orders = []

    # go through all orders and get information about them
    for order_entity in order_entities:
        purchased_products = json.loads(order_entity.purchased_products)

        products_rows = ''
        for product_id, quantity in purchased_products.items():
            product_entity = ProductModel.query.get(int(product_id))

            product_row = product_entity.name + ': ' + str(quantity) + '<br>'

            products_rows += product_row

            if not order_entity.received:
                received = '<p style="color: red">Not received</p>'
            else:
                received = '<p style="color: green">Received</p>'

        shipment_method_entity = ShipmentMethodModel.query.get(order_entity.shipment_method)
        s = shipment_method_entity
        shipment = s.name + ': ' + str(s.cost) + '$'

        order_dict = {'id': int(order_entity.id), 'products': products_rows,
                      'total_price': str(order_entity.total_price) + ' $',
                      'datetime': order_entity.order_datetime, 'received': received, 'shipment': shipment}

        orders.append(order_dict)

    return orders


@account.route('/validate-personal-data-edit/', methods=['POST'])
@unavailable_for_admin
@login_required
def validate_personal_data_edit():

    form = EditAccountForm()
    if form.validate_on_submit():
        data = request.form

        try:
            print(data)
            customer_id = session.get('customer')['customer_id']
            customer_entity = CustomerModel.query.get(int(customer_id))

            extra_data = {'password': encrypt_sha1(data['password'])}
            customer_entity = update_entity(customer_entity, data, extra_data)

            db.session.commit()

        except Exception as e:
            return {"message": str(e)}

        return redirect(url_for('account.index'))


def update_entity(entity, data, extra_data):

    # assign new values

    attrs_list = [['login', 'name', 'surname', 'patronymic', 'delivery_address', 'birthday'], ['password',]]

    for attr in attrs_list[0]:
        # If no data was sent, old data will not be deleted
        print(attr)
        print(data[attr])
        if data[attr]:
            print(attr)
            setattr(entity, attr, data[attr])

    for attr in attrs_list[1]:
        # If no data was sent, old data will not be deleted
        print(attr)
        print(extra_data[attr])
        if extra_data[attr]:
            print(attr)
            setattr(entity, attr, extra_data[attr])

    return entity


@account.route('/signup/', methods=['GET', 'POST'])
@unavailable_for_logged_customer
@unavailable_for_admin
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        data = request.form
        try:
            customer_id = CustomerModelRepository.create_id()
            encrypted_password = encrypt_sha1(data['password'])
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_customer = CustomerModel(id=customer_id, email=data['email'], password=encrypted_password,
                                         register_date=date_time)
            db.session.add(new_customer)
            db.session.commit()
            set_session_vars(customer={'customer_id': new_customer.id})
        except:
            return {"message": "customer creation failed"}
        return redirect(url_for('account.index'))

    return render_template('account/signup.html', form=form)


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
            return render_template('account/login.html', form=form, er='Email or login is invalid')

    return render_template('account/login.html', form=form)


@account.route('/logout/', methods=['GET'])
@login_required
def logout():
    session.pop('customer', None)
    session['admin'] = None
    return redirect(url_for('index'))


