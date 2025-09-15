import os

from flask import Flask
from .config import Config
from .database import db
from .login import jwt
from flask_migrate import Migrate
from .utils.data_fill import init_data
from flask_cors import CORS

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    os.makedirs(Config.EXPORTS_DIR, exist_ok=True)

    from . import models

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api')

    init_data(app, db)

    return app
