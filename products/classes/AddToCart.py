from flask import session
from app import db
from abc import ABC, abstractmethod
from typing import List
from account.models.Customer import CustomerModel
from functions import set_session_vars
import json


class Strategy(ABC):
    @abstractmethod
    def add_product(self, product_id):
        pass


class AddToCart:

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def add_product(self, product_id) -> None:
        return self._strategy.add_product(product_id)


class AddToCustomer(Strategy):
    def add_product(self, product_id):
        customer_id = session.get('customer')['customer_id']
        customer = CustomerModel.query.get(customer_id)

        if customer.active_cart is not None:
            cart_products = json.loads(customer.active_cart)
        else:
            cart_products = {}

        if product_id in cart_products:
            cart_products[product_id] = int(cart_products[product_id]) + 1
        else:
            cart_products[product_id] = 1

        customer.active_cart = json.dumps(cart_products)
        db.session.commit()


class AddToSession(Strategy):
    def add_product(self, product_id):

        session_cart = session.get('active_cart')

        if session_cart is not None:
            if product_id in session_cart:
                session_cart[product_id] = session_cart[product_id] + 1
            else:
                session_cart[product_id] = 1
            # update session
            set_session_vars(active_cart=session_cart)
        else:
            set_session_vars(active_cart={product_id: 1})








