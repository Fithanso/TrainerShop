from flask import request, session

from account.models.Customer import CustomerModel

from helpers import *


def get_edited_personal_data(form_data) -> dict:
    data_dict = form_data.to_dict()
    data_dict['password'] = encrypt_sha1(data_dict['password'])
    data_dict = nullify_empty_values_in_dict(data_dict)

    return data_dict


def get_customer_from_session() -> CustomerModel:

    customer_id = int(session.get('customer')['customer_id'])
    customer_entity = CustomerModel.query.get(customer_id)

    return customer_entity
