from flask import session
from application import db

from account.models.Customer import CustomerModel

from helpers import del_session_vars
from abc import ABC, abstractmethod

import json


class Strategy(ABC):
    @abstractmethod
    def delete_cart(self):
        pass


class EmptyCart:

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


class EmptyInCustomer(Strategy):

    def __init__(self, customer_entity):
        super().__init__()
        self.customer_entity = customer_entity

    def delete_cart(self):

        # condition may be pointless, but I'll leave it anyway, in case the direct request is sent
        if self.customer_entity.active_cart is not None:
            empty_cart = {}
            self.customer_entity.active_cart = json.dumps(empty_cart)

            db.session.commit()


class EmptyInSession(Strategy):
    def delete_cart(self):
        del_session_vars('active_cart')

