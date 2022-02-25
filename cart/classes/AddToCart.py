from flask import session
from application import db

from account.models.Customer import CustomerModel

from helpers import set_session_vars

from abc import ABC, abstractmethod
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

    def add_product(self, product_id: str) -> None:
        return self._strategy.add_product(product_id)


class AddToCustomer(Strategy):

    def __init__(self, customer_entity):
        super().__init__()
        self.customer_entity = customer_entity

    def add_product(self, product_id):

        if self.customer_entity.active_cart is not None:
            cart_products = json.loads(self.customer_entity.active_cart)
        else:
            cart_products = {}

        cart_products[product_id] = 1

        self.customer_entity.active_cart = json.dumps(cart_products)
        db.session.commit()


class AddToSession(Strategy):

    def __init__(self, session_cart_dict):
        super().__init__()
        self.session_cart_dict = session_cart_dict

    def add_product(self, product_id):

        if self.session_cart_dict is not None:

            self.session_cart_dict[product_id] = 1
            # update session
            set_session_vars(active_cart=self.session_cart_dict)
        else:
            set_session_vars(active_cart={product_id: 1})








