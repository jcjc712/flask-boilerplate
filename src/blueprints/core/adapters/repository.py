import abc
from typing import Set
from src.blueprints.core.domain import model


class AbstractTodoRepository(abc.ABC):

    def __init__(self):
        self.seen = set()  # type: Set[model.TodoList]

    def add(self, todo: model.TodoList):
        self._add(todo)
        self.seen.add(todo)

    def get(self, id) -> model.TodoList:
        todo = self._get(id)
        if todo:
            self.seen.add(todo)
        return todo

    @abc.abstractmethod
    def _add(self, todo: model.TodoList):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id) -> model.TodoList:
        raise NotImplementedError


class SqlAlchemyTodoRepository(AbstractTodoRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, todo):
        self.session.add(todo)

    def _get(self, id):
        return self.session.query(model.TodoList).filter_by(id=id).first()
