from flask import Blueprint

from app.func import __import_all__

bp = Blueprint("admin", __name__)


__import_all__("app/blueprints/admin/routes")
