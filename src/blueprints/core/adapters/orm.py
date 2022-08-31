from src.blueprints.core.domain import model
from src.blueprints.auth.domain.model import User

from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, ForeignKey,
    event,
)
from sqlalchemy.orm import mapper, relationship


metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255)),
    Column('password', String(255)),
    Column('created_at', Date, nullable=True),
)


todo_list = Table(
    'todo_list', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255)),
    Column('user_id', ForeignKey('users.id')),
    Column('created_at', Date, nullable=True),
)


def start_mappers():
    todo_list_mapper = mapper(model.TodoList, todo_list)
    mapper(User, users, properties={
        'todo_list': relationship(todo_list_mapper)
    })


@event.listens_for(User, 'load')
def receive_load(user, _):
    user.events = []


@event.listens_for(model.TodoList, 'load')
def receive_load(todo, _):
    todo.events = []
