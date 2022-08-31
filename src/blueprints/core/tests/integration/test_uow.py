from src.blueprints.core.service_layer import unit_of_work


def insert_todo(session, name):
    session.execute(
        'INSERT INTO users (name, password) VALUES (:name, :password)',
        dict(name="juan", password="abc123"),
    )
    session.execute(
        'INSERT INTO todo_list (name, user_id) VALUES (:name, :user_id)',
        dict(name=name, user_id=1),
    )


def test_user_creation(session_factory):
    session = session_factory()
    insert_todo(session, 'Comprar')
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        todo = uow.todo.get(1)
        assert todo.name == 'Comprar'
