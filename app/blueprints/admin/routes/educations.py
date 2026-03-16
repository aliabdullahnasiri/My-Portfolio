from flask import render_template

from app.blueprints.admin import bp
from app.forms.education import AddEducationForm, UpdateEducationForm
from app.models.user import admin_required


@bp.get("/educations")
@admin_required
def educations():
    return render_template(
        "admin/pages/educations.html",
        title="Educations",
        form={"a": AddEducationForm(), "u": UpdateEducationForm()},
    )
