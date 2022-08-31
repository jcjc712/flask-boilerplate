from src.blueprints.auth.service_layer import unit_of_work


def insert_user(session):
    session.execute(
        'INSERT INTO users (name, password) VALUES (:name, :password)',
        dict(name="juan", password="abc123"),
    )


def test_user_creation(session_factory):
    session = session_factory()
    insert_user(session)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        todo = uow.users.get(1)
        assert todo.name == 'juan'
