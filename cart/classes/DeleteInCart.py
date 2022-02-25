from flask import session
from application import db

from account.models.Customer import CustomerModel

from helpers import set_session_vars

from abc import ABC, abstractmethod
import json


class Strategy(ABC):
    @abstractmethod
    def delete_product(self, product_id):
        pass


class DeleteInCart:

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def delete_product(self, product_id: str) -> None:
        return self._strategy.delete_product(product_id)


class DeleteInCustomer(Strategy):

    def __init__(self, customer_entity):
        super().__init__()
        self.customer_entity = customer_entity

    def delete_product(self, product_id):

        # condition may be pointless, but I'll leave it anyway, in case the direct request is sent
        if self.customer_entity.active_cart is not None:
            cart_products = json.loads(self.customer_entity.active_cart)

            cart_products.pop(product_id, None)
            self.customer_entity.active_cart = json.dumps(cart_products)

            db.session.commit()


class DeleteInSession(Strategy):
    def delete_product(self, product_id):
        session_cart = session.get('active_cart')
        session_cart.pop(product_id, None)
        set_session_vars(active_cart=session_cart)

