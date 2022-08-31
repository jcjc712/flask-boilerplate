from flask import Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import src.config
from datetime import datetime
from flask import request
from src.blueprints.core.domain import commands
from src.blueprints.core.adapters import orm
from src.blueprints.core.service_layer import messagebus, unit_of_work
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.extension import limiter

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(src.config.get_mysql_uri()))
main_page = Blueprint('main_page', __name__)


@main_page.route('/', methods=['GET'])
@jwt_required()
@limiter.limit("5/minute")
def index():
    cache = src.config.get_cache_client()
    print(get_jwt_identity())
    if cache.exists('foo99'):
        return {'message': str(cache.get('foo99'))}
    cache.set('foo99', "bar")
    return 'No cache'


@main_page.route('/todo', methods=['GET'])
@jwt_required()
@limiter.limit("5/minute")
def todo():
    cmd = commands.RetrieveTodoList(user_id=request.json['user_id'])
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    results = messagebus.handle(cmd, uow)
    return results[0], 200


@main_page.route("/add_todo", methods=['POST'])
@jwt_required()
@limiter.limit("5/minute")
def add_todo():
    created_at = request.json['created_at']
    if created_at is not None:
        created_at = datetime.fromisoformat(created_at).date()
    cmd = commands.CreateTodo(
        request.json['name'], request.json['user_id'], created_at,
    )
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    messagebus.handle(cmd, uow)
    return 'OK', 201
