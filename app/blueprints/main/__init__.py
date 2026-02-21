from flask import Blueprint

from app.func import __import_all__

bp = Blueprint("main", __name__)


__import_all__("app/blueprints/main/routes")
