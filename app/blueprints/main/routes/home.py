from flask import Response

from app.blueprints.main import bp


@bp.get("/")
def home() -> Response: ...
