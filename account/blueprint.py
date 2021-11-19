from flask import Blueprint, request, render_template
from app import db
from account.models.Customer import CustomerModel, CustomerModelRepository
from order.models.Order import OrderModel
from order.models.Order import OrderModelRepository
from account.classes.COR import CustomerLoginHandler, AdminLoginHandler
from account.classes.SearchAccount import AccountSearcher, SearchByName, SearchByPhoneNumber
from account.forms import *
from functions import *
from decorators import *
from datetime import datetime
from sqlalchemy import desc

account = Blueprint('account', __name__, template_folder='templates')


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

        return render_template('account/display_list.html', accounts=account_entities)
    else:
        return redirect(request.referrer)


@account.route('/', methods=['GET'])
@unavailable_for_admin
@login_required
def index():

    form = EditAccountForm()

    customer_entity = CustomerModel.query.get(int(session.get('customer')['customer_id']))

    insert_data_into_form(customer_entity, form, ('submit', 'csrf_token'))

    orders = []
    if customer_entity.orders:
        order_ids = customer_entity.orders.split(',')
        order_entities = OrderModel.query.filter(OrderModel.id.in_(order_ids)). \
            order_by(desc(OrderModel.order_datetime)).all()

        orders = OrderModelRepository.get_orders_info(order_entities)

    return render_template('account/account.html', form=form, orders=orders)


@account.route('/personal-data-edit/', methods=['POST'])
@unavailable_for_admin
@login_required
def personal_data_edit():

    form = EditAccountForm()
    if form.validate_on_submit():
        data = request.form

        try:
            customer_id = session.get('customer')['customer_id']
            customer_entity = CustomerModel.query.get(int(customer_id))

            extra_data = {'password': encrypt_sha1(data['password'])}
            update_entity(customer_entity, data, extra_data)

            db.session.commit()

        except Exception as e:
            return {"message": str(e)}

        return redirect(url_for('account.index'))


def update_entity(entity, data, extra_data):

    # assign new values

    attrs_list = [['login', 'name', 'surname', 'patronymic', 'phone_number', 'delivery_address', 'birthday'], ['password']]

    for attr in attrs_list[0]:
        # If no data was sent, old data will not be deleted
        if data[attr]:
            setattr(entity, attr, data[attr])

    for attr in attrs_list[1]:
        # If no data was sent, old data will not be deleted
        if extra_data[attr]:
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


