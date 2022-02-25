from application import db

from order.models.Order import OrderModel

from abc import ABC, abstractmethod
from sqlalchemy import desc


class Strategy(ABC):
    @abstractmethod
    def search(self, search_query):
        pass


class OrderSearcher:

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy) -> None:
        self._strategy = strategy

    def search(self, search_query):
        result = self._strategy.search(search_query)
        if not isinstance(result, list):
            result = [result]

        return result


class SearchById(Strategy):
    def search(self, search_query):
        result_entity = OrderModel.query.get(int(search_query))
        return result_entity


class SearchByPhoneNumber(Strategy):
    def search(self, search_query):
        result_entities = OrderModel.query.filter(OrderModel.recipient_phone_number == search_query)
        result_entities = result_entities.order_by(desc(OrderModel.order_datetime)).all()

        return result_entities


class SearchByName(Strategy):
    def search(self, search_query):
        splitted_query = search_query.split(' ')
        search_queries = ["%{}%".format(query) for query in splitted_query]
        result_entities = OrderModel.query.filter(OrderModel.recipient_name.ilike(search_queries[0]),
                                                  OrderModel.recipient_surname.ilike(search_queries[1]),
                                                  OrderModel.recipient_patronymic.ilike(search_queries[2]))
        result_entities = result_entities.order_by(desc(OrderModel.order_datetime)).all()

        return result_entities
