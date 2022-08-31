# pylint: disable=protected-access
from src.blueprints.core.domain import model
from src.blueprints.core.adapters import repository


def test_get_by_batchref(session):
    repo = repository.SqlAlchemyTodoRepository(session)
    b1 = model.TodoList(name='b1', user_id=1, created_at=None)
    b2 = model.TodoList(name='b2', user_id=1, created_at=None)
    repo.add(b1)
    repo.add(b2)
    assert repo.get(1) == b1
    assert repo.get(2) == b2
