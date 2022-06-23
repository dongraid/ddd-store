from abc import ABC, abstractmethod
from domain import model


class AbstractRepository(ABC):

    def __init__(self):
        self.seen = set()

    @abstractmethod
    def _add(self, product: model.Product):
        raise NotImplemented

    @abstractmethod
    def _get(self, product: model.Product):
        raise NotImplemented

    def get(self, name):
        product = self._get(name)
        if product:
            self.seen.add(product)
        return product

    def add(self, product):
        self._add(product)
        self.seen.add(product)


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session
        super().__init__()

    def _add(self, product):
        self.session.add(product)

    def _get(self, name):
        return self.session.query(model.Product).filter_by(name=name).first()
