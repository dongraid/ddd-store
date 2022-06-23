from abc import ABC, abstractmethod
from adapters import repository

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class AbstractUnitOfWork(ABC):
    products: repository.AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self,  *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplemented

    @abstractmethod
    def rollback(self):
        raise NotImplemented

    def collect_new_events(self):
        for product in self.products.seen:
            while product.events:
                yield product.events.pop(0)


DEFAULT_SESSION_FACTORY = sessionmaker(
    # Never save credentials in git! It's only for example purpose
    bind=create_engine(
        "postgresql://vitalii:12345@localhost:54321/store",
        isolation_level="REPEATABLE READ",
    )
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.products = repository.SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
