from src.blueprints.core.adapters import repository
from src.blueprints.core.domain import commands
from src.blueprints.core.service_layer import handlers, messagebus, unit_of_work


class FakeRepository(repository.AbstractTodoRepository):

    def __init__(self, products):
        super().__init__()
        self._products = set(products)

    def _add(self, product):
        self._products.add(product)

    def _get(self, name):
        return next((p for p in self._products if p.name == name), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):

    def __init__(self):
        self.todo = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_todo():
    uow = FakeUnitOfWork()
    messagebus.handle(
        commands.CreateTodo("b1", 1, None), uow
    )
    assert uow.todo.get("b1") is not None
    assert uow.committed
