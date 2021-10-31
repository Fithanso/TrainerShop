from flask import Blueprint, request, render_template
from app import db
from account.models.Customer import CustomerModel, CustomerModelRepository
from account.classes.COR import CustomerLoginHandler, AdminLoginHandler
from account.forms import *
from functions import *
from decorators import *
from datetime import datetime


account = Blueprint('account', __name__, template_folder='templates')


@account.route('/', methods=['GET'])
@unavailable_for_admin
@login_required
def index():

    form = EditAccountForm()

    return render_template('account/account.html', form=form)


@account.route('/validate-personal-data-edit/', methods=['POST'])
@unavailable_for_admin
@login_required
def validate_personal_data_edit():

    form = EditAccountForm()

    if form.validate_on_submit():
        data = request.form

        try:
           pass
        except Exception as e:
            return {"message": str(e)}

        return redirect(url_for('account.index'))


@account.route('/signup/', methods=['GET', 'POST'])
@unavailable_for_logged_customer
@unavailable_for_logged_admin
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
@unavailable_for_logged_admin
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


