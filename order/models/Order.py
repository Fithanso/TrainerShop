from application import db
from flask import url_for

from classes.abstract import Repository

from global_settings.models.GlobalSetting import GlobalSettingModelRepository
from products.models.Product import ProductModel
from shipment.models.ShipmentMethod import ShipmentMethodModel

from constants import BIGINT_MAX, BIGINT_LEN

from typing import List
import json
import random


class OrderModel(db.Model):
    __tablename__ = 'order'
    __table_args__ = {'extend_existing': True}  # added this because sqlalchemy was dropping an error. seems that
    # I shouldn't have created tables through pgAdmin, but using SqlAlchemy

    id = db.Column(db.BigInteger, primary_key=True)
    customer_id = db.Column(db.BigInteger())
    purchased_products = db.Column(db.JSON())
    order_datetime = db.Column(db.DateTime())
    received = db.Column(db.Boolean())
    shipment_method = db.Column(db.SmallInteger())
    boxes_content = db.Column(db.JSON())
    courier_id = db.Column(db.SmallInteger())
    customer_registered = db.Column(db.Boolean())
    recipient_name = db.Column(db.String())
    recipient_surname = db.Column(db.String())
    recipient_patronymic = db.Column(db.String())
    recipient_phone_number = db.Column(db.String())
    recipient_email = db.Column(db.String())
    delivery_address = db.Column(db.String())
    total_price = db.Column(db.Numeric(10, 4))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Order {self.__dict__}>"


class OrderModelRepository(Repository):
    model = OrderModel

    """Method generates unique id according to maximum integer possible and checks for duplicates in the table.
    """

    @staticmethod
    def create_id() -> int:

        max_int = BIGINT_MAX
        max_len = BIGINT_LEN

        rand_int = str(random.randrange(1, max_int))

        free_units = '1' * (max_len - len(rand_int))

        # to always maintain the same length
        unique_id = int(free_units + rand_int)

        #  if a product with the same id is found, then rerun function

        if OrderModelRepository.model.query.get(unique_id):
            OrderModelRepository.create_id()
        else:
            return unique_id
        return 0

    @staticmethod
    def get_orders_info_list(order_entities: List) -> List:
        """function iterates all order entities and extracts the information needed"""
        orders = []
        main_currency_sign = GlobalSettingModelRepository.get('main_currency_sign')

        # go through all orders and get information about them
        for order_entity in order_entities:
            purchased_products = json.loads(order_entity.purchased_products)

            products_rows = []
            for product_id, quantity in purchased_products.items():
                product_entity = ProductModel.query.get(int(product_id))

                product_row = {'product_id': product_id, 'product_name': product_entity.name, 'quantity': quantity}
                products_rows.append(product_row)

            shipment_method = ShipmentMethodModel.query.get(order_entity.shipment_method)

            shipment = 'Information about shipment is not available'
            if shipment_method:
                shipment = shipment_method.name + ': ' + str(shipment_method.cost) + ' ' + main_currency_sign

            order_dict = {'entity': order_entity, 'products': products_rows,
                          'total_price': str(order_entity.total_price) + ' ' + main_currency_sign,
                          'received': order_entity.received, 'shipment': shipment}

            orders.append(order_dict)

        return orders
