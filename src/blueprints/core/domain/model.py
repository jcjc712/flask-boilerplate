from __future__ import annotations
from datetime import date
from typing import Optional, List
from . import events


class TodoList:
    def __init__(self, name: str, user_id: int, created_at: Optional[date], id: Optional[int] = None):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.events = []  # type: List[events.Event]
        self.created_at = created_at
