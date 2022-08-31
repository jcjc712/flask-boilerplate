from flask import Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import src.config
from flask import jsonify
from flask import request
from src.blueprints.auth.domain import commands
from src.blueprints.auth.service_layer import messagebus, unit_of_work
from flask_jwt_extended import get_jwt, jwt_required
from src.extension import jwt
from src.blueprints.auth.service_layer.handlers import LoginException


get_session = sessionmaker(bind=create_engine(src.config.get_mysql_uri()))
api = Blueprint('api', __name__, url_prefix='/auth')


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    cache = src.config.get_cache_client()
    token_in_redis = cache.get(jti)
    return token_in_redis is not None


@api.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    cache = src.config.get_cache_client()
    cache.set(jti, "")
    return jsonify(msg="Access token revoked")


@api.route('/register', methods=["POST"])
def register():
    print(request.remote_addr)
    username = request.json.get('username')
    password = request.json.get('password')

    cmd = commands.CreateUser(username, password)

    uow = unit_of_work.SqlAlchemyUnitOfWork()
    result = messagebus.handle(cmd, uow)
    return jsonify(message=result[0])


@api.route('/login', methods=["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    cmd = commands.Login(username, password)
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    try:
        result = messagebus.handle(cmd, uow)
        response = jsonify(message='success', access_token=result[0])
        return response, 200
    except LoginException:
        return jsonify(message='login failed'), 401
