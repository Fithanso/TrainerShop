from app import *
from flask import Blueprint, render_template, request, redirect, url_for
from account.models.Customer import CustomerModel
from products.models.Product import ProductModel
from order.models.Order import OrderModel, OrderModelRepository
from order.classes.GetCartProducts import GetCartProducts, GetCartFromCustomer, GetCartFromSession
from order.classes.DeleteCart import DeleteCart, DeleteInCustomer, DeleteInSession
from shipment.models.ShipmentMethod import ShipmentMethodModel
from functions import customer_logged, insert_data_into_form
from order.forms import *
import json
from datetime import datetime

order = Blueprint('order', __name__, template_folder='templates')


@order.route('/create/', methods=['GET'])
def create():
    form = CreateOrderForm()

    if customer_logged():
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

    # load shipment options
    shipment_methods = ShipmentMethodModel.query.all()
    # make pairs of ids and names for each shipment method for select in form
    form.shipment_method.choices = [(s.id, s.name + ': ' + str(s.cost) + '$') for s in shipment_methods]

    if customer_logged():
        # insert existing data if customer is logged in
        customer_id = int(session.get('customer')['customer_id'])
        customer = CustomerModel.query.get(customer_id)

        #  insert existing data to form's fields
        form = insert_data_into_form(customer, form, ('submit', 'csrf_token', 'shipment_method', 'customer_id',
                                                      'purchased_products'))

        form.customer_id.data = customer_id

    return render_template('order/create.html', form=form)


@order.route('/create/', methods=['POST'])
def validate_create():
    form = CreateOrderForm()
    if form.validate_on_submit():

        empty_cart()

        data = request.values

        purchased_products = json.loads(data['purchased_products'])
        total_price = count_total_price(purchased_products)

        new_order_id = OrderModelRepository.create_id()

        order_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        shipment_method = ShipmentMethodModel.query.get(int(data['shipment_method']))
        total_price += shipment_method.cost

        boxes_content = json.dumps({'box1': 2, 'box2': 1})

        courier_id = 0

        customer_id = data['customer_id'] if data['customer_id'] else 0

        customer_registered = True if data['customer_id'] else False

        new_order = OrderModel(id=new_order_id, customer_id=customer_id,
                               purchased_products=data['purchased_products'], order_datetime=order_datetime,
                               received=False, shipment_method=int(data['shipment_method']),
                               boxes_content=boxes_content, courier_id=courier_id,
                               customer_registered=customer_registered, recipient_name=data['name'],
                               recipient_surname=data['surname'], recipient_patronymic=data['patronymic'],
                               recipient_phone_number=data['phone_number'], recipient_email=data['email'],
                               total_price=total_price
                               )

        # add new order to customer
        if customer_id != 0:
            add_order_to_customer(customer_id, new_order_id)

        db.session.add(new_order)
        db.session.commit()
    else:
        return redirect(url_for('index'))

    return redirect(url_for('order.success', order_id=new_order_id))


def empty_cart():
    if customer_logged():
        strategy = DeleteInCustomer()
    else:
        strategy = DeleteInSession()

    cart_deleter = DeleteCart(strategy)
    cart_deleter.delete_cart()


def count_total_price(purchased_products):
    total_price = 0
    for product_id, quantity in purchased_products.items():
        product = ProductModel.query.get(int(product_id))
        total_price += int(product.price) * int(quantity)

    return total_price


def add_order_to_customer(customer_id, new_order_id):
    customer = CustomerModel.query.get(customer_id)
    if customer.orders is None:
        customer.orders = str(new_order_id)
    else:
        customer.orders = str(customer.orders) + ', ' + str(new_order_id)


@order.route('/success/<order_id>')
def success(order_id):
    order_entity = OrderModel.query.get(order_id)
    if not order_entity:
        return redirect(url_for('index'))

    return render_template('order/success.html', order_id=order_id)
