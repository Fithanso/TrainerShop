from app import db, BIGINT_MAX, BIGINT_LEN
from classes.abstract import Repository
from global_settings.models.GlobalSetting import GlobalSettingModelRepository
from products.models.Product import ProductModel
from shipment.models.ShipmentMethod import ShipmentMethodModel
import json
import random
import os
from typing import List


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
    total_price = db.Column(db.Integer())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Order {self.id}>"


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
    def prepare_list(entities, chunks, max_chars):
        """Method takes Product entities and makes them ready to be displayed. List of entities is splitted \
        into chunks, additional information about each is loaded"""

        # split all products into chunks of certain length - n. It is needed to display them in rows of n elements
        products_list = [entities[i:i + chunks] for i in range(0, len(entities), chunks)]

        upload_path = GlobalSettingModelRepository.get('uploads_path')

        # prepare icons for all loaded products (1 per product), crop descriptions to max chars possible
        for product in entities:
            filenames = json.loads(product.img_names)
            description = product.description[0:max_chars]

            if len(product.description) > max_chars:
                description += '...'

            if len(filenames) != 0:
                # i add a system separator to make a path absolute,
                # otherwise it'll search a 'static' folder inside products
                setattr(product, 'icon_path', os.path.sep + os.path.join(upload_path, filenames[0]))

            setattr(product, 'description', description)

        return products_list

    @staticmethod
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

            order_dict = {'entity': order_entity, 'products': products_rows,
                          'total_price': str(order_entity.total_price) + ' $',
                          'received': received, 'shipment': shipment}

            orders.append(order_dict)

        return orders
