from flask import redirect, url_for
from typing import Any
from classes.abstract import AbstractHandler
from account.models.Customer import CustomerModel
from admin_panel.models.Admin import AdminModel
from functions import *


class CustomerLoginHandler(AbstractHandler):
    def handle(self, data: Any):

        client = CustomerModel.query.filter(CustomerModel.email == data['email']).first()

        if client:
            if password_valid(client.password, data['password']):
                set_session_vars(client={'client_id': client.id})
                return redirect(url_for('account.index'))
            else:
                return False
        else:
            return super().handle(data)


class AdminLoginHandler(AbstractHandler):
    def handle(self, data: Any):
        admin = AdminModel.query.filter(AdminModel.email == data['email']).first()

        if admin and admin.password == data['password']:
            set_session_vars(admin={'admin_id': admin.id})
            return redirect(url_for('admin_panel.admin'))
        return False


