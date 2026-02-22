from flask import render_template

from app.blueprints.admin import bp
from app.models.user import admin_required


@bp.get("/permissions")
@admin_required
def permissions():
    return render_template("admin/pages/permissions.html", title="Permissions")
