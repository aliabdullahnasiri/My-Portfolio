from flask import render_template

from app.blueprints.admin import bp
from app.models.user import admin_required


@bp.get("/roles")
@admin_required
def roles():
    return render_template("admin/pages/roles.html", title="Roles")
