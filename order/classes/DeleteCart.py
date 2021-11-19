from flask import session
from app import db
from abc import ABC, abstractmethod
from account.models.Customer import CustomerModel
from functions import del_session_vars
import json


class Strategy(ABC):
    @abstractmethod
    def delete_cart(self):
        pass


class DeleteCart:

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def delete_cart(self) -> None:
        return self._strategy.delete_cart()


class DeleteInCustomer(Strategy):
    def delete_cart(self):
        customer_id = session.get('customer')['customer_id']
        customer_entity = CustomerModel.query.get(customer_id)

        # condition may be pointless, but I'll leave it anyway, in case the direct request is sent
        if customer_entity.active_cart is not None:
            empty_cart = {}
            customer_entity.active_cart = json.dumps(empty_cart)

            db.session.commit()


class DeleteInSession(Strategy):
    def delete_cart(self):
        del_session_vars('active_cart')

