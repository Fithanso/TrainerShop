from app import db
from abc import ABC, abstractmethod
from order.models.Order import OrderModel


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
        return self._strategy.search(search_query)


class SearchById(Strategy):
    def search(self, search_query):
        result_entity = OrderModel.query.get(int(search_query))
        return result_entity


class SearchByPhoneNumber(Strategy):
    def search(self, search_query):
        result_entities = OrderModel.query.filter(OrderModel.recipient_phone_number == search_query).all()
        return result_entities


class SearchByName(Strategy):
    def search(self, search_query):
        splitted_query = search_query.split(' ')
        search_queries = ["%{}%".format(query) for query in splitted_query]
        result_entities = OrderModel.query.filter(OrderModel.recipient_name.ilike(search_queries[0]),
                                                  OrderModel.recipient_surname.ilike(search_queries[1]),
                                                  OrderModel.recipient_patronymic.ilike(search_queries[2])).all()

        return result_entities
