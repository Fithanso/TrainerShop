from application import *
from flask import Blueprint, render_template, request, redirect, url_for

from order.classes.GetCartProducts import GetCartProducts, GetCartFromCustomer, GetCartFromSession
from order.classes.SearchOrder import OrderSearcher, SearchById, SearchByName, SearchByPhoneNumber
from order.models.Order import OrderModel, OrderModelRepository
from order.forms import *

from account.models.Customer import CustomerModel
from products.models.Product import ProductModel
from shipment.models.ShipmentMethod import ShipmentMethodModel
from global_settings.models.GlobalSetting import *

from helpers import customer_logged, to_int_if_fractional_zero
from cart.funcs import empty_cart
from decorators import admin_only

from datetime import datetime
from typing import List
import json


order = Blueprint('order', __name__, template_folder='templates')


@order.route('/<string:order_id>', methods=['GET'])
def view(order_id):

    order_entity = OrderModel.query.get(order_id)
    if not order_entity:
        abort(404)

    order_info = OrderModelRepository.get_orders_info_list([order_entity])[0]
    return render_template('order/view_order.html', order=order_info)


@order.route('/search/', methods=['GET', 'POST'])
@admin_only
def search():
    form = SearchOrderForm()

    if form.validate_on_submit():
        form_data = request.values

        strategy = None
        search_query = None
        orders_list = []

        if form_data['order_id']:
            strategy = SearchById()
            search_query = form_data['order_id']
        elif form_data['customer_phone_number']:
            strategy = SearchByPhoneNumber()
            search_query = form_data['customer_phone_number']
        elif form_data['customer_name']:
            strategy = SearchByName()
            search_query = form_data['customer_name']

        order_entities = OrderSearcher(strategy).search(search_query)

        if order_entities:
            orders_list = OrderModelRepository.get_orders_info_list(order_entities)

        return render_template('order/display_found_orders.html', orders_list=orders_list)

    return render_template('order/search_order.html', form=form)


@order.route('/create/', methods=['GET'])
def create():
    form = CreateOrderForm()

    if customer_logged():
        # insert existing data if customer is logged in
        customer_id = int(session.get('customer')['customer_id'])
        customer_entity = CustomerModel.query.get(customer_id)

        #  insert existing data to form's fields
        form = CreateOrderForm(data=customer_entity.__dict__)
        form.customer_id.data = customer_id

        strategy = GetCartFromCustomer()

    else:
        strategy = GetCartFromSession()

    products_getter = GetCartProducts(strategy)
    products_quantity = products_getter.get_products()

    # redirect away, if cart was empty
    if not products_quantity:
        return redirect(url_for('cart.index'))

    # insert info about products that are in cart
    form.purchased_products.data = json.dumps(products_quantity)

    shipment_methods = load_shipment_methods()

    form.shipment_method.choices = shipment_methods

    return render_template('order/create_order.html', form=form)


def load_shipment_methods() -> List:
    shipment_method_entities = ShipmentMethodModel.query.all()
    main_currency_sign = GlobalSettingModelRepository.get('main_currency_sign')

    # make pairs of ids and names for each shipment method for select in form
    shipment_methods = []
    for s in shipment_method_entities:
        shipment_info = s.name + ': ' + str(s.cost) + main_currency_sign + ' - ' + str(s.estimated_time) + ' days'
        shipment_method_item = (s.id,  shipment_info)
        shipment_methods.append(shipment_method_item)
    return shipment_methods


@order.route('/create/', methods=['POST'])
def validate_create():
    form = CreateOrderForm()
    if form.validate_on_submit():

        form_data = request.values

        purchased_products = json.loads(form_data['purchased_products'])
        decrease_pieces_left(purchased_products)
        total_price = count_total_price(purchased_products)

        new_order_id = OrderModelRepository.create_id()

        order_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        shipment_method_entity = ShipmentMethodModel.query.get(int(form_data['shipment_method']))
        total_price += shipment_method_entity.cost

        boxes_content = json.dumps({'box1': 2, 'box2': 1})

        courier_id = 0

        customer_id = form_data['customer_id'] if form_data['customer_id'] else 0

        customer_registered = True if form_data['customer_id'] else False

        new_order = OrderModel(id=new_order_id, customer_id=customer_id,
                               purchased_products=form_data['purchased_products'], order_datetime=order_datetime,
                               received=False, shipment_method=int(form_data['shipment_method']),
                               boxes_content=boxes_content, courier_id=courier_id,
                               customer_registered=customer_registered, recipient_name=form_data['name'],
                               recipient_surname=form_data['surname'], recipient_patronymic=form_data['patronymic'],
                               recipient_phone_number=form_data['phone_number'], recipient_email=form_data['email'],
                               delivery_address=form_data['delivery_address'], total_price=total_price
                               )

        # add new order to customer
        if customer_id != 0:
            add_order_to_customer(customer_id, new_order_id)

        db.session.add(new_order)
        db.session.commit()

        empty_cart()
    else:
        return redirect(url_for('index'))

    return redirect(url_for('order.success', order_id=new_order_id))


def decrease_pieces_left(product_ids):
    for product_id, quantity in product_ids.items():
        product_entity = ProductModel.query.get(product_id)
        product_entity.pieces_left -= quantity

    db.session.commit()


def count_total_price(purchased_products):
    total_price = 0
    for product_id, quantity in purchased_products.items():
        product_entity = ProductModel.query.get(int(product_id))
        total_price += float(product_entity.price) * int(quantity)

    total_price = to_int_if_fractional_zero(total_price)
    return total_price


def add_order_to_customer(customer_id, new_order_id):
    customer_entity = CustomerModel.query.get(customer_id)
    if customer_entity.orders is None:
        customer_entity.orders = str(new_order_id)
    else:
        customer_entity.orders = str(customer_entity.orders) + ', ' + str(new_order_id)


@order.route('/success/<int:order_id>')
def success(order_id):
    order_entity = OrderModel.query.get(order_id)
    if not order_entity:
        return redirect(url_for('index'))

    return render_template('order/order_success.html', order_id=order_id)
