from __future__ import annotations
from typing import TYPE_CHECKING
from src.blueprints.core.domain import commands, model
if TYPE_CHECKING:
    from . import unit_of_work


def add_todo(
        cmd: commands.CreateTodo, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        uow.todo.add(todo=model.TodoList(name=cmd.name, user_id=cmd.user_id, created_at=cmd.created_at))
        uow.commit()


def retrieve_todo(cmd: commands.RetrieveTodoList, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        user = uow.users.get(cmd.user_id)
        return [{"id":todo.id, "name": todo.name} for todo in user.todo_list]
