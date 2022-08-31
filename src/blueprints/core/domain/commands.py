from datetime import date
from typing import Optional
from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreateTodo(Command):
    name: str
    user_id: int
    created_at: Optional[date] = None


@dataclass
class RetrieveTodoList(Command):
    user_id: int
