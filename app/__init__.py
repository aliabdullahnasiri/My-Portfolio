import os

from flask import Flask

from app.config import Config
from app.extensions import bcrypt, db, login_manager, migrate


def create_app(config_class: type[Config] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(config_class or Config())

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app
