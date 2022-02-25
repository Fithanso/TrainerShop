from abc import ABC, abstractmethod
from account.models.Customer import CustomerModel


class Strategy(ABC):
    @abstractmethod
    def search(self, search_query):
        pass


class AccountSearcher:

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


class SearchByPhoneNumber(Strategy):
    def search(self, search_query):
        results = CustomerModel.query.filter(CustomerModel.phone_number == search_query).all()
        return results


class SearchByName(Strategy):
    def search(self, search_query):
        splitted_query = search_query.split(' ')
        search_queries = ["%{}%".format(query) for query in splitted_query]
        results = CustomerModel.query.filter(CustomerModel.name.ilike(search_queries[0]),
                                             CustomerModel.surname.ilike(search_queries[1]),
                                             CustomerModel.patronymic.ilike(search_queries[2])).all()

        return results
