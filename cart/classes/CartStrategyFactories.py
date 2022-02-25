from __future__ import annotations
from abc import ABC, abstractmethod

from cart.classes.ChangeQuantityInCart import *
from cart.classes.AddToCart import *


class AbstractFactory(ABC):

    @abstractmethod
    def create_customer_strategy(self, strategy_data):
        pass

    @abstractmethod
    def create_session_strategy(self, strategy_data):
        pass


class IncreaseStrategyFactory(AbstractFactory):

    def create_customer_strategy(self, strategy_data) -> IncreaseInCustomer:
        return IncreaseInCustomer(strategy_data)

    def create_session_strategy(self, strategy_data) -> IncreaseInSession:
        return IncreaseInSession(strategy_data)


class DecreaseStrategyFactory(AbstractFactory):

    def create_customer_strategy(self, strategy_data) -> DecreaseInCustomer:
        return DecreaseInCustomer(strategy_data)

    def create_session_strategy(self, strategy_data) -> DecreaseInSession:
        return DecreaseInSession(strategy_data)


class AddToCartFactory(AbstractFactory):

    def create_customer_strategy(self, strategy_data) -> AddToCustomer:
        return AddToCustomer(strategy_data)

    def create_session_strategy(self, strategy_data) -> AddToSession:
        return AddToSession(strategy_data)
