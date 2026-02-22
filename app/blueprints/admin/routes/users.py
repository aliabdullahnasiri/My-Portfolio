from flask import render_template

from app.blueprints.admin import bp
from app.models.user import admin_required


@bp.get("/users")
@admin_required
def users():
    return render_template("admin/pages/users.html", title="Users")
