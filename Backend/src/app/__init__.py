from flask import Flask
from .config import Config
from .database import db
from flask_migrate import Migrate
from .utils.data_fill import init_data
from flask_cors import CORS

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, origins=['http://localhost:5174'])
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api')

    init_data(app, db)

    return app
