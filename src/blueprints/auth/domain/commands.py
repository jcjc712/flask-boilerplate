from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreateUser(Command):
    username: str
    password: str


@dataclass
class Login(Command):
    username: str
    password: str
