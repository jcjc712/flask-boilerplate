# pylint: disable=protected-access
from src.blueprints.auth.domain import model
from src.blueprints.auth.adapters import repository


def test_get_by_batchref(session):
    repo = repository.SqlAlchemyUserRepository(session)
    b1 = model.User(name='juan', password="abc123")
    b2 = model.User(name='david', password="abc123")
    repo.add(b1)
    repo.add(b2)
    assert repo.get(1) == b1
    assert repo.get(2) == b2
