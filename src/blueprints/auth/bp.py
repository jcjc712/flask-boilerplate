from flask import Blueprint
from src.blueprints.auth import routes

bp = Blueprint('auth', __name__)


def config(app):
    app.register_blueprint(routes.api)
    app.register_blueprint(bp)
