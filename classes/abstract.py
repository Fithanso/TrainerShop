from abc import ABC, abstractmethod
from typing import Any, Optional

"""file stores all abstract classes used in many blueprints"""


class Repository(ABC):

    @property
    def model(self):
        return self.model

    @model.setter
    def model(self, model):
        self.model = model

    @staticmethod
    @abstractmethod
    def create_id() -> int:
        pass


class CORHandler(ABC):

    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(CORHandler):

    _next_handler: CORHandler = None

    def set_next(self, handler: CORHandler) -> CORHandler:
        self._next_handler = handler

        return handler

    @abstractmethod
    def handle(self, request: Any) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)

        return ''
