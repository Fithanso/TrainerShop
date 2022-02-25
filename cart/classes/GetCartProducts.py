from flask import session
from application import db
from abc import ABC, abstractmethod
from typing import Dict
from account.models.Customer import CustomerModel
import json


class Strategy(ABC):
    @abstractmethod
    def get_products(self):
        pass


class GetCartProducts:

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def get_products(self) -> Dict:
        return self._strategy.get_products()


class GetCartFromCustomer(Strategy):
    def get_products(self):
        customer_id = session.get('customer')['customer_id']
        customer_entity = CustomerModel.query.get(customer_id)

        if customer_entity.active_cart is not None:
            cart_products = json.loads(customer_entity.active_cart)
        else:
            cart_products = {}

        return cart_products


class GetCartFromSession(Strategy):
    def get_products(self):
        session_cart = session.get('active_cart')

        return session_cart






