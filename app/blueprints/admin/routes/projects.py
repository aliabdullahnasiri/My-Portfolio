from flask import render_template

from app.blueprints.admin import bp
from app.forms.project import AddProjectForm, UpdateProjectForm
from app.models.user import admin_required


@bp.get("/projects")
@admin_required
def projects():
    return render_template(
        "admin/pages/projects.html",
        title="Projects",
        form={"a": AddProjectForm(), "u": UpdateProjectForm()},
    )
