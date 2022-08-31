from flask import Blueprint
from src.blueprints.core import routes

bp = Blueprint('core', __name__)


def config(app):
    app.register_blueprint(routes.main_page)
    app.register_blueprint(bp)
