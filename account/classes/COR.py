from flask import redirect, url_for
from classes.abstract import AbstractHandler

from account.models.Customer import CustomerModel

from admin_panel.models.Admin import AdminModel

from helpers import *

from typing import Any


class CustomerLoginHandler(AbstractHandler):
    def handle(self, data: Any):

        customer = CustomerModel.query.filter(CustomerModel.email == data['email']).first()

        if customer:
            if password_valid(customer.password, data['password']):
                set_session_vars(customer={'customer_id': customer.id})
                # active cart now means nothing since a customer is already logged in
                del_session_vars('active_cart')
                return redirect(url_for('index'))
            else:
                return False
        else:
            return super().handle(data)


class AdminLoginHandler(AbstractHandler):
    def handle(self, data: Any):
        admin_entity = AdminModel.query.filter(AdminModel.email == data['email']).first()

        if admin_entity and password_valid(admin_entity.password, data['password']):
            set_session_vars(admin={'admin_id': admin_entity.id})
            return redirect(url_for('admin_panel.index'))
        return False


