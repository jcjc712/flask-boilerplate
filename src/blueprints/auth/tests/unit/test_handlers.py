from src.blueprints.auth.adapters import repository
from src.blueprints.auth.domain import commands
from src.blueprints.auth.service_layer import messagebus, unit_of_work


class FakeRepository(repository.AbstractUserRepository):

    def __init__(self, products):
        super().__init__()
        self._products = set(products)

    def _add(self, product):
        self._products.add(product)

    def _get(self, name):
        return next((p for p in self._products if p.name == name), None)

    def _filter(self, params: {}):
        return None


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):

    def __init__(self):
        self.users = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_todo():
    uow = FakeUnitOfWork()
    messagebus.handle(
        commands.CreateUser("juan", "abc123"), uow
    )
    assert uow.users.get("juan") is not None
    assert uow.committed
