from flask import *
from application import db
from abc import ABC, abstractmethod

from helpers import set_session_vars

import json


class Strategy(ABC):
    @abstractmethod
    def change_quantity(self, product_id):
        pass


class ChangeQuantityInCart:

    DECREASE = 'decrease'
    INCREASE = 'increase'

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def change_quantity(self, product_id: str) -> int:
        return self._strategy.change_quantity(product_id)


class IncreaseInCustomer(Strategy):
    def __init__(self, customer_entity):
        super().__init__()
        self.customer_entity = customer_entity

    def change_quantity(self, product_id):
        cart_products = json.loads(self.customer_entity.active_cart)

        cart_products[product_id] += 1
        self.customer_entity.active_cart = json.dumps(cart_products)

        db.session.commit()
        return cart_products[product_id]


class IncreaseInSession(Strategy):

    def __init__(self, session_cart_dict):
        super().__init__()
        self.session_cart_dict = session_cart_dict

    def change_quantity(self, product_id):

        self.session_cart_dict[product_id] += 1
        set_session_vars(active_cart=self.session_cart_dict)

        return self.session_cart_dict[product_id]


class DecreaseInCustomer(Strategy):

    def __init__(self, customer_entity):
        super().__init__()
        self.customer_entity = customer_entity

    def change_quantity(self, product_id):

        cart_products = json.loads(self.customer_entity.active_cart)

        cart_products[product_id] -= 1
        self.customer_entity.active_cart = json.dumps(cart_products)

        db.session.commit()
        return cart_products[product_id]


class DecreaseInSession(Strategy):

    def __init__(self, session_cart_dict):
        super().__init__()
        self.session_cart_dict = session_cart_dict

    def change_quantity(self, product_id):
        self.session_cart_dict[product_id] -= 1
        set_session_vars(active_cart=self.session_cart_dict)

        return self.session_cart_dict[product_id]
