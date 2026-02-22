from flask import render_template

from app.blueprints.admin import bp
from app.models.user import admin_required


@bp.get("/dashboard")
@admin_required
def dashboard():
    return render_template("admin/pages/dashboard.html", title="Dashboard")
