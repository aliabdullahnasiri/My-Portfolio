from flask import Blueprint

from app.func import __import_all__

bp = Blueprint("auth", __name__)


__import_all__("app/blueprints/auth/routes")
