from flask import render_template

from app.blueprints.admin import bp


@bp.get("/")
@bp.get("/dashboard")
def dashboard():
    return render_template("admin/pages/dashboard.html", title="Dashboard")
