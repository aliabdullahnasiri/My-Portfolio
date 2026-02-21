import os

from flask import Flask

import app.models as _
from app.blueprints.admin import bp as admin_bp
from app.blueprints.api import bp as api_bp
from app.blueprints.auth import bp as auth_bp
from app.blueprints.main import bp as main_bp
from app.config import Config
from app.extensions import bcrypt, db, login_manager, migrate
from app.models.permission import Permission


def create_app(config_class: type[Config] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(config_class or Config())

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(main_bp)

    with app.app_context():
        if Permission.administer():
            Permission.refresh()

    return app
