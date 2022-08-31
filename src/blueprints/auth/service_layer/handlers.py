from __future__ import annotations
from typing import TYPE_CHECKING
from src.blueprints.auth.domain import commands, model
from flask_jwt_extended import get_jwt, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
if TYPE_CHECKING:
    from . import unit_of_work


def add_user(
        cmd: commands.CreateUser, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        user = uow.users.filter({'name': cmd.username})

        if user is not None:
            return 'username exist'
        hashed_password = generate_password_hash(cmd.password)
        user = model.User(name=cmd.username, password=hashed_password)
        uow.users.add(user)
        uow.commit()
        return 'user created'


class LoginException(Exception):
    pass


def login(
        cmd: commands.Login, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        user = uow.users.filter({'name': cmd.username})
        if user is not None and check_password_hash(user.password, cmd.password):
            access_token = create_access_token(identity=cmd.username)
            return access_token
        else:
            raise LoginException
