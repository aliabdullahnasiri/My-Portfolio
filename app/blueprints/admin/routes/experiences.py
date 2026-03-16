from flask import render_template

from app.blueprints.admin import bp
from app.forms.experience import AddExperienceForm, UpdateExperienceForm
from app.models.user import admin_required


@bp.get("/experiences")
@admin_required
def experiences():
    return render_template(
        "admin/pages/experiences.html",
        title="Experiences",
        form={"a": AddExperienceForm(), "u": UpdateExperienceForm()},
    )
