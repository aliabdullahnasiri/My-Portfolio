from flask import Blueprint

from app.func import __import_all__
from app.models.user import admin_required

bp = Blueprint("admin", __name__)


@bp.before_request
@admin_required
def _(): ...


__import_all__("app/blueprints/admin/routes")
