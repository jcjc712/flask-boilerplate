from __future__ import annotations
from datetime import date
from typing import Optional, List
from . import events
from src.blueprints.core.domain import model


class User:
    def __init__(self, name: str, password: str, created_at: Optional[date] = None, todo_list: List[model.TodoList] = []):
        self.name = name
        self.password = password
        self.created_at = created_at
        self.todo_list = todo_list
        self.events = []  # type: List[events.Event]
