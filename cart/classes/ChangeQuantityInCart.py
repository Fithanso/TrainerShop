from flask import session
from app import db
from abc import ABC, abstractmethod
from account.models.Customer import CustomerModel
from functions import set_session_vars
import json


class Strategy(ABC):
    @abstractmethod
    def change_quantity(self, product_id):
        pass


class ChangeQuantityInCart:

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def change_quantity(self, product_id) -> None:
        return self._strategy.change_quantity(product_id)


class IncreaseInCustomer(Strategy):
    def change_quantity(self, product_id):
        customer_id = session.get('customer')['customer_id']
        customer = CustomerModel.query.get(customer_id)

        # condition may be pointless, but I'll leave it anyway, in case the direct request is sent
        if customer.active_cart is not None:
            cart_products = json.loads(customer.active_cart)

            cart_products[product_id] += 1
            customer.active_cart = json.dumps(cart_products)

            db.session.commit()


class IncreaseInSession(Strategy):
    def change_quantity(self, product_id):
        session_cart = session.get('active_cart')
        session_cart[product_id] += 1
        set_session_vars(active_cart=session_cart)


class DecreaseInCustomer(Strategy):
    def change_quantity(self, product_id):
        customer_id = session.get('customer')['customer_id']
        customer = CustomerModel.query.get(customer_id)

        # condition may be pointless, but I'll leave it anyway, in case the direct request is sent
        if customer.active_cart is not None:
            cart_products = json.loads(customer.active_cart)

            cart_products[product_id] -= 1
            customer.active_cart = json.dumps(cart_products)

            db.session.commit()


class DecreaseInSession(Strategy):
    def change_quantity(self, product_id):
        session_cart = session.get('active_cart')
        session_cart[product_id] -= 1
        set_session_vars(active_cart=session_cart)






