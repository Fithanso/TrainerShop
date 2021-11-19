from flask import session
from app import db
from abc import ABC, abstractmethod
from account.models.Customer import CustomerModel
from functions import set_session_vars
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

    def delete_product(self, product_id) -> None:
        return self._strategy.delete_product(product_id)


class DeleteInCustomer(Strategy):
    def delete_product(self, product_id):
        customer_id = session.get('customer')['customer_id']
        customer_entity = CustomerModel.query.get(customer_id)

        # condition may be pointless, but I'll leave it anyway, in case the direct request is sent
        if customer_entity.active_cart is not None:
            cart_products = json.loads(customer_entity.active_cart)

            cart_products.pop(product_id, None)
            customer_entity.active_cart = json.dumps(cart_products)

            db.session.commit()


class DeleteInSession(Strategy):
    def delete_product(self, product_id):
        session_cart = session.get('active_cart')
        session_cart.pop(product_id, None)
        set_session_vars(active_cart=session_cart)

