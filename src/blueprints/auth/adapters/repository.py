import abc
from typing import Set
from src.blueprints.auth.domain import model


class AbstractUserRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.User]

    def add(self, user: model.User):
        self._add(user)
        self.seen.add(user)

    def get(self, id) -> model.User:
        user = self._get(id)
        if user:
            self.seen.add(user)
        return user

    def filter(self, params: {}):
        user = self._filter(params)
        if user:
            self.seen.add(user)
        return user

    @abc.abstractmethod
    def _add(self, product: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> model.User:
        raise NotImplementedError

    @abc.abstractmethod
    def _filter(self, params: {}) -> model.User:
        raise NotImplementedError


class SqlAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, user):
        self.session.add(user)

    def _get(self, id):
        return self.session.query(model.User).filter_by(id=id).first()

    def _filter(self, params: {}):
        return self.session.query(model.User).filter_by(**params).first()
