from flask import render_template

from app.blueprints.admin import bp


@bp.get("/users")
def users():
    return render_template("admin/pages/users.html", title="Users")
