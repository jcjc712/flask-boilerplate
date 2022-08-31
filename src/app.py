from flask import Flask
from src.config import get_mysql_uri
from src.blueprints.core.adapters.orm import metadata
from sqlalchemy import create_engine
from src.extension import jwt, limiter
import src.config
import os


def create_app():
    engine = create_engine(src.config.get_mysql_uri())
    app = Flask(__name__)
    metadata.create_all(engine)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)
    app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY', None)
    jwt.init_app(app)
    limiter.init_app(app)
    from src.blueprints.core import bp as bp_core
    from src.blueprints.auth import bp as bp_auth
    bp_core.config(app)
    bp_auth.config(app)
    return app
