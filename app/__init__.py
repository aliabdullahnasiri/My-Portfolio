import os
from typing import Dict

from flask import Flask, current_app, url_for

import app.models as _
from app.blueprints.admin import bp as admin_bp
from app.blueprints.api import bp as api_bp
from app.blueprints.auth import bp as auth_bp
from app.blueprints.main import bp as main_bp
from app.config import Config
from app.extensions import bcrypt, db, login_manager, migrate
from app.models.permission import Permission


def ctx() -> Dict:
    dct: Dict = {
        "PROJECT_TITLE": Config.PROJECT_TITLE,
        "DEFAULT_AVATAR_URL": url_for(
            "static", filename=current_app.config["DEFAULT_AVATAR"]
        ),
        "DEVELOPER": "Ali Abdullah Nasiri",
        "CURRENCY_SYMBOL": current_app.config["CURRENCY_SYMBOL"],
    }

    return dct


def create_app(config_class: type[Config] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(config_class or Config())

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    @app.context_processor
    def _():
        dct = ctx()
        return {"CURRENT_APP": current_app, **dct}

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(main_bp)

    with app.app_context():
        if Permission.administer():
            Permission.refresh()

    return app
